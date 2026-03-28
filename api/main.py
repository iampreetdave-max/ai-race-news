"""
AI Pulse API - FastAPI Application
"""
import sys
import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Query, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import (
    ArticleResponse,
    ArticleListResponse,
    ScrapeLogResponse,
    StatsResponse,
    ScrapeRunResponse,
    HealthResponse,
)
from scraper.database import get_database
from scraper.pipeline import run_scraper

app = FastAPI(
    title="AI Pulse API",
    description=(
        "Real-time AI, ML & Data news aggregated from 110+ sources. "
        "Filter by audience: developers, business, finance, research."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
def health_check():
    return HealthResponse(timestamp=datetime.utcnow())


@app.get("/api/v1/articles", response_model=ArticleListResponse)
def get_articles(
    audience: Optional[str] = Query(
        None,
        description="Filter by audience: developers, business, finance, research, general",
    ),
    tags: Optional[str] = Query(
        None,
        description="Comma-separated tags: llm, funding, tutorial, etc.",
    ),
    source: Optional[str] = Query(None, description="Filter by source name"),
    since: Optional[str] = Query(
        None, description="ISO date string, e.g. 2026-03-01T00:00:00"
    ),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    db = get_database()
    tag_list = [t.strip() for t in tags.split(",")] if tags else None
    since_dt = None
    if since:
        try:
            since_dt = datetime.fromisoformat(since)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use ISO format.",
            )

    articles = db.get_articles(
        audience=audience,
        tags=tag_list,
        source=source,
        limit=limit,
        offset=offset,
        since=since_dt,
    )

    total = db.get_article_count()

    article_responses = []
    for a in articles:
        article_responses.append(
            ArticleResponse(
                id=a.id,
                title=a.title,
                url=a.url,
                summary=a.summary,
                author=a.author,
                image_url=a.image_url,
                source_name=a.source_name,
                published_at=a.published_at,
                scraped_at=a.scraped_at,
                tags=a.tags,
                audiences=a.audiences,
                priority=a.priority,
            )
        )

    return ArticleListResponse(
        articles=article_responses,
        total=total,
        limit=limit,
        offset=offset,
    )


@app.get("/api/v1/feed/{audience}", response_model=ArticleListResponse)
def get_audience_feed(
    audience: str,
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    valid_audiences = {
        "developers", "business", "finance", "research", "general",
    }
    if audience not in valid_audiences:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid audience '{audience}'. "
                f"Choose from: {', '.join(sorted(valid_audiences))}"
            ),
        )

    db = get_database()
    articles = db.get_articles(
        audience=audience, limit=limit, offset=offset
    )
    total = db.get_article_count()

    article_responses = [
        ArticleResponse(
            id=a.id,
            title=a.title,
            url=a.url,
            summary=a.summary,
            author=a.author,
            image_url=a.image_url,
            source_name=a.source_name,
            published_at=a.published_at,
            scraped_at=a.scraped_at,
            tags=a.tags,
            audiences=a.audiences,
            priority=a.priority,
        )
        for a in articles
    ]

    return ArticleListResponse(
        articles=article_responses,
        total=total,
        limit=limit,
        offset=offset,
    )


@app.get("/api/v1/stats", response_model=StatsResponse)
def get_stats():
    db = get_database()
    stats = db.get_scrape_stats()
    return StatsResponse(**stats)


@app.get("/api/v1/scrape-logs", response_model=list[ScrapeLogResponse])
def get_scrape_logs(
    limit: int = Query(50, ge=1, le=200),
):
    db = get_database()
    logs = db.get_recent_scrape_logs(limit=limit)
    return [ScrapeLogResponse(**log) for log in logs]


@app.post("/api/v1/scrape/run", response_model=ScrapeRunResponse)
def trigger_scrape(background_tasks: BackgroundTasks):
    """Trigger a scrape run. Runs synchronously for now."""
    stats = run_scraper()
    return ScrapeRunResponse(
        status="completed",
        timestamp=stats["timestamp"],
        duration_seconds=stats["duration_seconds"],
        sources_processed=stats["sources_processed"],
        sources_successful=stats["sources_successful"],
        sources_failed=stats["sources_failed"],
        articles_fetched=stats["articles_fetched"],
        articles_unique=stats["articles_unique"],
        articles_duplicate=stats["articles_duplicate"],
        articles_inserted=stats["articles_inserted"],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
