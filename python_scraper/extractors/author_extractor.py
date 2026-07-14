"""
Extracts the author/byline from an HTML page.
"""
import re
from bs4 import BeautifulSoup


def extract_author(soup: BeautifulSoup) -> str | None:
    """
    Extract the article author from the parsed HTML.
    
    The Addis Fortune archive typically places the author at the bottom
    of the content area with patterns like:
      "By WUDINEH ZENEBE"
      "By DANIEL KIFLE"
      "SPECIAL TO FORTUNE"
      "FORTUNE STAFF WRITER"
    """
    # Look in the bottom-right area of the content table for the byline
    # Strategy 1: Find the signature block — typically inside table id="table316"
    # which contains "By" italic + uppercase author name
    signature_table = soup.find("table", id="table315")
    if signature_table:
        text = signature_table.get_text(strip=True)
        author = _extract_author_from_text(text)
        if author:
            return author

    signature_table = soup.find("table", id="table316")
    if signature_table:
        text = signature_table.get_text(strip=True)
        author = _extract_author_from_text(text)
        if author:
            return author

    # Strategy 2: Search for "By" pattern in the entire document
    # Look for <i>By</i> or <i>By </i> followed by uppercase text
    for italic in soup.find_all("i"):
        if italic.get_text(strip=True).lower() in ("by", "by "):
            # The author name is typically in the same parent or next sibling
            parent = italic.parent
            if parent:
                full_text = parent.get_text(strip=True)
                author = _extract_author_from_text(full_text)
                if author:
                    return author

            # Or the next sibling/adjacent element
            next_elem = italic.find_next_sibling()
            if next_elem:
                text = next_elem.get_text(strip=True)
                author = _extract_author_from_text(text)
                if author:
                    return author

    # Strategy 3: Regex search on the full page text for common patterns
    body_text = soup.get_text()
    patterns = [
        r"By\s+([A-Z][A-Z\s\.]+)\s*(?:FORTUNE|SPECIAL)",
        r"By\s+([A-Z][A-Z\s\.]+)$",
        r"(FORTUNE\s+STAFF\s+WRITER)",
        r"(SPECIAL\s+TO\s+FORTUNE)",
    ]
    for pattern in patterns:
        match = re.search(pattern, body_text, re.MULTILINE)
        if match:
            name = match.group(1).strip()
            if name:
                return name.title().strip()

    return None


def _extract_author_from_text(text: str) -> str | None:
    """Try to extract an author name from a text fragment."""
    # Pattern: "By NAME" or "By NAME FORTUNE STAFF WRITER"
    match = re.search(r"By\s+([A-Z][A-Z\s\.]+)", text)
    if match:
        name = match.group(1).strip()
        # Filter out false positives (e.g., "By Berhanu Mekonnen")
        if len(name) > 3 and not any(
            keyword in name.lower()
            for keyword in ["editor", "fortune", "addis", "click", "read more"]
        ):
            return name.title().strip()

    # Pattern: standalone role titles
    if "FORTUNE STAFF WRITER" in text.upper():
        return "FORTUNE STAFF WRITER"

    if "SPECIAL TO FORTUNE" in text.upper():
        return "SPECIAL TO FORTUNE"

    return None