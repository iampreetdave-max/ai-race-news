"""
Export scraped articles to static JSON files for the frontend.

Pipeline:
  1. Content quality filter  - drop thin summaries / bad images
  2. Fuzzy dedup             - collapse near-duplicate titles, keep best source
  3. Trending score          - boost articles covered by multiple sources in 24h
  4. Display score sort      - tier x trending x freshness_decay, top 500 exported

Also generates:
  - Atom 1.0 RSS feeds  -> frontend/public/feed.xml + feed-{audience}.xml
  - sitemap.xml         -> frontend/public/sitemap.xml
"""
import json
import math
import os
import re
import sqlite3
from datetime import datetime, timedelta, timezone
from difflib import SequenceMatcher
from pathlib import Path


SITE_URL = "https://ai-race-news.pages.dev"

# ---------------------------------------------------------------------------
# Source credibility tiers  (1 = most authoritative, 7 = weakest)
# ---------------------------------------------------------------------------
SOURCE_PRIORITIES: dict[str, int] = {
    "HuggingFace Blog": 1, "OpenAI Blog": 1, "DeepMind Blog": 1,
    "Google AI Blog": 1, "NVIDIA AI Blog": 1, "Microsoft Research": 1,
    "Anthropic News": 1,
    "The Decoder": 2, "MarkTechPost": 2, "Synced Review": 2,
    "AI News": 2, "AI Business": 2, "CB Insights AI": 2, "Emerj AI": 2,
    "VentureBeat AI": 3, "TechCrunch": 3, "The Verge": 3,
    "Wired AI": 3, "Ars Technica": 3, "MIT Technology Review": 3,
    "Bloomberg Technology": 3,
    "Last Week in AI": 4, "Latent Space": 4, "Ahead of AI": 4,
    "The Gradient": 4, "AI Snake Oil": 4, "Interconnects": 4,
    "SemiAnalysis": 4, "Import AI": 4, "TheSequence": 4, "One Useful Thing": 4,
    "KDnuggets": 5, "Machine Learning Mastery": 5, "LangChain Blog": 5,
    "Towards Data Science": 5, "Stack Overflow Blog": 5, "DEV Community": 5,
    "Hacker Noon AI": 5, "Replicate Blog": 5, "Weights & Biases": 5,
    "arXiv cs.AI": 5, "arXiv cs.LG": 5, "arXiv cs.CL": 5, "arXiv cs.CV": 5,
    "MIT News ML": 5, "Berkeley BAIR": 5, "ScienceDaily AI": 5,
    "Google Research": 5,
    "IEEE Spectrum AI": 6, "The Guardian AI": 6, "The Register AI": 6,
    "SiliconANGLE AI": 6, "Crunchbase News": 6,
    "r/MachineLearning": 7, "r/LocalLLaMA": 7, "r/artificial": 7,
    "r/deeplearning": 7, "r/datascience": 7, "r/ChatGPT": 7,
    "Simon Willison": 7, "Chip Huyen": 7, "Eugene Yan": 7, "R-bloggers": 7,
}

MIN_SUMMARY_CHARS = 80
DEDUP_THRESHOLD = 0.55
TRENDING_WINDOW_HOURS = 24
TRENDING_THRESHOLD = 0.55
TRENDING_BOOST = 0.3
FRESHNESS_HALF_LIFE_H = 24
OUTPUT_LIMIT = 500

_BAD_IMAGE_RE = re.compile(
    r"1[xX]1"
    r"|pixel\."
    r"|tracking"
    r"|beacon"
    r"|spacer\.gif|blank\.gif|transparent\.gif"
    r"|\/og[-_]image"
    r"|\/social[-_]"
    r"|noimage|no[-_]image|placeholder",
    re.IGNORECASE,
)


def _source_priority(source_name: str) -> int:
    return SOURCE_PRIORITIES.get(source_name, 6)


