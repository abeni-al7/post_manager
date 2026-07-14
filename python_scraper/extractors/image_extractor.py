"""
Extracts image references from an HTML page.
Returns image paths relative to the archive directory.
"""
import os
from bs4 import BeautifulSoup


# Image files that are layout/design elements, not article images
LAYOUT_IMAGE_KEYWORDS = [
    "addisvirtical",
    "fortunetopbanner",
    "aboutuses",
    "advertise",
    "classified",
    "contact",
    "contribute",
    "fortuneoff",
    "fortuneon",
    "newsoff",
    "newson",
    "newsinbrief",
    "agenda",
    "editorsnote",
    "opinion",
    "comments",
    "viewpoint",
    "perspective",
    "lifematters",
    "viewfromarada",
    "restaurant",
    "business",
    "cartoon",
    "gossip",
    "archive",
    "guest",
    "homepage",
    "bottomad",
    "top right banner",
    "ad here",
    "slide",
    "star.gif",
]


def _is_layout_image(src: str) -> bool:
    """Check if an image is a layout/design element rather than article content."""
    lower_src = src.lower()
    for keyword in LAYOUT_IMAGE_KEYWORDS:
        if keyword in lower_src:
            return True
    return False


def extract_images(soup: BeautifulSoup, source_file: str) -> list[dict]:
    """
    Extract article image references from the parsed HTML.
    
    Returns a list of dicts with keys:
      - image_path: relative path to the image
      - alt_text: alt text of the image (if any)
    """
    images = []
    seen_srcs = set()

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if not src:
            continue

        # Skip layout/structure images
        if _is_layout_image(src):
            continue

        # Skip external URLs (tracking pixels, etc.)
        if src.startswith("http"):
            continue

        # Normalize the path
        src = src.replace("%20", " ")

        # Build a relative path from archive root
        img_path = src

        # Remove potential leading directory components if they match
        # common patterns (e.g., "images/" or "vol 7 No 364 images/")
        if not img_path.startswith("images/") and not img_path.startswith("vol"):
            # Check if it's already an absolute-like path starting with the
            # volume directory name
            if not os.path.exists(os.path.join(os.path.dirname(source_file), img_path)):
                continue

        alt = img.get("alt", "") or img.get("title", "") or ""

        # Deduplicate by source path
        if img_path not in seen_srcs:
            seen_srcs.add(img_path)
            images.append(
                {
                    "image_path": img_path,
                    "alt_text": alt.strip(),
                }
            )

    return images