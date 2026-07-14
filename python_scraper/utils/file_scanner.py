"""
Scans the archive directory for HTML files, filtering out
navigation pages, templates, and non-HTML files.
"""
import os
import re
from pathlib import Path

from config import (
    HTML_ARCHIVE_DIR,
    SKIP_FILES,
    SKIP_DIRECTORIES,
    TEMPLATE_PATTERNS,
    NAVIGATION_FILES,
)


def is_template_file(filename: str) -> bool:
    """Check if a filename matches known template patterns."""
    for pattern in TEMPLATE_PATTERNS:
        if pattern in filename:
            return True
    return False


def is_article_html(filepath: str) -> bool:
    """
    Determine whether a given file is an article HTML worth parsing.
    Filters out navigation pages, templates, and non-HTML files.
    """
    path = Path(filepath)
    filename = path.name

    # Skip non-HTML files
    if path.suffix.lower() not in (".htm", ".html"):
        return False

    # Skip known non-article files
    if filename in SKIP_FILES or filename in NAVIGATION_FILES:
        return False

    # Skip template files
    if is_template_file(filename):
        return False

    return True


def scan_archive(directory: str = None) -> list[str]:
    """
    Recursively scan the archive directory and return a sorted list
    of HTML file paths that are likely articles.
    """
    if directory is None:
        directory = HTML_ARCHIVE_DIR

    article_files = []

    for root, dirs, files in os.walk(directory):
        # Skip image directories
        dir_name = os.path.basename(root)
        if dir_name in SKIP_DIRECTORIES:
            continue

        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            if is_article_html(filepath):
                article_files.append(filepath)

    return article_files


def get_relative_path(filepath: str) -> str:
    """Get the path relative to the archive directory."""
    return os.path.relpath(filepath, HTML_ARCHIVE_DIR)