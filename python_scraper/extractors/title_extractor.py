"""
Extracts the article title from an HTML page.
Uses multiple fallback strategies in priority order.
"""
from bs4 import BeautifulSoup


def extract_title(soup: BeautifulSoup) -> str | None:
    """
    Extract the article title from the parsed HTML.
    
    Priority:
    1. Large bold heading: <span style="font-size: 14.0pt; font-family: Verdana">
       or <span style="font-size: 18.0pt; ..."> inside the main content area
    2. The HTML <title> tag (cleaned up)
    3. First <h1> tag
    """
    # Strategy 1: Look for large bold heading spans in the main content area
    candidates = soup.find_all(
        "span",
        style=lambda v: v and ("font-size: 14.0pt" in v or "font-size: 18.0pt" in v)
                        and "font-family: Verdana" in v
    )
    for candidate in candidates:
        text = candidate.get_text(strip=True)
        # Clean up newlines and extra whitespace
        text = " ".join(text.split())
        # Skip short fragments or empty text
        if len(text) > 10:
            return text

    # Strategy 2: Look for <b> or <strong> with large font size inside content
    for tag in soup.find_all(["b", "strong"]):
        inner = tag.find("span", style=lambda v: v and "font-size: 14" in (v or ""))
        if inner:
            text = inner.get_text(strip=True)
            if len(text) > 10:
                return text

    # Strategy 3: Use the HTML <title> tag
    title_tag = soup.find("title")
    if title_tag:
        text = title_tag.get_text(strip=True)
        # Clean up common suffixes
        for suffix in [
            " - Addis Fortune-Content Matters",
            " | Addis Fortune",
            "Addis Fortune-Content Matters:",
        ]:
            if text.endswith(suffix):
                text = text[: -len(suffix)].strip()
            if text.startswith(suffix):
                text = text[len(suffix) :].strip()
        if text and len(text) > 5:
            return text

    # Strategy 4: First <h1> tag
    h1 = soup.find("h1")
    if h1:
        text = h1.get_text(strip=True)
        if text:
            return text

    return None