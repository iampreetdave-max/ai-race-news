"""
Export scraped articles to static JSON files for the frontend.

Pipeline (in order):
  1. Content quality filter  - drop articles with thin summaries or bad images
  2. Fuzzy dedup             - collapse near-duplicate titles, keep best source
  3. Trending score          - boost articles covered by multiple sources in 24h
  4. Display score sort      - tier × trending × freshness_decay, top 500 exported
"""
import json
import math
import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path


# ---------------------------------------------------------------------------
# Source credibility tiers  (1 = most authoritative, 7 = weakest)
# ---------------------------------------------------------------------------
SOURCE_PRIORITIES: dict[str, int] = {
    # Priority 1 – Official AI company blogs
    "HuggingFace Blog": 1, "OpenAI Blog": 1, "DeepMind Blog": 1,
    "Google AI Blog": 1, "NVIDIA AI Blog": 1, "Microsoft Research": 1,
    "Anthropic News": 1,
    # Priority 2 – AI-focused publications
    "The Decoder": 2, "MarkTechPost": 2, "Synced Review": 2,
    "AI News": 2, "AI Business": 2, "CB Insights AI": 2, "Emerj AI": 2,
    # Priority 3 – Major tech news
    "VentureBeat AI": 3, "TechCrunch": 3, "The Verge": 3,
    "Wired AI": 3, "Ars Technica": 3, "MIT Technology Review": 3,
    "Bloomberg Technology": 3,
    # Priority 4 – Newsletters & substacks
    "Last Week in AI": 4, "Latent Space": 4, "Ahead of AI": 4,
    "The Gradient": 4, "AI Snake Oil": 4, "Interconnects": 4,
    "SemiAnalysis": 4, "Import AI": 4, "TheSequence": 4, "One Useful Thing": 4,
    # Priority 5 – Developer resources & research
    "KDnuggets": 5, "Machine Learning Mastery": 5, "LangChain Blog": 5,
    "Towards Data Science": 5, "Stack Overflow Blog": 5, "DEV Community": 5,
    "Hacker Noon AI": 5, "Replicate Blog": 5, "Weights & Biases": 5,
    "arXiv cs.AI": 5, "arXiv cs.LG": 5, "arXiv cs.CL": 5, "arXiv cs.CV": 5,
    "MIT News ML": 5, "Berkeley BAIR": 5, "ScienceDaily AI": 5,
    "Google Research": 5,
    # Priority 6 – Other tech outlets
    "IEEE Spectrum AI": 6, "The Guardian AI": 6, "The Register AI": 6,
    "SiliconANGLE AI": 6, "Crunchbase News": 6,
    # Priority 7 – Reddit & personal blogs
    "r/MachineLearning": 7, "r/LocalLLaMA": 7, "r/artificial": 7,
    "r/deeplearning": 7, "r/datascience": 7, "r/ChatGPT": 7,
    "Simon Willison": 7, "Chip Huyen": 7, "Eugene Yan": 7, "R-bloggers": 7,
}

# ---------------------------------------------------------------------------
# Tuning constants
# ---------------------------------------------------------------------------
MIN_SUMMARY_CHARS = 80       # articles shorter than this are dropped
DEDUP_THRESHOLD = 0.55       # title similarity ratio to collapse as duplicate
TRENDING_WINDOW_HOURS = 24   # window for cross-source trending detection
TRENDING_THRESHOLD = 0.55    # title similarity ratio for trending cluster
TRENDING_BOOST = 0.3         # score boost per additional source in cluster
FRESHNESS_HALF_LIFE_H = 24  # hours until freshness score halves
OUTPUT_LIMIT = 500

