"""
Deduplication utilities for the Addis Fortune HTML parser.
"""
import hashlib
from typing import Optional


def compute_content_hash(content: str) -> str:
    """
    Compute a hash of the content for deduplication purposes.
    Uses SHA-256 for better collision resistance.
    """
    if not content:
        return ""
    return hashlib.sha256(content.encode("utf-8", errors="replace")).hexdigest()


def is_duplicate_title(title: str, existing_titles: set[str]) -> bool:
    """
    Check if a title is a duplicate of an existing title.
    Uses normalized comparison (case-insensitive, whitespace-normalized).
    """
    if not title:
        return False
    normalized = " ".join(title.lower().split())
    return normalized in existing_titles


def normalize_title(title: str) -> str:
    """
    Normalize a title for comparison.
    """
    if not title:
        return ""
    return " ".join(title.lower().split())