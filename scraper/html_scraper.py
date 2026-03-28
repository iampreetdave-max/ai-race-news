"""
AI Pulse HTML Scraper - BeautifulSoup based
"""
import logging
import re
import time
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .models import Article, ScrapeResult
from .config import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    USER_AGENT,
    MAX_ARTICLES_PER_SOURCE,
)

logger = logging.getLogger(__name__)


class HTMLScraper:
    """Scrapes articles from HTML pages without RSS feeds."""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": (
                    "text/html,application/xhtml+xml,"
                    "application/xml;q=0.9,*/*;q=0.8"
                ),
                "Accept-Language": "en-US,en;q=0.5",
            }
        )

    def scrape_source(
        self, source: dict
    ) -> tuple[list[Article], ScrapeResult]:
        source_name = source["name"]
        source_url = source["url"]
        selectors = source.get("selectors", {})
        priority = source.get("priority", 5)
        start_time = time.time()
        articles: list[Article] = []

        logger.info(f"Scraping HTML source: {source_name}")

        try:
            html = self._fetch_page(source_url)
            if not html:
                return [], ScrapeResult(
                    source_name=source_name,
                    source_url=source_url,
                    status="error",
                    error_message="Failed to fetch page",
                    duration_seconds=time.time() - start_time,
                )

            soup = BeautifulSoup(html, "html.parser")
            article_selector = selectors.get("article_container", "article")
            containers = soup.select(article_selector)[
                :MAX_ARTICLES_PER_SOURCE
            ]

            for container in containers:
                article = self._parse_article(
                    container, source_name, source_url, selectors, priority
                )
                if article:
                    articles.append(article)

            logger.info(
                f"Scraped {len(articles)} articles from {source_name}"
            )

            return articles, ScrapeResult(
                source_name=source_name,
                source_url=source_url,
                status="success",
                articles_found=len(articles),
                duration_seconds=time.time() - start_time,
            )

        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return [], ScrapeResult(
                source_name=source_name,
                source_url=source_url,
                status="error",
                error_message=str(e),
                duration_seconds=time.time() - start_time,
            )

    def _fetch_page(self, url: str) -> Optional[str]:
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                logger.warning(
                    f"Fetch attempt {attempt + 1} failed for {url}: {e}"
                )
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
        return None

    def _parse_article(
        self,
        container,
        source_name: str,
        base_url: str,
        selectors: dict,
        priority: int,
    ) -> Optional[Article]:
        try:
            title = self._extract_text(
                container, selectors.get("title", "h2, h3")
            )
            if not title:
                return None

            link_elem = container.select_one(selectors.get("link", "a"))
            if not link_elem:
                return None
            url = link_elem.get("href")
            if not url:
                return None
            url = urljoin(base_url, url)

            summary = self._extract_text(
                container, selectors.get("summary", "p, .description")
            )
            author = self._extract_text(
                container, selectors.get("author", ".author, .byline")
            )
            date_str = self._extract_text(
                container, selectors.get("date", "time, .date")
            )
            image_url = self._extract_image(
                container, selectors.get("image", "img"), base_url
            )

            published_at = self._parse_date(date_str) if date_str else None

            return Article(
                title=title.strip(),
                url=url,
                summary=summary.strip() if summary else None,
                author=author.strip() if author else None,
                image_url=image_url,
                source_name=source_name,
                published_at=published_at,
                priority=priority,
            )
        except Exception as e:
            logger.debug(f"Error parsing article: {e}")
            return None

    def _extract_text(
        self, container, selector: str
    ) -> Optional[str]:
        elem = container.select_one(selector)
        if elem:
            return elem.get_text(strip=True)
        return None

    def _extract_image(
        self, container, selector: str, base_url: str
    ) -> Optional[str]:
        img = container.select_one(selector)
        if img:
            for attr in ["src", "data-src", "data-lazy-src"]:
                url = img.get(attr)
                if url:
                    return urljoin(base_url, url)
        return None

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        if not date_str:
            return None

        try:
            from dateutil import parser as dateparser

            return dateparser.parse(date_str)
        except Exception:
            pass

        formats = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%B %d, %Y",
            "%b %d, %Y",
            "%m/%d/%Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue

        date_str_lower = date_str.lower()
        now = datetime.utcnow()

        if "today" in date_str_lower:
            return now.replace(hour=0, minute=0, second=0, microsecond=0)

        match = re.search(
            r"(\d+)\s*(hour|day|week|month)s?\s*ago", date_str_lower
        )
        if match:
            num = int(match.group(1))
            unit = match.group(2)
            if unit == "hour":
                return now - timedelta(hours=num)
            elif unit == "day":
                return now - timedelta(days=num)
            elif unit == "week":
                return now - timedelta(weeks=num)
            elif unit == "month":
                return now - timedelta(days=num * 30)

        return None