def _tier_score(priority: int) -> float:
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
    dt = _parse_dt(published_at)
    if dt is None:
        return 0.5
    age_h = (now - dt).total_seconds() / 3600
    return math.exp(-0.693 * age_h / FRESHNESS_HALF_LIFE_H)


def _quality_filter(articles: list[dict]) -> list[dict]:
    return [a for a in articles if len((a.get("summary") or "")) >= MIN_SUMMARY_CHARS]


def _dedup(articles: list[dict]) -> list[dict]:
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
                if pri_i <= pri_j:
                    keep[j] = False
                else:
                    keep[i] = False
                    break
    return [a for a, ok in zip(articles, keep) if ok]


def _source_counts(articles: list[dict], now: datetime) -> dict[int, int]:
    cutoff = now - timedelta(hours=TRENDING_WINDOW_HOURS)
    recent = [
        a for a in articles
        if (dt := _parse_dt(a["published_at"])) is not None and dt >= cutoff
    ]
    if len(recent) < 2:
        return {a["id"]: 1 for a in articles}
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

    cluster_sources: dict[int, set[str]] = {}
    for a in recent:
        root = find(a["id"])
        cluster_sources.setdefault(root, set()).add(a["source_name"])

    recent_ids = {a["id"] for a in recent}
    counts: dict[int, int] = {}
    for a in articles:
        if a["id"] not in recent_ids:
            counts[a["id"]] = 1
        else:
            counts[a["id"]] = len(cluster_sources.get(find(a["id"]), {a["source_name"]}))
    return counts


def _display_score(article: dict, src_count: int, now: datetime) -> float:
    tier = _tier_score(_source_priority(article["source_name"]))
    trending_mult = 1.0 + TRENDING_BOOST * (src_count - 1)
    return tier * trending_mult * _freshness(article["published_at"], now)


