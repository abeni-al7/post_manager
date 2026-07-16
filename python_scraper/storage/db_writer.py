"""
Database writer for Addis Fortune HTML parser.
Handles saving articles and images to MySQL database.
"""
import mysql.connector
from typing import Optional

from .db_connection import get_connection
from utils import compute_content_hash


def save_article(
    source_file: str,
    title: str | None,
    subtitle: str | None,
    author: str | None,
    content: str | None,
    category: str,
    volume: str | None,
    issue: str | None,
    published_date: str | None,
    image_paths: list[dict],
) -> int | None:
    """
    Save an article to the database.
    
    Returns the post ID if successful, None otherwise.
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Compute content hash and word count
        content_hash = compute_content_hash(content) if content else ""
        word_count = len(content.split()) if content else 0
        
        # Insert the post
        query = """
            INSERT INTO posts (
                source_file, title, subtitle, author, content,
                category, volume, issue_number, published_date,
                content_hash, word_count
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                source_file,
                title,
                subtitle,
                author,
                content,
                category,
                volume,
                issue,
                published_date,
                content_hash,
                word_count,
            ),
        )
        post_id = cursor.lastrowid
        
        # Insert image references
        if image_paths:
            image_query = "INSERT INTO post_images (post_id, image_path, alt_text, sort_order) VALUES (%s, %s, %s, %s)"
            for idx, img in enumerate(image_paths):
                cursor.execute(
                    image_query,
                    (post_id, img.get("image_path", ""), img.get("alt_text", ""), idx)
                )
        
        conn.commit()
        return post_id
        
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return None
    finally:
        if conn:
            conn.close()


def article_exists(source_file: str) -> bool:
    """Check if an article with the given source file has already been processed."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE source_file = %s", (source_file,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as e:
        print(f"Database error checking existence: {e}")
        return False
    finally:
        if conn:
            conn.close()