_BAD_IMAGE_RE = re.compile(
    r"1[xX]1|pixel\.|tracking|beacon|spacer\.gif|blank\.gif|transparent\.gif",
    re.IGNORECASE,
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
def _source_priority(source_name: str) -> int:
    return SOURCE_PRIORITIES.get(source_name, 6)


def _tier_score(priority: int) -> float:
    """Map priority 1→‘7 to score 1.0→→0.14."""
    return (8 - priority) / 7


def _normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def _is_valid_image(url: str) -> bool:
    return bool(url) and not _BAD_IMAGE_RE.search(url)


def _parse_dt(published_at: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def _freshness(published_at: str, now: datetime) -> float:
    """Exponential decay with FRESHNESS_HALF_LIFE_H half-life."""
    dt = _parse_dt(published_at)
    if dt is None:
        return 0.5
    age_h = (now - dt).total_seconds() / 3600
    return math.exp(-0.693 * age_h / FRESHNESS_HALF_LIFE_H)


# ---------------------------------------------------------------------------
# Stage 1: content quality filter
# ---------------------------------------------------------------------------
def _quality_filter(articles: list[dict]) -> list[dict]:
    return [a for a in articles if len((a.get("summary") or "")) >= MIN_SUMMARY_CHARS]


# ---------------------------------------------------------------------------
# Stage 2: fuzzy dedup
# ---------------------------------------------------------------------------
def _dedup(articles: list[dict]) -> list[dict]:
    """Keep highest-priority source when two articles share a similar title."""
    norms = [_normalize_title(a["title"]) for a in articles]
    keep = [True] * len(articles)

    for i in range(len(articles)):
        if not keep[i]:
            continue
        for j in range(i + 1, len(articles)):
            if not keep[j]:
                continue
            if SequenceMatcher(None, norms[i], norms[j]).ratio() >= DEDUP_THRESHOLD:
                pri_i = _source_priority(articles[i]["source_name"])
                pri_j = _source_priority(articles[j]["source_name"])
                if pri_i <= pri_j:   # i is equal or better → drop j
                    keep[j] = False
                else:                # j is better → drop i and move on
                    keep[i] = False
                    break

    return [a for a, ok in zip(articles, keep) if ok]


# ---------------------------------------------------------------------------
# Stage 3: trending score
# ---------------------------------------------------------------------------
def _trending_scores(articles: list[dict], now: datetime) -> dict[int, float]:
    """
    Cluster articles published within TRENDING_WINDOW_HOURS by title similarity.
    Articles covered by N unique sources get a multiplier of 1 + TRENDING_BOOST*(N-1).
    """
    cutoff = now - timedelta(hours=TRENDING_WINDOW_HOURS)
    recent = [
        a for a in articles
        if (dt := _parse_dt(a["published_at"])) is not None and dt >= cutoff
    ]

    if len(recent) < 2:
        return {a["id"]: 1.0 for a in articles}

    norms = {a["id"]: _normalize_title(a["title"]) for a in recent}
    ids = [a["id"] for a in recent]
    parent: dict[int, int] = {aid: aid for aid in ids}

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            if SequenceMatcher(None, norms[ids[i]], norms[ids[j]]).ratio() >= TRENDING_THRESHOLD:
                parent[find(ids[i])] = find(ids[j])

    # Count unique sources per cluster
    cluster_sources: dict[int, set[str]] = {}
    for a in recent:
        root = find(a["id"])
        cluster_sources.setdefault(root, set()).add(a["source_name"])

    recent_ids = {a["id"] for a in recent}
    scores: dict[int, float] = {}
    for a in articles:
        if a["id"] not in recent_ids:
            scores[a["id"]] = 1.0
        else:
            n = len(cluster_sources.get(find(a["id"]), {a["source_name"]}))
            scores[a["id"]] = 1.0 + TRENDING_BOOST * (n - 1)

    return scores


# ---------------------------------------------------------------------------
# Stage 4: display score
# ---------------------------------------------------------------------------
def _display_score(article: dict, trending: dict[int, float], now: datetime) -> float:
    tier = _tier_score(_source_priority(article["source_name"]))
    return tier * trending.get(article["id"], 1.0) * _freshness(article["published_at"], now)


# ---------------------------------------------------------------------------
# Main export
# ---------------------------------------------------------------------------
def export_all(db_path=None, output_dir=None):
    if db_path is None:
        db_path = str(Path(__file__).parent.parent / "data" / "ai_pulse.db")
    if output_dir is None:
        output_dir = str(Path(__file__).parent.parent / "frontend" / "public" / "data")

    os.makedirs(output_dir, exist_ok=True)
    now = datetime.now(timezone.utc)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    def row_to_dict(r) -> dict:
        d: dict = {
            "id": r["id"],
            "title": r["title"],
            "url": r["url"],
            "source_name": r["source_name"],
            "published_at": r["published_at"],
            "tags": r["tags"].split(",") if r["tags"] else [],
            "audiences": r["audiences"].split(",") if r["audiences"] else [],
        }
        if r["summary"]:
            d["summary"] = r["summary"]
        if r["image_url"] and _is_valid_image(r["image_url"]):
            d["image_url"] = r["image_url"]
        if r["author"]:
            d["author"] = r["author"]
        return d

    # Fetch 3× the output limit to absorb quality/dedup losses
    rows = conn.execute(
        "SELECT * FROM articles ORDER BY published_at DESC LIMIT 1500"
    ).fetchall()
    raw = [row_to_dict(r) for r in rows]
    print(f"Fetched {len(raw)} articles from DB")

    # Stage 1: quality filter
    after_quality = _quality_filter(raw)
    print(f"Quality filter : {len(raw)} → {len(after_quality)} ({len(raw) - len(after_quality)} removed)")

    # Stage 2: dedup
    after_dedup = _dedup(after_quality)
    print(f"Dedup          : {len(after_quality)} → {len(after_dedup)} ({len(after_quality) - len(after_dedup)} removed)")

    # Stage 3: trending
    trending = _trending_scores(after_dedup, now)
    clustered = sum(1 for v in trending.values() if v > 1.0)
    print(f"Trending       : {clustered} articles boosted")

    # Stage 4: score + sort + cap
    after_dedup.sort(key=lambda a: -_display_score(a, trending, now))
    all_articles = after_dedup[:OUTPUT_LIMIT]

    def write_json(filename: str, data) -> float:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, separators=(",", ":"))
        return os.path.getsize(filepath) / 1024

    size = write_json("articles.json", {
        "articles": all_articles,
        "total": len(all_articles),
        "limit": OUTPUT_LIMIT,
        "offset": 0,
    })
    print(f"\narticles.json      : {len(all_articles)} articles ({size:.0f} KB)")

    for audience in ["developers", "business", "finance", "research"]:
        feed = [a for a in all_articles if audience in a["audiences"]]
        size = write_json(f"feed-{audience}.json", {
            "articles": feed,
            "total": len(feed),
            "limit": OUTPUT_LIMIT,
            "offset": 0,
        })
        print(f"  feed-{audience}.json : {len(feed)} articles ({size:.0f} KB)")

    # Stats
    total = conn.execute("SELECT COUNT(*) as c FROM articles").fetchone()["c"]
    scrapes = conn.execute("SELECT COUNT(*) as c FROM scrape_logs").fetchone()["c"]
    success = conn.execute(
        "SELECT COUNT(*) as c FROM scrape_logs WHERE status = 'success'"
    ).fetchone()["c"]
    by_source = conn.execute(
        "SELECT source_name, COUNT(*) as c FROM articles "
        "GROUP BY source_name ORDER BY c DESC LIMIT 20"
    ).fetchall()

    write_json("stats.json", {
        "total_articles": total,
        "total_scrapes": scrapes,
        "successful_scrapes": success,
        "success_rate": round(success / scrapes, 2) if scrapes > 0 else 0,
        "articles_by_source": {r["source_name"]: r["c"] for r in by_source},
        "last_updated": now.isoformat(),
    })

    conn.close()
    print("\nJSON export complete!")


if __name__ == "__main__":
    export_all()
