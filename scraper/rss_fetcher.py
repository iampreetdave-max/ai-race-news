"""
AI Pulse RSS Fetcher - Parse RSS/Atom feeds
"""
import logging
import re
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
        published_at = self._extract_date(entry)

        # Extract image (multiple strategies)
        image_url = self._extract_image(entry)

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

    def _extract_date(self, entry) -> Optional[datetime]:
        """Try multiple date fields."""
        for attr in ["published_parsed", "updated_parsed", "created_parsed"]:
            parsed = getattr(entry, attr, None)
            if parsed:
                try:
                    return datetime.fromtimestamp(mktime(parsed))
                except (TypeError, ValueError, OverflowError):
                    continue
        return None

    def _extract_image(self, entry) -> Optional[str]:
        """Extract image URL using multiple strategies."""

        # Strategy 1: media:thumbnail
        if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
            url = entry.media_thumbnail[0].get("url")
            if url:
                return url

        # Strategy 2: media:content with image type
        if hasattr(entry, "media_content") and entry.media_content:
            for media in entry.media_content:
                media_type = media.get("type", "")
                url = media.get("url", "")
                if "image" in media_type or url.endswith(
                    (".jpg", ".jpeg", ".png", ".webp", ".gif")
                ):
                    return url

        # Strategy 3: enclosures with image type
        if hasattr(entry, "enclosures") and entry.enclosures:
            for enc in entry.enclosures:
                enc_type = enc.get("type", "")
                href = enc.get("href", "")
                if "image" in enc_type or href.endswith(
                    (".jpg", ".jpeg", ".png", ".webp", ".gif")
                ):
                    return href

        # Strategy 4: <img> tag in summary/description/content HTML
        html_sources = []
        if hasattr(entry, "summary"):
            html_sources.append(entry.summary)
        if hasattr(entry, "description"):
            html_sources.append(entry.description)
        if hasattr(entry, "content") and entry.content:
            for c in entry.content:
                html_sources.append(c.get("value", ""))

        for html in html_sources:
            if not html:
                continue
            match = re.search(
                r'<img[^>]+src=["\']([^"\'> ]+)', html
            )
            if match:
                img_url = match.group(1)
                # Skip tiny tracking pixels and icons
                if not any(
                    skip in img_url.lower()
                    for skip in [
                        "pixel", "tracking", "1x1", "badge",
                        "icon", "logo", "avatar", "gravatar",
                        "feeds.feedburner",
                    ]
                ):
                    return img_url

        return None

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags and decode entities."""
        import html as html_module

        if not text:
            return ""
        clean = re.sub(r"<[^>]+>", "", text)
        clean = html_module.unescape(clean)
        clean = " ".join(clean.split())
        return clean[:1000]
