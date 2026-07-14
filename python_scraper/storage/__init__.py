"""
Storage package for Addis Fortune HTML parser.
"""
from .db_connection import get_connection, get_connection_pool
from .db_writer import save_article, article_exists, init_database

__all__ = [
    "get_connection",
    "get_connection_pool",
    "save_article",
    "article_exists",
    "init_database",
]
