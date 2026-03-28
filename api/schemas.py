"""
AI Pulse API - Pydantic Schemas
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ArticleResponse(BaseModel):
    id: str
    title: str
    url: str
    summary: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    source_name: str
    published_at: Optional[datetime] = None
    scraped_at: datetime
    tags: list[str] = []
    audiences: list[str] = []
    priority: int = 5


class ArticleListResponse(BaseModel):
    articles: list[ArticleResponse]
    total: int
    limit: int
    offset: int


class ScrapeLogResponse(BaseModel):
    source_name: str
    source_url: str
    status: str
    articles_found: int = 0
    articles_new: int = 0
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    scraped_at: str


class StatsResponse(BaseModel):
    total_articles: int
    total_scrapes: int
    successful_scrapes: int
    success_rate: float
    articles_by_source: dict[str, int]


class ScrapeRunResponse(BaseModel):
    status: str
    timestamp: str
    duration_seconds: float
    sources_processed: int
    sources_successful: int
    sources_failed: int
    articles_fetched: int
    articles_unique: int
    articles_duplicate: int
    articles_inserted: int


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    timestamp: datetime
