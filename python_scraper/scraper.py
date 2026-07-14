#!/usr/bin/env python3
"""
Main entry point for the Addis Fortune HTML scraper.
Parses HTML files from the archive and stores extracted data in MySQL.
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import HTML_ARCHIVE_DIR
from parser import parse_html_file
from storage import save_article, article_exists, init_database
from utils import scan_archive, get_relative_path


def run_scraper(
    dry_run: bool = False,
    limit: int | None = None,
    output_file: str | None = None,
    incremental: bool = False,
):
    """
    Run the scraper on all HTML files in the archive.
    
    Args:
        dry_run: If True, only print what would be done without saving to DB
        limit: Optional limit on number of files to process
        output_file: Optional path to save results as JSON instead of DB
        incremental: If True, skip previously imported files (default behavior)
    """
    print(f"Scanning archive directory: {HTML_ARCHIVE_DIR}")
    
    # Initialize database tables (only if not dry_run and not output_file)
    if not dry_run and not output_file:
        init_database()
    
    # Get all article files
    article_files = scan_archive()
    print(f"Found {len(article_files)} potential article files")
    
    processed = 0
    saved = 0
    skipped = 0
    
    for filepath in article_files:
        if limit and processed >= limit:
            break
        
        relative_path = get_relative_path(filepath)
        
        # Check if already processed
        if article_exists(relative_path):
            skipped += 1
            continue
        
        try:
            article_data = parse_html_file(filepath)
            
            # Skip if incremental and already exists
            if incremental and not dry_run and not output_file:
                if article_exists(relative_path):
                    skipped += 1
                    continue
            
            if dry_run:
                print(f"\n[DRY RUN] Would process: {relative_path}")
                print(f"  Title: {article_data['title']}")
                print(f"  Author: {article_data['author']}")
                print(f"  Category: {article_data['category']}")
                print(f"  Images: {len(article_data['images'])}")
            elif output_file:
                # Save to JSON file
                import json
                with open(output_file, "a", encoding="utf-8") as f:
                    f.write(json.dumps(article_data, ensure_ascii=False) + "\n")
                saved += 1
                print(f"Saved to JSON: {article_data['title']}")
            else:
                article_id = save_article(
                    source_file=article_data["source_file"],
                    title=article_data["title"],
                    subtitle=article_data["subtitle"],
                    author=article_data["author"],
                    content=article_data["content"],
                    category=article_data["category"],
                    volume=article_data["volume"],
                    issue=article_data["issue"],
                    published_date=article_data["published_date"],
                    image_paths=article_data["images"],
                )
                
                if article_id:
                    saved += 1
                    print(f"Saved article {article_id}: {article_data['title']}")
                else:
                    print(f"Failed to save: {relative_path}")
            
            processed += 1
            
        except Exception as e:
            print(f"Error processing {relative_path}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Scraping complete!")
    print(f"  Processed: {processed}")
    print(f"  Saved: {saved}")
    print(f"  Skipped (already in DB): {skipped}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Addis Fortune HTML Scraper")
    parser.add_argument(
        "--input-dir",
        type=str,
        default=None,
        help="Input directory containing HTML archive (default: config.HTML_ARCHIVE_DIR)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse files without saving to database",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of files to process",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Save results to JSON file instead of database",
    )
    parser.add_argument(
        "--incremental",
        action="store_true",
        default=True,
        help="Skip previously imported files (default: True)",
    )
    
    args = parser.parse_args()
    
    # Override HTML_ARCHIVE_DIR if provided
    if args.input_dir:
        import config
        config.HTML_ARCHIVE_DIR = args.input_dir
    
    run_scraper(
        dry_run=args.dry_run,
        limit=args.limit,
        output_file=args.output,
        incremental=args.incremental,
    )
