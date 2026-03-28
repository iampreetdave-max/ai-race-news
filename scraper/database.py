"""
AI Pulse Database - SQLite for dev, PostgreSQL for production
"""
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from contextlib import contextmanager

from .models import Article, ScrapeResult
from .config import DB_PATH, DATA_DIR

logger = logging.getLogger(__name__)


class Database:
    """Database interface for AI Pulse."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    @contextmanager
    def _get_connection(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_schema(self) -> None:
        schema = """
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL,
            summary TEXT,
            content TEXT,
            author TEXT,
            image_url TEXT,
            source_name TEXT NOT NULL,
            published_at TIMESTAMP,
            scraped_at TIMESTAMP NOT NULL,
            content_hash TEXT UNIQUE,
            tags TEXT,
            audiences TEXT,
            priority INTEGER DEFAULT 5
        );

        CREATE INDEX IF NOT EXISTS idx_articles_published_at ON articles(published_at DESC);
        CREATE INDEX IF NOT EXISTS idx_articles_source_name ON articles(source_name);
        CREATE INDEX IF NOT EXISTS idx_articles_scraped_at ON articles(scraped_at DESC);
        CREATE INDEX IF NOT EXISTS idx_articles_content_hash ON articles(content_hash);

        CREATE TABLE IF NOT EXISTS scrape_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_name TEXT NOT NULL,
            source_url TEXT NOT NULL,
            status TEXT NOT NULL,
            articles_found INTEGER DEFAULT 0,
            articles_new INTEGER DEFAULT 0,
            articles_duplicate INTEGER DEFAULT 0,
            error_message TEXT,
            duration_seconds REAL DEFAULT 0,
            scraped_at TIMESTAMP NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_scrape_logs_scraped_at ON scrape_logs(scraped_at DESC);
        """

        with self._get_connection() as conn:
            conn.executescript(schema)

        logger.info(f"Database initialized at {self.db_path}")

    def insert_article(self, article: Article) -> bool:
        sql = """
        INSERT OR IGNORE INTO articles
        (id, title, url, summary, content, author, image_url, source_name,
         published_at, scraped_at, content_hash, tags, audiences, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        data = article.to_dict()
        values = (
            data["id"], data["title"], data["url"], data["summary"],
            data["content"], data["author"], data["image_url"], data["source_name"],
            data["published_at"], data["scraped_at"], data["content_hash"],
            data["tags"], data["audiences"], data["priority"]
        )

        with self._get_connection() as conn:
            cursor = conn.execute(sql, values)
            return cursor.rowcount > 0

    def insert_articles(self, articles: list[Article]) -> tuple[int, int]:
        inserted = 0
        duplicates = 0

        for article in articles:
            if self.insert_article(article):
                inserted += 1
            else:
                duplicates += 1

        logger.info(f"Inserted {inserted} articles, {duplicates} duplicates skipped")
        return inserted, duplicates

    def get_existing_hashes(self) -> set[str]:
        sql = "SELECT content_hash FROM articles WHERE content_hash IS NOT NULL"
        with self._get_connection() as conn:
            cursor = conn.execute(sql)
            return {row["content_hash"] for row in cursor.fetchall()}

    def get_existing_urls(self) -> set[str]:
        sql = "SELECT url FROM articles"
        with self._get_connection() as conn:
            cursor = conn.execute(sql)
            return {row["url"] for row in cursor.fetchall()}

    def get_articles(
        self,
        audience: Optional[str] = None,
        tags: Optional[list[str]] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
        since: Optional[datetime] = None,
    ) -> list[Article]:
        sql = "SELECT * FROM articles WHERE 1=1"
        params: list = []

        if audience:
            sql += " AND audiences LIKE ?"
            params.append(f"%{audience}%")

        if tags:
            tag_conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            sql += f" AND ({tag_conditions})"
            params.extend([f"%{tag}%" for tag in tags])

        if source:
            sql += " AND source_name = ?"
            params.append(source)

        if since:
            sql += " AND published_at >= ?"
            params.append(since.isoformat())

        sql += " ORDER BY published_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        with self._get_connection() as conn:
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()
            return [Article.from_dict(dict(row)) for row in rows]

    def get_article_count(self) -> int:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT COUNT(*) as count FROM articles")
            return cursor.fetchone()["count"]

    def get_articles_by_date_range(
        self, start: datetime, end: datetime, limit: int = 100
    ) -> list[Article]:
        sql = """
        SELECT * FROM articles
        WHERE published_at BETWEEN ? AND ?
        ORDER BY published_at DESC
        LIMIT ?
        """
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (start.isoformat(), end.isoformat(), limit))
            rows = cursor.fetchall()
            return [Article.from_dict(dict(row)) for row in rows]

    def log_scrape(self, result: ScrapeResult) -> None:
        sql = """
        INSERT INTO scrape_logs
        (source_name, source_url, status, articles_found, articles_new,
         articles_duplicate, error_message, duration_seconds, scraped_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        data = result.to_dict()
        values = (
            data["source_name"], data["source_url"], data["status"],
            data["articles_found"], data["articles_new"], data["articles_duplicate"],
            data["error_message"], data["duration_seconds"], data["scraped_at"]
        )
        with self._get_connection() as conn:
            conn.execute(sql, values)

    def get_recent_scrape_logs(self, limit: int = 50) -> list[dict]:
        sql = "SELECT * FROM scrape_logs ORDER BY scraped_at DESC LIMIT ?"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_scrape_stats(self) -> dict:
        with self._get_connection() as conn:
            total = conn.execute(
                "SELECT COUNT(*) as count FROM scrape_logs"
            ).fetchone()["count"]
            success = conn.execute(
                "SELECT COUNT(*) as count FROM scrape_logs WHERE status = 'success'"
            ).fetchone()["count"]
            articles = conn.execute(
                "SELECT COUNT(*) as count FROM articles"
            ).fetchone()["count"]
            by_source = conn.execute(
                """
                SELECT source_name, COUNT(*) as count
                FROM articles
                GROUP BY source_name
                ORDER BY count DESC
                """
            ).fetchall()

            return {
                "total_scrapes": total,
                "successful_scrapes": success,
                "success_rate": success / total if total > 0 else 0,
                "total_articles": articles,
                "articles_by_source": {
                    row["source_name"]: row["count"] for row in by_source
                },
            }

    def cleanup_old_articles(self, days: int = 30) -> int:
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        sql = "DELETE FROM articles WHERE scraped_at < ?"
        with self._get_connection() as conn:
            cursor = conn.execute(sql, (cutoff,))
            deleted = cursor.rowcount
        logger.info(f"Cleaned up {deleted} articles older than {days} days")
        return deleted


_db: Optional[Database] = None


def get_database() -> Database:
    global _db
    if _db is None:
        _db = Database()
    return _db
