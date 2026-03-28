# AI Race News

Real-time AI, ML & Data news aggregated from 110+ sources. Filter by audience: developers, business, finance, research.

## Features

- **110+ Sources** - RSS feeds and HTML scraping from top AI/ML publications, official blogs, newsletters, Reddit, and more
- **Audience-Specific Feeds** - News filtered for developers, business, finance, research, or general audiences
- **Smart Deduplication** - URL normalization, content hashing, and title similarity matching
- **Auto-Tagging** - 12 tag categories (LLM, computer vision, robotics, funding, etc.) with keyword-based classification
- **REST API** - FastAPI backend with filtering, pagination, and audience feeds
- **Scheduled Scraping** - APScheduler runs every 15 minutes

## Quick Start

```bash
# Clone
git clone https://github.com/iampreetdave-max/ai-race-news.git
cd ai-race-news

# Install
pip install -r requirements.txt

# Run scraper once
python run.py

# Start API server
python run.py --api
# Visit http://localhost:8000/docs

# Run on schedule (every 15 min)
python run.py --schedule

# View stats
python run.py --stats
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/articles` | All articles (filterable) |
| GET | `/api/v1/feed/{audience}` | Audience-specific feed |
| GET | `/api/v1/stats` | Database statistics |
| GET | `/api/v1/scrape-logs` | Recent scrape logs |
| POST | `/api/v1/scrape/run` | Trigger a scrape |

### Query Parameters

- `audience` - developers, business, finance, research, general
- `tags` - Comma-separated: llm, funding, tutorial, open-source, etc.
- `source` - Filter by source name
- `since` - ISO date (e.g., 2026-03-01T00:00:00)
- `limit` / `offset` - Pagination

## Docker

```bash
docker-compose up -d --build
```

This starts both the API (port 8000) and the scraper (every 15 min).

## Testing

```bash
pytest tests/ -v
```

## Project Structure

```
ai-race-news/
|-- api/
|   |-- main.py              # FastAPI application
|   |-- schemas.py           # Pydantic models
|-- scraper/
|   |-- config.py            # Sources, tags, settings
|   |-- models.py            # Article, ScrapeResult dataclasses
|   |-- rss_fetcher.py       # RSS/Atom feed parser
|   |-- html_scraper.py      # BeautifulSoup HTML scraper
|   |-- deduplicator.py      # URL + hash + title dedup
|   |-- tagger.py            # Keyword-based tagging
|   |-- database.py          # SQLite database layer
|   |-- pipeline.py          # Main orchestrator
|-- tests/
|-- sources_100.py           # Full 110+ source catalog
|-- run.py                   # CLI entry point
|-- requirements.txt
|-- Dockerfile
|-- docker-compose.yml
```

## Roadmap

- [ ] AI Race dashboard (model benchmarks comparison)
- [ ] Webhook subscriptions
- [ ] WebSocket real-time updates
- [ ] LinkedIn automation ($25/mo)
- [ ] Next.js frontend
