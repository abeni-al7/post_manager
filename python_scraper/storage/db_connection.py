"""
Database connection management for Addis Fortune HTML parser.
Handles MySQL connection pooling.
"""
import mysql.connector
from mysql.connector import pooling
from typing import Optional

from config import DB_CONFIG


# Create a connection pool
_connection_pool: Optional[pooling.MySQLConnectionPool] = None


def get_connection_pool():
    """Get or create the MySQL connection pool."""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = pooling.MySQLConnectionPool(
            pool_name="scraper_pool",
            pool_size=5,
            **DB_CONFIG
        )
    return _connection_pool


def get_connection():
    """Get a connection from the pool."""
    return get_connection_pool().get_connection()