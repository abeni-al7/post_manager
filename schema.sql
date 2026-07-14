-- Addis Fortune HTML Scraper Database Schema

-- Posts table
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
);

-- Post images table
CREATE TABLE IF NOT EXISTS post_images (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    post_id BIGINT UNSIGNED NOT NULL,
    image_path VARCHAR(500) NOT NULL,
    alt_text VARCHAR(500) NULL,
    sort_order INT DEFAULT 0,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_category ON posts(category);
CREATE INDEX idx_author ON posts(author);
CREATE FULLTEXT INDEX idx_content_search ON posts(title, content);
