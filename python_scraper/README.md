# Addis Fortune HTML Scraper

A Python scraper for parsing Addis Fortune HTML archive files and storing extracted data in MySQL.

## Project Structure

```
python_scraper/
├── config.py           # Configuration (paths, DB settings, skip lists)
├── scraper.py          # Main entry point
├── requirements.txt    # Python dependencies
├── schema.sql          # Database schema
├── extractors/         # HTML extraction modules
│   ├── __init__.py
│   ├── title_extractor.py
│   ├── author_extractor.py
│   ├── content_extractor.py
│   ├── image_extractor.py
│   └── metadata_extractor.py
├── classifiers/        # Category classification
│   └── __init__.py
├── storage/            # Database operations
│   └── __init__.py
└── utils/              # Utility functions
    ├── __init__.py
    ├── file_scanner.py
    └── dedup.py
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the MySQL database (using Docker):
```bash
docker compose up -d
```

3. Run the scraper:
```bash
# Dry run (no database writes)
python3 python_scraper/scraper.py --dry-run

# Full run
python3 python_scraper/scraper.py
```

## Features

- **Title Extraction**: Extracts article titles from styled `<span>` elements or `<title>` tags
- **Author Extraction**: Finds bylines in signature tables or italic "By" patterns
- **Content Extraction**: Extracts article body text, filtering out navigation and ads
- **Image Extraction**: Identifies article images, excluding layout elements
- **Metadata Extraction**: Extracts volume, issue number, and published date
- **Category Classification**: Classifies articles based on keywords and file paths
- **Deduplication**: Tracks processed files to avoid re-processing

## Database Schema

The scraper creates two tables:
- `articles`: Stores article metadata and content
- `article_images`: Stores references to article images

## Configuration

Edit `config.py` to customize:
- `HTML_ARCHIVE_DIR`: Path to HTML archive
- `DB_CONFIG`: MySQL connection settings
- `SKIP_FILES`: Files to ignore during scanning
- `NAVIGATION_FILES`: Navigation pages to skip
- `TEMPLATE_PATTERNS`: Template file patterns to skip