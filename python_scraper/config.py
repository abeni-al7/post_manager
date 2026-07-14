"""
Configuration for the Addis Fortune HTML parser.
All configurable paths and database settings are centralized here.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Directory containing the HTML archive files
HTML_ARCHIVE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Vol 7 No 364  Archive"
)

# MySQL Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DATABASE", "post_manager"),
}

# Files and directories to skip during scanning
SKIP_FILES = {
    "Thumbs.db",
    "Desktop__.ini",
    ".DS_Store",
}

SKIP_DIRECTORIES = {"images", "vol 7 No 364 images"}

# Template files (not actual articles) — identified by their filename patterns
TEMPLATE_PATTERNS = [
    "FORTUNE NEWS PAGE TEMPLATE",
    "TEMPLATE",
    "template",
]

# Navigation / utility pages to skip (not articles)
NAVIGATION_FILES = {
    "Index.htm",
    "index.htm",
    "Homepage.htm",
    "archive.htm",
    "classifieds.htm",
    "classifieds_Car For Rent.htm",
    "classifieds_Car For Sale.htm",
    "classifieds_House For Rent.htm",
    "classifieds_House For Sale.htm",
    "aboutus.htm",
    "advertise.htm",
    "contactus.htm",
    "contribute.htm",
    "guestbook.htm",
    "businessopportunities.htm",
    "newsinbrief.htm",
    "cartoon.htm",
    "Allcartoons.htm",
    "comic stripes.htm",
    "Clock.htm",
    "Published On.htm",
    "volume_Number.htm",
    "fortune_crawling_news.htm",
    "News_364.htm",
    "News_365.htm",
    "News_366.htm",
    "Newsinbriefindex.htm",
    "restaurantsreview.htm",
    "Addis Fortune news.htm",
    "Business Oppoerunities_index.htm",
    "Business Opportunities_Executive Calendar.htm",
    "Business Opportunities_Exporter.htm",
    "Business Opportunities_Importer.htm",
    "Business Opportunities_Partnership.htm",
    "tender_mart.htm",
    "Gossip.htm",
    "Expert Corner.htm",
    "agenda.htm",
    "fortuneeditorsnote.htm",
    "opinion.htm",
    "Commentary.htm",
    "viewpoint.htm",
    "myperspective.htm",
    "lifematters.htm",
    "viewfromarada.htm",
}
