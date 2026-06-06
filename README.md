# AI Race News

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)

A production news-aggregation platform for AI, ML, and data: a scheduled scraping pipeline ingests 110+ sources every 15 minutes, deduplicates and auto-tags every article, and serves audience-specific feeds through a public REST API and a Next.js frontend.

## Overview

AI Race News solves the firehose problem: AI news is scattered across publications, official lab blogs, newsletters, and Reddit, and what matters to a developer is noise to an investor. The platform continuously ingests all of it into one normalized store, classifies each article by audience (developers, business, finance, research, general) and topic tags, and exposes the result as filterable feeds.

The system runs unattended. APScheduler triggers a full scrape cycle every 15 minutes; each cycle fetches RSS/Atom feeds and scrapes HTML sources, normalizes and deduplicates the results, tags them, and writes to the database. The API and scraper run as separate services under Docker Compose, and the frontend deploys to Netlify.

## Key Features

- 110+ sources: RSS/Atom feeds and HTML scraping across top AI/ML publications, official lab blogs, newsletters, and Reddit (full catalog in `sources_100.py`)
- Audience classification: every article routed to developers, business, finance, research, or general feeds
- Three-layer deduplication: URL normalization, content hashing, and title-similarity matching
- Auto-tagging across 12 topic categories (LLM, computer vision, robotics, funding, open-source, tutorial, and more) via keyword classification
- Public REST API (FastAPI) with filtering by audience, tags, source, and date, plus pagination
- Scheduled ingestion: APScheduler runs the full pipeline every 15 minutes
- Scrape observability: per-run logs queryable through the API
- Test suite under `tests/` (pytest)

## Architecture

```
sources_100.py (110+ sources)
        |
        v
rss_fetcher.py / html_scraper.py     fetch
        |
        v
deduplicator.py                      URL + hash + title dedup
        |
        v
tagger.py                            audience + 12-category tagging
        |
        v
database.py (SQLite)                 normalized article store
        |
        +--> api/main.py (FastAPI)   REST API: feeds, filters, stats
        +--> frontend/ (Next.js)     web UI (Netlify)

pipeline.py orchestrates each cycle; run.py is the CLI entry point;
APScheduler triggers the cycle every 15 minutes.
```

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/articles` | All articles, filterable |
| GET | `/api/v1/feed/{audience}` | Audience-specific feed |
| GET | `/api/v1/stats` | Database statistics |
| GET | `/api/v1/scrape-logs` | Recent scrape-run logs |
| POST | `/api/v1/scrape/run` | Trigger an on-demand scrape |

Query parameters: `audience` (developers, business, finance, research, general), `tags` (comma-separated), `source`, `since` (ISO date), `limit`/`offset` for pagination. Interactive docs at `/docs`.

## Tech Stack

- Pipeline and API: Python, FastAPI, APScheduler, BeautifulSoup, SQLite
- Frontend: Next.js, TypeScript, Tailwind CSS (deployed via Netlify)
- Operations: Docker, Docker Compose, Makefile, pytest

## Getting Started

### Run with Docker (recommended)

```bash
git clone https://github.com/iampreetdave-max/ai-race-news.git
cd ai-race-news
docker-compose up -d --build
```

This starts the API on port 8000 and the scheduled scraper (15-minute cycle).

### Run Locally

```bash
pip install -r requirements.txt

python run.py             # one scrape cycle
python run.py --api       # start the API server (http://localhost:8000/docs)
python run.py --schedule  # run the scraper on the 15-minute schedule
python run.py --stats     # print database statistics
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Tests

```bash
pytest tests/ -v
```

## Project Structure

```
ai-race-news/
├── api/
│   ├── main.py             # FastAPI application
│   └── schemas.py          # Pydantic models
├── scraper/
│   ├── config.py           # Sources, tags, settings
│   ├── models.py           # Article, ScrapeResult dataclasses
│   ├── rss_fetcher.py      # RSS/Atom feed parser
│   ├── html_scraper.py     # HTML scraper
│   ├── deduplicator.py     # URL + hash + title dedup
│   ├── tagger.py           # Keyword-based tagging
│   ├── database.py         # SQLite layer
│   └── pipeline.py         # Cycle orchestrator
├── frontend/               # Next.js + Tailwind web UI (Netlify)
├── tests/                  # pytest suite
├── sources_100.py          # Full 110+ source catalog
├── run.py                  # CLI entry point
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── LICENSE
```

## Roadmap

- AI Race dashboard: model benchmark comparisons across labs
- Webhook subscriptions and WebSocket real-time updates
- LinkedIn content automation

## License

MIT — see [LICENSE](LICENSE).
