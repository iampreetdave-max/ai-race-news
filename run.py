#!/usr/bin/env python3
"""
AI Pulse Scraper Runner
Usage:
    python run.py                 # Run scraper once
    python run.py --schedule      # Run on schedule (every 15 min)
    python run.py --stats         # Show database stats
    python run.py --cleanup 30    # Remove articles older than 30 days
    python run.py --api           # Start the API server
"""
import sys
import os
import argparse
import logging

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scraper.pipeline import run_scraper
from scraper.database import get_database
from scraper.config import SCRAPE_INTERVAL_MINUTES


def main():
    parser = argparse.ArgumentParser(description="AI Pulse News Scraper")
    parser.add_argument(
        "--schedule", action="store_true", help="Run on schedule"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=SCRAPE_INTERVAL_MINUTES,
        help="Interval in minutes (default: 15)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Show database stats"
    )
    parser.add_argument(
        "--cleanup",
        type=int,
        metavar="DAYS",
        help="Remove old articles",
    )
    parser.add_argument(
        "--api", action="store_true", help="Start API server"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="API port (default: 8000)"
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.stats:
        db = get_database()
        stats = db.get_scrape_stats()
        print("\n=== AI Pulse Database Statistics ===")
        print(f"Total articles: {stats['total_articles']:,}")
        print(f"Total scrapes: {stats['total_scrapes']:,}")
        print(f"Success rate: {stats['success_rate']:.1%}")
        print("\nArticles by source:")
        for source, count in list(
            stats["articles_by_source"].items()
        )[:15]:
            print(f"  {source}: {count:,}")
        return

    if args.cleanup:
        db = get_database()
        deleted = db.cleanup_old_articles(args.cleanup)
        print(
            f"Cleaned up {deleted} articles older than {args.cleanup} days"
        )
        return

    if args.api:
        try:
            import uvicorn
        except ImportError:
            print("uvicorn not installed. Run: pip install uvicorn[standard]")
            sys.exit(1)

        print(f"Starting AI Pulse API on port {args.port}...")
        print(f"Docs: http://localhost:{args.port}/docs")
        uvicorn.run(
            "api.main:app",
            host="0.0.0.0",
            port=args.port,
            reload=True,
        )
        return

    if args.schedule:
        try:
            from apscheduler.schedulers.blocking import BlockingScheduler
        except ImportError:
            print("APScheduler not installed. Run: pip install APScheduler")
            sys.exit(1)

        scheduler = BlockingScheduler()
        print(
            f"Starting AI Pulse Scraper "
            f"(every {args.interval} minutes)"
        )

        # Run once immediately
        run_scraper()

        scheduler.add_job(
            run_scraper, "interval", minutes=args.interval
        )

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("\nScheduler stopped")
    else:
        print("Running AI Pulse Scraper...\n")
        stats = run_scraper()
        print(f"\nComplete! {stats['articles_inserted']} new articles added")
        print(f"Duration: {stats['duration_seconds']:.1f}s")
        print(
            f"Sources: {stats['sources_successful']}/"
            f"{stats['sources_processed']} successful"
        )


if __name__ == "__main__":
    main()
