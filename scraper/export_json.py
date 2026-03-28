"""
Export scraped articles to static JSON files for the frontend.
Runs after each scrape, commits to frontend/public/data/
"""
import json
import sqlite3
import os
from pathlib import Path
from datetime import datetime


def export_all(db_path=None, output_dir=None):
    if db_path is None:
        db_path = str(Path(__file__).parent.parent / "data" / "ai_pulse.db")
    if output_dir is None:
        output_dir = str(Path(__file__).parent.parent / "frontend" / "public" / "data")

    os.makedirs(output_dir, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    def row_to_dict(r):
        tags = r["tags"].split(",") if r["tags"] else []
        audiences = r["audiences"].split(",") if r["audiences"] else []
        return {
            "id": r["id"],
            "title": r["title"],
            "url": r["url"],
            "summary": r["summary"],
            "author": r["author"],
            "image_url": r["image_url"],
            "source_name": r["source_name"],
            "published_at": r["published_at"],
            "scraped_at": r["scraped_at"],
            "tags": tags,
            "audiences": audiences,
            "priority": r["priority"],
        }

    rows = conn.execute(
        "SELECT * FROM articles ORDER BY published_at DESC LIMIT 500"
    ).fetchall()
    all_articles = [row_to_dict(r) for r in rows]

    with open(os.path.join(output_dir, "articles.json"), "w") as f:
        json.dump({"articles": all_articles, "total": len(all_articles), "limit": 500, "offset": 0}, f)
    print(f"Exported {len(all_articles)} articles to articles.json")

    for audience in ["developers", "business", "finance", "research"]:
        filtered = [a for a in all_articles if audience in a["audiences"]]
        with open(os.path.join(output_dir, f"feed-{audience}.json"), "w") as f:
            json.dump({"articles": filtered, "total": len(filtered), "limit": 500, "offset": 0}, f)
        print(f"  {audience}: {len(filtered)} articles")

    total = conn.execute("SELECT COUNT(*) as c FROM articles").fetchone()["c"]
    scrapes = conn.execute("SELECT COUNT(*) as c FROM scrape_logs").fetchone()["c"]
    success = conn.execute("SELECT COUNT(*) as c FROM scrape_logs WHERE status = 'success'").fetchone()["c"]
    by_source = conn.execute("SELECT source_name, COUNT(*) as c FROM articles GROUP BY source_name ORDER BY c DESC").fetchall()

    stats = {
        "total_articles": total,
        "total_scrapes": scrapes,
        "successful_scrapes": success,
        "success_rate": success / scrapes if scrapes > 0 else 0,
        "articles_by_source": {r["source_name"]: r["c"] for r in by_source},
        "last_updated": datetime.utcnow().isoformat(),
    }
    with open(os.path.join(output_dir, "stats.json"), "w") as f:
        json.dump(stats, f)
    print(f"  stats: {total} total articles")

    conn.close()
    print("JSON export complete!")


if __name__ == "__main__":
    export_all()
