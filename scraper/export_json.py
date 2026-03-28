"""
Export scraped articles to static JSON files for the frontend.
Optimized for small file size - strips nulls and limits to recent articles.
"""
import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime, timezone


def export_all(db_path=None, output_dir=None):
    if db_path is None:
        db_path = str(Path(__file__).parent.parent / "data" / "ai_pulse.db")
    if output_dir is None:
        output_dir = str(Path(__file__).parent.parent / "frontend" / "public" / "data")

    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    def row_to_dict(r):
        """Convert row to dict, stripping null fields to save space."""
        d = {
            "id": r["id"],
            "title": r["title"],
            "url": r["url"],
            "source_name": r["source_name"],
            "published_at": r["published_at"],
            "tags": r["tags"].split(",") if r["tags"] else [],
            "audiences": r["audiences"].split(",") if r["audiences"] else [],
        }
        # Only include non-null optional fields
        if r["summary"]:
            d["summary"] = r["summary"][:300]  # Truncate for size
        if r["image_url"]:
            d["image_url"] = r["image_url"]
        if r["author"]:
            d["author"] = r["author"]
        return d

    # Latest 400 articles (sweet spot: enough content, small file)
    rows = conn.execute(
        "SELECT * FROM articles ORDER BY published_at DESC LIMIT 400"
    ).fetchall()
    all_articles = [row_to_dict(r) for r in rows]

    def write_json(filename, data):
        """Write compact JSON (no indentation, no extra spaces)."""
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, separators=(",", ":"))
        size_kb = os.path.getsize(filepath) / 1024
        return size_kb

    # All articles
    size = write_json("articles.json", {
        "articles": all_articles,
        "total": len(all_articles),
        "limit": 400,
        "offset": 0,
    })
    print(f"articles.json: {len(all_articles)} articles ({size:.0f}KB)")

    # Per-audience feeds
    for audience in ["developers", "business", "finance", "research"]:
        filtered = [a for a in all_articles if audience in a["audiences"]]
        size = write_json(f"feed-{audience}.json", {
            "articles": filtered,
            "total": len(filtered),
            "limit": 400,
            "offset": 0,
        })
        print(f"  feed-{audience}.json: {len(filtered)} articles ({size:.0f}KB)")

    # Stats
    total = conn.execute("SELECT COUNT(*) as c FROM articles").fetchone()["c"]
    scrapes = conn.execute("SELECT COUNT(*) as c FROM scrape_logs").fetchone()["c"]
    success = conn.execute(
        "SELECT COUNT(*) as c FROM scrape_logs WHERE status = 'success'"
    ).fetchone()["c"]
    by_source = conn.execute(
        "SELECT source_name, COUNT(*) as c FROM articles GROUP BY source_name ORDER BY c DESC LIMIT 20"
    ).fetchall()

    write_json("stats.json", {
        "total_articles": total,
        "total_scrapes": scrapes,
        "successful_scrapes": success,
        "success_rate": round(success / scrapes, 2) if scrapes > 0 else 0,
        "articles_by_source": {r["source_name"]: r["c"] for r in by_source},
        "last_updated": datetime.now(timezone.utc).isoformat(),
    })

    conn.close()
    print("\nJSON export complete!")


if __name__ == "__main__":
    export_all()
