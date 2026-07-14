"""
Extracts metadata from an HTML page: volume number, issue number,
published date, and the subtitle/teaser.
"""
import re
from datetime import datetime
from bs4 import BeautifulSoup, Tag


def extract_subtitle(soup: BeautifulSoup) -> str | None:
    """
    Extract the article subtitle or teaser (the bold line above the title).
    This is typically in a <span> with class='Berhanu3' or a bold paragraph
    right before the main heading.
    """
    # Look for the subtitle in the row before the title
    # In the archive, it's often a <p class="Berhanu3"> above the heading
    subtitle_para = soup.find("p", class_="Berhanu3")
    if subtitle_para:
        text = subtitle_para.get_text(strip=True)
        if len(text) > 20:
            return text

    # Alternative: find a bold/subtitle span right before the main title
    title_span = soup.find(
        "span",
        style=lambda v: v and "font-size: 14.0pt" in v and "font-family: Verdana" in v,
    )
    if title_span:
        # Check the previous row/paragraph
        parent_tr = title_span.find_parent("tr")
        if parent_tr:
            prev_tr = parent_tr.find_previous_sibling("tr")
            if prev_tr:
                text = prev_tr.get_text(strip=True)
                if text and len(text) > 20:
                    return text

    return None


def extract_volume_and_issue(soup: BeautifulSoup) -> tuple[str | None, str | None]:
    """
    Extract volume and issue number from the page.
    These are typically in iframe src="volume_Number.htm" which contains
    "Volume 7, Number 364" — but since we parse individual articles,
    we look for any mention of volume/number in the page text.
    """
    body_text = soup.get_text()

    # Pattern: "Volume X, Number Y" or "Vol X No Y"
    vol_match = re.search(r"Volume\s+(\d+)[,\s]+(?:Number|No)[.\s]*(\d+)", body_text)
    if vol_match:
        return f"Volume {vol_match.group(1)}", vol_match.group(2)

    vol_match = re.search(r"Vol[.\s]*(\d+)[,\s]+No[.\s]*(\d+)", body_text)
    if vol_match:
        return f"Volume {vol_match.group(1)}", vol_match.group(2)

    return None, None


def _convert_to_mysql_date(date_str: str) -> str | None:
    """
    Convert a date string to MySQL-compatible format (YYYY-MM-DD).
    
    Args:
        date_str: Date string in various formats (e.g., "April 22, 2007", "22 April 2007")
        
    Returns:
        Date string in YYYY-MM-DD format, or None if conversion fails
    """
    if not date_str:
        return None
    
    # Clean up the date string
    date_str = date_str.strip()
    
    # Try different date formats
    date_formats = [
        "%B %d, %Y",      # "April 22, 2007"
        "%B %d %Y",       # "April 22 2007"
        "%d %B %Y",       # "22 April 2007"
        "%d %B, %Y",      # "22 April, 2007"
        "%Y-%m-%d",       # "2007-04-22" (already in correct format)
        "%m/%d/%Y",       # "04/22/2007"
        "%d/%m/%Y",       # "22/04/2007"
    ]
    
    for fmt in date_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    # If none of the formats matched, try to extract with regex
    # Pattern: Month Day, Year or Day Month Year
    match = re.search(
        r"(\d{1,2})[\/\s]+(\d{1,2})[\/\s]+(\d{4})", date_str
    )
    if match:
        # Could be MM/DD/YYYY or DD/MM/YYYY - assume MM/DD/YYYY for US format
        try:
            dt = datetime.strptime(match.group(0), "%m/%d/%Y")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            try:
                dt = datetime.strptime(match.group(0), "%d/%m/%Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
    
    return None


def extract_published_date(soup: BeautifulSoup) -> str | None:
    """
    Extract the published date from the page.
    The date is typically in an iframe src="Published On.htm" which contains
    "April 22, 2007". On the article page, look for date patterns.
    
    Returns the date in MySQL-compatible format (YYYY-MM-DD).
    """
    body_text = soup.get_text()

    # Pattern: "Published On April 22, 2007"
    date_match = re.search(
        r"Published\s+On[:\s]*([A-Z][a-z]+\s+\d{1,2},?\s*\d{4})", body_text
    )
    if date_match:
        date_str = date_match.group(1).strip()
        return _convert_to_mysql_date(date_str)

    # Pattern: standalone date in the page
    date_match = re.search(
        r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})",
        body_text,
    )
    if date_match:
        date_str = f"{date_match.group(1)} {date_match.group(2)}, {date_match.group(3)}"
        return _convert_to_mysql_date(date_str)

    return None
