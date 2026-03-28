"""
AI Pulse Tagger - Keyword-based article tagging
"""
import logging
import re
from typing import Optional

from .models import Article
from .config import TAG_KEYWORDS, AUDIENCE_TAG_MAPPING, AUDIENCE_KEYWORDS

logger = logging.getLogger(__name__)


class Tagger:
    """Tags articles based on content keywords."""

    def __init__(
        self,
        tag_keywords: Optional[dict[str, list[str]]] = None,
        audience_tag_mapping: Optional[dict[str, list[str]]] = None,
        audience_keywords: Optional[dict[str, list[str]]] = None,
    ):
        self.tag_keywords = tag_keywords or TAG_KEYWORDS
        self.audience_tag_mapping = audience_tag_mapping or AUDIENCE_TAG_MAPPING
        self.audience_keywords = audience_keywords or AUDIENCE_KEYWORDS
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        self.tag_patterns: dict[str, list[re.Pattern]] = {}
        for tag, keywords in self.tag_keywords.items():
            patterns = []
            for keyword in keywords:
                escaped = re.escape(keyword)
                pattern = re.compile(rf"\b{escaped}", re.IGNORECASE)
                patterns.append(pattern)
            self.tag_patterns[tag] = patterns

    def tag_article(self, article: Article) -> Article:
        text = self._get_searchable_text(article)
        tags = self._find_tags(text)
        article.tags = list(tags)
        audiences = self._determine_audiences(tags, text)
        article.audiences = list(audiences)

        logger.debug(
            f"Tagged '{article.title[:40]}': tags={article.tags}, "
            f"audiences={article.audiences}"
        )
        return article

    def tag_articles(self, articles: list[Article]) -> list[Article]:
        tagged = [self.tag_article(article) for article in articles]

        tag_counts: dict[str, int] = {}
        for article in tagged:
            for tag in article.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:5]
        logger.info(f"Tagged {len(articles)} articles. Top tags: {top_tags}")
        return tagged

    def _get_searchable_text(self, article: Article) -> str:
        parts = [article.title]
        if article.summary:
            parts.append(article.summary)
        if article.content:
            parts.append(article.content[:1000])
        if article.source_name:
            parts.append(article.source_name)
        return " ".join(parts)

    def _find_tags(self, text: str) -> set[str]:
        tags: set[str] = set()
        for tag, patterns in self.tag_patterns.items():
            for pattern in patterns:
                if pattern.search(text):
                    tags.add(tag)
                    break
        return tags

    def _determine_audiences(self, tags: set[str], text: str) -> set[str]:
        audiences: set[str] = set()

        # Check if article tags match audience tag mappings
        for audience, audience_tags in self.audience_tag_mapping.items():
            if tags & set(audience_tags):
                audiences.add(audience)

        # Check text for audience-specific keywords
        text_lower = text.lower()
        for audience, keywords in self.audience_keywords.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    audiences.add(audience)
                    break

        # Default to general if no specific audience matched
        if not audiences:
            audiences.add("general")

        return audiences


def tag_articles(articles: list[Article]) -> list[Article]:
    tagger = Tagger()
    return tagger.tag_articles(articles)


def get_tag_statistics(articles: list[Article]) -> dict:
    tag_counts: dict[str, int] = {}
    audience_counts: dict[str, int] = {}

    for article in articles:
        for tag in article.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        for audience in article.audiences:
            audience_counts[audience] = audience_counts.get(audience, 0) + 1

    return {
        "total_articles": len(articles),
        "tag_counts": dict(sorted(tag_counts.items(), key=lambda x: -x[1])),
        "audience_counts": dict(
            sorted(audience_counts.items(), key=lambda x: -x[1])
        ),
        "articles_without_tags": sum(1 for a in articles if not a.tags),
        "avg_tags_per_article": (
            sum(len(a.tags) for a in articles) / len(articles)
            if articles
            else 0
        ),
    }
