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


def init_database():
    """Initialize the database tables if they don't exist."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create posts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(500) NOT NULL,
                subtitle TEXT NULL,
                author VARCHAR(255) NULL,
                content LONGTEXT NOT NULL,
                category VARCHAR(100) NULL,
                source_file VARCHAR(500) NOT NULL UNIQUE,
                volume VARCHAR(50) NULL,
                issue_number VARCHAR(50) NULL,
                published_date DATE NULL,
                content_hash VARCHAR(64) NOT NULL,
                word_count INT UNSIGNED DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY uk_content_hash (content_hash)
            )
        """)
        
        # Create post_images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS post_images (
                id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                post_id BIGINT UNSIGNED NOT NULL,
                image_path VARCHAR(500) NOT NULL,
                alt_text VARCHAR(500) NULL,
                sort_order INT DEFAULT 0,
                FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX idx_category ON posts(category)")
        cursor.execute("CREATE INDEX idx_author ON posts(author)")
        cursor.execute("CREATE FULLTEXT INDEX idx_content_search ON posts(title, content)")
        
        conn.commit()
        print("Database tables initialized successfully.")
        
    except mysql.connector.Error as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()