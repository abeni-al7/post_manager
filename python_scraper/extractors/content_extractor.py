"""
Extracts the article body content from an HTML page.
Strips navigation, headers, footers, and other chrome elements.
"""
import re
from bs4 import BeautifulSoup, Tag


def extract_content(soup: BeautifulSoup) -> str | None:
    """
    Extract the clean article body text from the parsed HTML.
    Removes navigation elements, ads, scripts, and other non-content areas.
    Returns the text with paragraphs separated by double newlines.
    """
    # Remove unwanted elements first
    _remove_non_content_elements(soup)

    # Strategy 1: Find the main content table — typically table id="table312"
    # inside the larger layout. This contains the article body spans.
    content_table = soup.find("table", id="table312")
    if content_table:
        text = _extract_content_from_table(content_table)
        if text and len(text) > 50:
            return text

    # Strategy 2: Look for the main content section by finding the
    # largest block of <span style="font-size: 9.0pt; font-family: Verdana">
    content_spans = soup.find_all(
        "span",
        style=lambda v: v and "font-size: 9.0pt" in v and "font-family: Verdana" in v,
    )
    if content_spans:
        # Filter out spans that are too short (likely labels, not article text)
        paragraphs = []
        for span in content_spans:
            text = span.get_text(strip=True)
            # Skip very short fragments (navigation labels, copyright, etc.)
            if len(text) < 20:
                continue
            # Skip spans that are clearly navigation
            parent_text = _get_parent_text_context(span)
            if "classifieds" in parent_text.lower() or "archive" in parent_text.lower():
                continue
            paragraphs.append(text)

        if paragraphs:
            return "\n\n".join(paragraphs)

    # Strategy 3: Last resort — grab all text from <td> elements
    # that contain substantial paragraphs
    td_elements = soup.find_all("td")
    paragraphs = []
    for td in td_elements:
        text = td.get_text(strip=True, separator="\n")
        lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 40]
        if lines:
            paragraphs.extend(lines)

    if paragraphs:
        joined = "\n\n".join(paragraphs)
        # Clean up the text
        joined = _clean_text(joined)
        if len(joined) > 100:
            return joined

    return None


def _remove_non_content_elements(soup: BeautifulSoup) -> None:
    """Remove non-content elements from the soup in-place."""
    # Remove scripts
    for tag in soup.find_all(["script", "style", "noscript"]):
        tag.decompose()

    # Remove iframes (typically ads or navigation)
    for tag in soup.find_all("iframe"):
        tag.decompose()

    # Remove object/embed (Flash ads)
    for tag in soup.find_all(["object", "embed"]):
        tag.decompose()

    # Remove form elements (search forms)
    for tag in soup.find_all("form"):
        tag.decompose()


def _extract_content_from_table(table: Tag) -> str | None:
    """Extract text from the main content table."""
    paragraphs = []

    # Find all content spans within the table
    content_spans = table.find_all(
        "span",
        style=lambda v: v and "font-size: 9.0pt" in v and "font-family: Verdana" in v,
    )

    for span in content_spans:
        text = span.get_text(strip=True)
        # Skip very short or boilerplate text
        if len(text) < 30:
            continue
        # Skip navigation-like text
        if any(
            keyword in text.lower()
            for keyword in [
                "back to addis fortune",
                "home page",
                "read more",
                "fortune news",
                "more letters",
            ]
        ):
            continue
        paragraphs.append(text)

    if not paragraphs:
        return None

    return "\n\n".join(paragraphs)


def _get_parent_text_context(tag: Tag) -> str:
    """Get the text context of parent elements to help classify the span."""
    texts = []
    parent = tag.parent
    for _ in range(3):  # Check up to 3 levels up
        if parent is None:
            break
        if hasattr(parent, "get_text"):
            texts.append(parent.get_text(strip=True)[:100])
        parent = parent.parent if hasattr(parent, "parent") else None
    return " ".join(texts)


def _clean_text(text: str) -> str:
    """Clean up extracted text — remove excess whitespace and HTML artifacts."""
    # Replace multiple newlines with double newline
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Replace multiple spaces with single space
    text = re.sub(r" {2,}", " ", text)
    # Remove leading/trailing whitespace on each line
    lines = [line.strip() for line in text.split("\n")]
    # Remove empty lines that don't separate paragraphs
    cleaned = []
    prev_empty = False
    for line in lines:
        if not line:
            if not prev_empty:
                cleaned.append("")
            prev_empty = True
        else:
            cleaned.append(line)
            prev_empty = False
    return "\n".join(cleaned).strip()