# ---------------------------------------------------------------------------
# RSS / Atom feed generation
# ---------------------------------------------------------------------------
def _xe(text: str) -> str:
    """XML-escape a string."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
    )


def _atom_feed(
    articles: list[dict],
    filepath: str,
    title: str,
    feed_url: str,
    alt_url: str,
    now: datetime,
) -> float:
    updated = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    entries = []
    for a in articles[:50]:
        t = _xe(a["title"])
        s = _xe((a.get("summary") or "")[:400])
        u = _xe(a["url"])
        author = _xe(a.get("author") or a["source_name"])
        try:
            pub_dt = datetime.fromisoformat(a["published_at"].replace("Z", "+00:00"))
            pub = pub_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception:
            pub = updated
        cats = "".join(
            '    <category term="' + _xe(tag) + '"/>\n'
            for tag in a.get("tags", [])[:5]
        )
        entry = (
            "  <entry>\n"
            "    <title>" + t + "</title>\n"
            '    <link href="' + u + '" rel="alternate"/>\n'
            "    <id>" + u + "</id>\n"
            "    <updated>" + pub + "</updated>\n"
            '    <summary type="text">" + s + "</summary>\n'
            "    <author><name>" + author + "</name></author>\n"
            + cats +
            "  </entry>"
        )
        entries.append(entry)

    content = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<feed xmlns="http://www.w3.org/2005/Atom">\n'
        '  <title>' + _xe(title) + '</title>\n'
        '  <link href="' + _xe(alt_url) + '" rel="alternate"/>\n'
        '  <link href="' + _xe(feed_url) + '" rel="self" type="application/atom+xml"/>\n'
        '  <id>' + _xe(alt_url) + '/</id>\n'
        '  <updated>' + updated + '</updated>\n'
        + "\n".join(entries)
        + "\n</feed>\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.getsize(filepath) / 1024


def _sitemap(public_dir: str, now: datetime):
    pages = [
        ("/", "1.0", "daily"),
        ("/developers", "0.9", "daily"),
        ("/business", "0.9", "daily"),
        ("/finance", "0.9", "daily"),
        ("/research", "0.9", "daily"),
        ("/ai-race", "0.8", "weekly"),
    ]
    lastmod = now.strftime("%Y-%m-%d")
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path, priority, freq in pages:
        lines += [
            "  <url>",
            "    <loc>" + SITE_URL + path + "</loc>",
            "    <lastmod>" + lastmod + "</lastmod>",
            "    <changefreq>" + freq + "</changefreq>",
            "    <priority>" + priority + "</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    with open(os.path.join(public_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main export
# ---------------------------------------------------------------------------
def export_all(db_path=None, output_dir=None):
    if db_path is None:
        db_path = str(Path(__file__).parent.parent / "data" / "ai_pulse.db")
    if output_dir is None:
        output_dir = str(Path(__file__).parent.parent / "frontend" / "public" / "data")

    os.makedirs(output_dir, exist_ok=True)
    public_dir = str(Path(output_dir).parent)
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

    rows = conn.execute(
        "SELECT * FROM articles ORDER BY published_at DESC LIMIT 1500"
    ).fetchall()
    raw = [row_to_dict(r) for r in rows]
    print(f"Fetched {len(raw)} articles from DB")

    after_quality = _quality_filter(raw)
    print(f"Quality filter : {len(raw)} -> {len(after_quality)} ({len(raw) - len(after_quality)} removed)")

    after_dedup = _dedup(after_quality)
    print(f"Dedup          : {len(after_quality)} -> {len(after_dedup)} ({len(after_quality) - len(after_dedup)} removed)")

    counts = _source_counts(after_dedup, now)
    trending_count = sum(1 for v in counts.values() if v > 1)
    print(f"Trending       : {trending_count} articles covered by 2+ sources")

    for a in after_dedup:
        n = counts.get(a["id"], 1)
        if n > 1:
            a["trending_sources"] = n

    after_dedup.sort(key=lambda a: -_display_score(a, counts.get(a["id"], 1), now))
    all_articles = after_dedup[:OUTPUT_LIMIT]

    def write_json(filename: str, data) -> float:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, separators=(",", ":"))
        return os.path.getsize(filepath) / 1024

    size = write_json("articles.json", {
        "articles": all_articles, "total": len(all_articles),
        "limit": OUTPUT_LIMIT, "offset": 0,
    })
    print(f"\narticles.json      : {len(all_articles)} articles ({size:.0f} KB)")

    audience_feeds: dict[str, list[dict]] = {}
    for audience in ["developers", "business", "finance", "research"]:
        feed = [a for a in all_articles if audience in a["audiences"]]
        audience_feeds[audience] = feed
        size = write_json(f"feed-{audience}.json", {
            "articles": feed, "total": len(feed),
            "limit": OUTPUT_LIMIT, "offset": 0,
        })
        print(f"  feed-{audience}.json : {len(feed)} articles ({size:.0f} KB)")

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
        "total_articles": total, "total_scrapes": scrapes,
        "successful_scrapes": success,
        "success_rate": round(success / scrapes, 2) if scrapes > 0 else 0,
        "articles_by_source": {r["source_name"]: r["c"] for r in by_source},
        "last_updated": now.isoformat(),
    })
    conn.close()

    # RSS Atom feeds
    audience_labels = {
        "developers": "Developers", "business": "Business",
        "finance": "Finance", "research": "Research",
    }
    _atom_feed(
        all_articles,
        os.path.join(public_dir, "feed.xml"),
        "AI Race News",
        SITE_URL + "/feed.xml",
        SITE_URL,
        now,
    )
    for audience, label in audience_labels.items():
        _atom_feed(
            audience_feeds[audience],
            os.path.join(public_dir, f"feed-{audience}.xml"),
            f"AI Race News - {label}",
            SITE_URL + f"/feed-{audience}.xml",
            SITE_URL + f"/{audience}",
            now,
        )
    print("RSS feeds generated")

    _sitemap(public_dir, now)
    print("sitemap.xml generated")

    print("\nJSON export complete!")


if __name__ == "__main__":
    export_all()
