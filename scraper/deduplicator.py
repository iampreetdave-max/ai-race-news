"""
AI Pulse Deduplicator - URL + content hash + title similarity
"""
import logging
import re
from typing import Optional
from difflib import SequenceMatcher
from urllib.parse import urlparse, parse_qs, urlencode

from .models import Article
from .config import DEDUP_SIMILARITY_THRESHOLD

logger = logging.getLogger(__name__)


class Deduplicator:
    """Deduplicates articles across sources."""

    def __init__(
        self,
        existing_hashes: Optional[set[str]] = None,
        existing_urls: Optional[set[str]] = None,
    ):
        self.seen_hashes: set[str] = existing_hashes or set()
        self.seen_urls: set[str] = existing_urls or set()
        self.seen_titles: dict[str, Article] = {}

    def is_duplicate(self, article: Article) -> bool:
        # Strategy 1: Exact URL match
        normalized_url = self._normalize_url(article.url)
        if normalized_url in self.seen_urls:
            logger.debug(f"Duplicate URL: {article.title[:50]}")
            return True

        # Strategy 2: Content hash match
        if article.content_hash and article.content_hash in self.seen_hashes:
            logger.debug(f"Duplicate content hash: {article.title[:50]}")
            return True

        # Strategy 3: Title similarity
        normalized_title = self._normalize_title(article.title)
        for seen_title, seen_article in self.seen_titles.items():
            similarity = self._calculate_similarity(normalized_title, seen_title)
            if similarity >= DEDUP_SIMILARITY_THRESHOLD:
                logger.debug(
                    f"Similar title ({similarity:.2f}): "
                    f"'{article.title[:30]}' ~ '{seen_article.title[:30]}'"
                )
                return True

        return False

    def mark_seen(self, article: Article) -> None:
        self.seen_urls.add(self._normalize_url(article.url))
        if article.content_hash:
            self.seen_hashes.add(article.content_hash)
        self.seen_titles[self._normalize_title(article.title)] = article

    def deduplicate(
        self, articles: list[Article]
    ) -> tuple[list[Article], int]:
        unique = []
        duplicates = 0

        for article in articles:
            if self.is_duplicate(article):
                duplicates += 1
            else:
                unique.append(article)
                self.mark_seen(article)

        logger.info(
            f"Deduplicated: {len(articles)} -> {len(unique)} "
            f"({duplicates} duplicates removed)"
        )
        return unique, duplicates

    def _normalize_url(self, url: str) -> str:
        parsed = urlparse(url.lower().strip())
        tracking_params = {
            "utm_source", "utm_medium", "utm_campaign", "utm_term",
            "utm_content", "ref", "source", "campaign", "fbclid",
            "gclid", "mc_eid", "mc_cid",
        }
        query_params = parse_qs(parsed.query)
        filtered_params = {
            k: v for k, v in query_params.items() if k not in tracking_params
        }
        clean_query = urlencode(filtered_params, doseq=True)
        clean_path = parsed.path.rstrip("/")

        normalized = f"{parsed.netloc}{clean_path}"
        if clean_query:
            normalized += f"?{clean_query}"
        return normalized

    def _normalize_title(self, title: str) -> str:
        normalized = title.lower().strip()

        # Remove common prefixes
        prefixes = [
            r"^\[.*?\]\s*", r"^breaking:\s*",
            r"^update:\s*", r"^exclusive:\s*",
        ]
        for pattern in prefixes:
            normalized = re.sub(pattern, "", normalized, flags=re.IGNORECASE)

        # Remove common suffixes
        suffixes = [
            r"\s*\|\s*.*$", r"\s*-\s*[A-Za-z]+\s*$", r"\s*\(.*?\)\s*$",
        ]
        for pattern in suffixes:
            normalized = re.sub(pattern, "", normalized)

        normalized = re.sub(r"[^\w\s]", "", normalized)
        normalized = " ".join(normalized.split())
        return normalized

    def _calculate_similarity(self, str1: str, str2: str) -> float:
        if not str1 or not str2:
            return 0.0
        return SequenceMatcher(None, str1, str2).ratio()


def deduplicate_articles(
    articles: list[Article],
    existing_hashes: Optional[set[str]] = None,
    existing_urls: Optional[set[str]] = None,
) -> tuple[list[Article], int]:
    deduplicator = Deduplicator(existing_hashes, existing_urls)
    return deduplicator.deduplicate(articles)
