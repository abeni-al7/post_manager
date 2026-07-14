"""
HTML parser for Addis Fortune articles.
Coordinates extraction of all article fields from HTML files.
"""
import logging
from typing import Optional
from bs4 import BeautifulSoup

from extractors import (
    extract_title,
    extract_author,
    extract_content,
    extract_images,
    extract_subtitle,
    extract_volume_and_issue,
    extract_published_date,
)
from classifiers import classify_category
from utils import get_relative_path

logger = logging.getLogger(__name__)


def parse_html_file(filepath: str) -> Optional[dict]:
    """
    Parse a single HTML file and extract all article data.
    
    Args:
        filepath: Path to the HTML file to parse
        
    Returns:
        Dictionary with extracted fields, or None if parsing fails
    """
    try:
        # Read the HTML file with Windows-1252 encoding (common for older HTML)
        with open(filepath, "r", encoding="windows-1252", errors="replace") as f:
            content = f.read()
    except Exception as e:
        logger.error(f"Failed to read file {filepath}: {e}")
        return None
    
    try:
        soup = BeautifulSoup(content, "html.parser")
    except Exception as e:
        logger.error(f"Failed to parse HTML in {filepath}: {e}")
        return None
    
    # Extract all fields using dedicated extractors
    try:
        title = extract_title(soup)
    except Exception as e:
        logger.warning(f"Failed to extract title from {filepath}: {e}")
        title = None
    
    try:
        author = extract_author(soup)
    except Exception as e:
        logger.warning(f"Failed to extract author from {filepath}: {e}")
        author = None
    
    try:
        article_content = extract_content(soup)
    except Exception as e:
        logger.warning(f"Failed to extract content from {filepath}: {e}")
        article_content = None
    
    try:
        subtitle = extract_subtitle(soup)
    except Exception as e:
        logger.warning(f"Failed to extract subtitle from {filepath}: {e}")
        subtitle = None
    
    try:
        volume, issue = extract_volume_and_issue(soup)
    except Exception as e:
        logger.warning(f"Failed to extract volume/issue from {filepath}: {e}")
        volume, issue = None, None
    
    try:
        published_date = extract_published_date(soup)
    except Exception as e:
        logger.warning(f"Failed to extract published date from {filepath}: {e}")
        published_date = None
    
    try:
        images = extract_images(soup, filepath)
    except Exception as e:
        logger.warning(f"Failed to extract images from {filepath}: {e}")
        images = []
    
    # Classify category based on filepath, title, and content
    try:
        category = classify_category(filepath, title, article_content)
    except Exception as e:
        logger.warning(f"Failed to classify category for {filepath}: {e}")
        category = "News"  # Default category
    
    # Build the result dictionary
    result = {
        "source_file": get_relative_path(filepath),
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "content": article_content,
        "category": category,
        "volume": volume,
        "issue_number": issue,
        "published_date": published_date,
        "images": images,
    }
    
    return result