"""
AI Pulse Data Models
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib


@dataclass
class Article:
    """Represents a single news article."""

    title: str
    url: str
    source_name: str

    summary: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[datetime] = None

    id: Optional[str] = None
    content_hash: Optional[str] = None
    scraped_at: datetime = field(default_factory=datetime.utcnow)

    tags: list[str] = field(default_factory=list)
    audiences: list[str] = field(default_factory=list)
    priority: int = 5

    def __post_init__(self):
        if not self.id:
            self.id = self._generate_id()
        if not self.content_hash:
            self.content_hash = self._generate_content_hash()

    def _generate_id(self) -> str:
        return hashlib.md5(self.url.encode()).hexdigest()[:16]

    def _generate_content_hash(self) -> str:
        content = self.title.lower().strip()
        if self.summary:
            content += self.summary[:500].lower().strip()
        elif self.content:
            content += self.content[:500].lower().strip()
        return hashlib.md5(content.encode()).hexdigest()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "summary": self.summary,
            "content": self.content,
            "author": self.author,
            "image_url": self.image_url,
            "source_name": self.source_name,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "scraped_at": self.scraped_at.isoformat(),
            "content_hash": self.content_hash,
            "tags": ",".join(self.tags),
            "audiences": ",".join(self.audiences),
            "priority": self.priority,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Article":
        tags_raw = data.get("tags", "")
        audiences_raw = data.get("audiences", "")
        return cls(
            id=data.get("id"),
            title=data["title"],
            url=data["url"],
            summary=data.get("summary"),
            content=data.get("content"),
            author=data.get("author"),
            image_url=data.get("image_url"),
            source_name=data["source_name"],
            published_at=(
                datetime.fromisoformat(data["published_at"])
                if data.get("published_at")
                else None
            ),
            scraped_at=(
                datetime.fromisoformat(data["scraped_at"])
                if data.get("scraped_at")
                else datetime.utcnow()
            ),
            content_hash=data.get("content_hash"),
            tags=tags_raw.split(",") if tags_raw else [],
            audiences=audiences_raw.split(",") if audiences_raw else [],
            priority=data.get("priority", 5),
        )


@dataclass
class ScrapeResult:
    """Result of a single scrape operation."""

    source_name: str
    source_url: str
    status: str
    articles_found: int = 0
    articles_new: int = 0
    articles_duplicate: int = 0
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    scraped_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "source_name": self.source_name,
            "source_url": self.source_url,
            "status": self.status,
            "articles_found": self.articles_found,
            "articles_new": self.articles_new,
            "articles_duplicate": self.articles_duplicate,
            "error_message": self.error_message,
            "duration_seconds": round(self.duration_seconds, 2),
            "scraped_at": self.scraped_at.isoformat(),
        }
