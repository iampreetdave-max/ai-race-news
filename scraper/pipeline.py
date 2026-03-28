"""
AI Pulse Scraper - Main Pipeline Orchestrator
"""
import logging
import time
from datetime import datetime
from typing import Optional

from .config import (
    RSS_SOURCES,
    HTML_SOURCES,
    LOG_LEVEL,
    LOG_FORMAT,
    SCRAPE_INTERVAL_MINUTES,
)
from .models import Article, ScrapeResult
from .rss_fetcher import RSSFetcher
from .html_scraper import HTMLScraper
from .deduplicator import Deduplicator
from .tagger import Tagger, get_tag_statistics
from .database import Database, get_database

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class AIPulseScraper:
    """Main scraper orchestrator."""

    def __init__(self, db: Optional[Database] = None):
        self.db = db or get_database()
        self.rss_fetcher = RSSFetcher()
        self.html_scraper = HTMLScraper()
        self.tagger = Tagger()
        logger.info("AI Pulse Scraper initialized")

    def run(self) -> dict:
        start_time = time.time()
        logger.info("=" * 60)
        logger.info("Starting AI Pulse scrape run")
        logger.info("=" * 60)

        # Load existing data for deduplication
        existing_hashes = self.db.get_existing_hashes()
        existing_urls = self.db.get_existing_urls()
        logger.info(
            f"Loaded {len(existing_hashes)} existing hashes, "
            f"{len(existing_urls)} URLs"
        )

        deduplicator = Deduplicator(existing_hashes, existing_urls)

        all_articles: list[Article] = []
        all_results: list[ScrapeResult] = []

        # Phase 1: Fetch RSS feeds
        logger.info("-" * 40)
        logger.info("Phase 1: Fetching RSS feeds")
        logger.info("-" * 40)

        for source in RSS_SOURCES:
            try:
                articles, result = self.rss_fetcher.fetch_source(source)
                all_articles.extend(articles)
                all_results.append(result)
                self.db.log_scrape(result)
                time.sleep(0.5)  # Be polite to servers
            except Exception as e:
                logger.error(f"Error with RSS source {source['name']}: {e}")
                result = ScrapeResult(
                    source_name=source["name"],
                    source_url=source["url"],
                    status="error",
                    error_message=str(e),
                )
                all_results.append(result)
                self.db.log_scrape(result)

        # Phase 2: Scrape HTML sources
        logger.info("-" * 40)
        logger.info("Phase 2: Scraping HTML sources")
        logger.info("-" * 40)

        for source in HTML_SOURCES:
            try:
                articles, result = self.html_scraper.scrape_source(source)
                all_articles.extend(articles)
                all_results.append(result)
                self.db.log_scrape(result)
                time.sleep(1.0)  # Longer delay for HTML scraping
            except Exception as e:
                logger.error(f"Error with HTML source {source['name']}: {e}")
                result = ScrapeResult(
                    source_name=source["name"],
                    source_url=source["url"],
                    status="error",
                    error_message=str(e),
                )
                all_results.append(result)
                self.db.log_scrape(result)

        # Phase 3: Deduplicate
        logger.info("-" * 40)
        logger.info("Phase 3: Deduplicating articles")
        logger.info("-" * 40)

        unique_articles, duplicate_count = deduplicator.deduplicate(
            all_articles
        )

        # Phase 4: Tag articles
        logger.info("-" * 40)
        logger.info("Phase 4: Tagging articles")
        logger.info("-" * 40)

        tagged_articles = self.tagger.tag_articles(unique_articles)
        tag_stats = get_tag_statistics(tagged_articles)

        # Phase 5: Store in database
        logger.info("-" * 40)
        logger.info("Phase 5: Storing articles")
        logger.info("-" * 40)

        inserted, db_duplicates = self.db.insert_articles(tagged_articles)

        # Summary
        duration = time.time() - start_time

        stats = {
            "timestamp": datetime.utcnow().isoformat(),
            "duration_seconds": round(duration, 2),
            "sources_processed": len(all_results),
            "sources_successful": sum(
                1 for r in all_results if r.status == "success"
            ),
            "sources_failed": sum(
                1 for r in all_results if r.status == "error"
            ),
            "articles_fetched": len(all_articles),
            "articles_unique": len(unique_articles),
            "articles_duplicate": duplicate_count,
            "articles_inserted": inserted,
            "tag_statistics": tag_stats,
        }

        logger.info("=" * 60)
        logger.info("Scrape run complete!")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info(
            f"Sources: {stats['sources_successful']}/"
            f"{stats['sources_processed']} successful"
        )
        logger.info(
            f"Articles: {inserted} new from {len(all_articles)} fetched"
        )
        logger.info("=" * 60)

        return stats


def run_scraper() -> dict:
    """Convenience function to run the scraper once."""
    scraper = AIPulseScraper()
    return scraper.run()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Pulse News Scraper")
    parser.add_argument(
        "--once", action="store_true", help="Run once and exit"
    )
    parser.add_argument(
        "--interval", type=int, default=SCRAPE_INTERVAL_MINUTES
    )
    args = parser.parse_args()

    if args.once:
        stats = run_scraper()
        print(f"\nScrape complete: {stats['articles_inserted']} new articles")
    else:
        from apscheduler.schedulers.blocking import BlockingScheduler

        scheduler = BlockingScheduler()
        run_scraper()
        scheduler.add_job(
            run_scraper, "interval", minutes=args.interval
        )
        logger.info(
            f"Scheduler started. Running every {args.interval} minutes."
        )

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped.")
