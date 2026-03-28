"""AI Pulse Scraper Module"""
from .models import Article, ScrapeResult
from .database import Database, get_database
from .deduplicator import Deduplicator, deduplicate_articles
from .tagger import Tagger, tag_articles
from .pipeline import AIPulseScraper, run_scraper
from .config import RSS_SOURCES, HTML_SOURCES

__version__ = "0.1.0"

__all__ = [
    "Article", "ScrapeResult", "Database", "get_database",
    "Deduplicator", "deduplicate_articles", "Tagger", "tag_articles",
    "AIPulseScraper", "run_scraper", "RSS_SOURCES", "HTML_SOURCES",
]
