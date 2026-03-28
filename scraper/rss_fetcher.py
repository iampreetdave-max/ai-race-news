"""
AI Pulse RSS Fetcher - Parse RSS/Atom feeds
"""
import logging
import time
from datetime import datetime
from time import mktime
from typing import Optional

import feedparser

from .models import Article, ScrapeResult
from .config import REQUEST_TIMEOUT, USER_AGENT, MAX_ARTICLES_PER_SOURCE

logger = logging.getLogger(__name__)


class RSSFetcher:
    """Fetches and parses RSS/Atom feeds."""

    def __init__(self):
        # feedparser respects this agent string
        feedparser.USER_AGENT = USER_AGENT

    def fetch_source(
        self, source: dict
    ) -> tuple[list[Article], ScrapeResult]:
        source_name = source["name"]
        source_url = source["url"]
        priority = source.get("priority", 5)
        start_time = time.time()
        articles: list[Article] = []

        logger.info(f"Fetching RSS: {source_name}")

        try:
            feed = feedparser.parse(source_url)

            if feed.bozo and feed.bozo_exception:
                logger.warning(
                    f"Feed parse warning for {source_name}: "
                    f"{feed.bozo_exception}"
                )

            for entry in feed.entries[:MAX_ARTICLES_PER_SOURCE]:
                try:
                    article = self._parse_entry(
                        entry, source_name, priority
                    )
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.debug(f"Error parsing entry from {source_name}: {e}")
                    continue

            logger.info(f"  -> {len(articles)} articles from {source_name}")

            return articles, ScrapeResult(
                source_name=source_name,
                source_url=source_url,
                status="success",
                articles_found=len(articles),
                duration_seconds=time.time() - start_time,
            )

        except Exception as e:
            logger.error(f"Error fetching {source_name}: {e}")
            return [], ScrapeResult(
                source_name=source_name,
                source_url=source_url,
                status="error",
                error_message=str(e),
                duration_seconds=time.time() - start_time,
            )

    def _parse_entry(
        self, entry, source_name: str, priority: int
    ) -> Optional[Article]:
        title = getattr(entry, "title", "").strip()
        link = getattr(entry, "link", None)

        if not title or not link:
            return None

        # Extract summary
        summary = None
        for attr in ["summary", "description"]:
            if hasattr(entry, attr):
                summary = self._clean_html(getattr(entry, attr))
                break

        # Extract author
        author = getattr(entry, "author", None)
        if not author and hasattr(entry, "author_detail"):
            author = entry.author_detail.get("name")

        # Extract published date
        published_at = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            try:
                published_at = datetime.fromtimestamp(
                    mktime(entry.published_parsed)
                )
            except (TypeError, ValueError, OverflowError):
                pass
        if not published_at and hasattr(entry, "updated_parsed") and entry.updated_parsed:
            try:
                published_at = datetime.fromtimestamp(
                    mktime(entry.updated_parsed)
                )
            except (TypeError, ValueError, OverflowError):
                pass

        # Extract image
        image_url = None
        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            image_url = entry.media_thumbnail[0].get("url")
        elif hasattr(entry, "media_content") and entry.media_content:
            image_url = entry.media_content[0].get("url")

        return Article(
            title=title,
            url=link,
            summary=summary,
            author=author,
            image_url=image_url,
            source_name=source_name,
            published_at=published_at,
            priority=priority,
        )

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and decode entities."""
        import re
        import html as html_module

        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", "", text)
        clean = html_module.unescape(clean)
        clean = " ".join(clean.split())
        return clean[:1000]
