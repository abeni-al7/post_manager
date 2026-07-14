"""
Utils package for Addis Fortune HTML parser.
"""
from .file_scanner import scan_archive, get_relative_path, is_article_html
from .dedup import compute_content_hash, is_duplicate_title, normalize_title

__all__ = [
    "scan_archive",
    "get_relative_path",
    "is_article_html",
    "compute_content_hash",
    "is_duplicate_title",
    "normalize_title",
]
