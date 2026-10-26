"""
Tests for AI Pulse Scraper
"""
import pytest
from datetime import datetime

from scraper.models import Article, ScrapeResult
from scraper.deduplicator import Deduplicator, deduplicate_articles
from scraper.tagger import Tagger, tag_articles, get_tag_statistics
from scraper.database import Database


class TestArticleModel:
    def test_create_article(self, sample_article):
        assert sample_article.title == "OpenAI Releases GPT-5 with Breakthrough Reasoning"
        assert sample_article.id is not None
        assert sample_article.content_hash is not None

    def test_article_id_from_url(self):
        a1 = Article(title="Test", url="https://example.com/1", source_name="Test")
        a2 = Article(title="Test", url="https://example.com/2", source_name="Test")
        assert a1.id != a2.id

    def test_content_hash_differs(self):
        a1 = Article(title="Article One", url="https://example.com/1", source_name="Test")
        a2 = Article(title="Article Two", url="https://example.com/2", source_name="Test")
        assert a1.content_hash != a2.content_hash

    def test_to_dict(self, sample_article):
        d = sample_article.to_dict()
        assert d["title"] == sample_article.title
        assert d["url"] == sample_article.url
        assert isinstance(d["tags"], str)
        assert isinstance(d["audiences"], str)

    def test_from_dict(self, sample_article):
        d = sample_article.to_dict()
        restored = Article.from_dict(d)
        assert restored.title == sample_article.title
        assert restored.url == sample_article.url


class TestDeduplicator:
    def test_url_dedup(self):
        dedup = Deduplicator()
        a1 = Article(title="Test 1", url="https://example.com/same", source_name="A")
        a2 = Article(title="Test 2", url="https://example.com/same", source_name="B")

        assert not dedup.is_duplicate(a1)
        dedup.mark_seen(a1)
        assert dedup.is_duplicate(a2)

    def test_tracking_param_removal(self):
        dedup = Deduplicator()
        a1 = Article(title="Test", url="https://example.com/article", source_name="A")
        a2 = Article(title="Test 2", url="https://example.com/article?utm_source=twitter", source_name="B")

        assert not dedup.is_duplicate(a1)
        dedup.mark_seen(a1)
        assert dedup.is_duplicate(a2)

    def test_title_similarity_dedup(self):
        dedup = Deduplicator()
        a1 = Article(
            title="OpenAI Releases GPT-5 with Major Improvements",
            url="https://site1.com/gpt5",
            source_name="A",
        )
        a2 = Article(
            title="OpenAI Releases GPT-5 with Major Improvements - TechCrunch",
            url="https://site2.com/gpt5",
            source_name="B",
        )

        assert not dedup.is_duplicate(a1)
        dedup.mark_seen(a1)
        assert dedup.is_duplicate(a2)

    def test_deduplicate_batch(self, sample_articles):
        # Add a duplicate
        dupe = Article(
            title="OpenAI Releases GPT-5 with Breakthrough Reasoning",
            url="https://other-site.com/gpt5",
            summary="OpenAI has released GPT-5 with major reasoning improvements.",
            source_name="VentureBeat",
        )
        articles = sample_articles + [dupe]
        unique, dupes = deduplicate_articles(articles)
        assert dupes >= 1
        assert len(unique) < len(articles)


class TestTagger:
    def test_tag_llm_article(self):
        tagger = Tagger()
        article = Article(
            title="OpenAI GPT-5 Shows Major Advances in Language Understanding",
            url="https://example.com/gpt5",
            summary="The new GPT-5 transformer model from OpenAI sets new benchmarks.",
            source_name="Test",
        )
        tagged = tagger.tag_article(article)
        assert "llm" in tagged.tags

    def test_tag_funding_article(self):
        tagger = Tagger()
        article = Article(
            title="AI Startup Raises $500M in Series C Funding",
            url="https://example.com/funding",
            summary="Investors value the company at $5 billion after latest investment round.",
            source_name="Crunchbase",
        )
        tagged = tagger.tag_article(article)
        assert "funding" in tagged.tags
        assert "finance" in tagged.audiences or "business" in tagged.audiences

    def test_tag_tutorial(self):
        tagger = Tagger()
        article = Article(
            title="How to Build a RAG Pipeline Step-by-Step",
            url="https://example.com/tutorial",
            summary="A hands-on guide to building retrieval augmented generation with vector embeddings.",
            source_name="Test",
        )
        tagged = tagger.tag_article(article)
        assert "tutorial" in tagged.tags or "rag" in tagged.tags
        assert "developers" in tagged.audiences

    def test_general_audience_fallback(self):
        tagger = Tagger()
        article = Article(
            title="The Future of Technology",
            url="https://example.com/future",
            summary="A look at what the future holds.",
            source_name="Test",
        )
        tagged = tagger.tag_article(article)
        if not tagged.tags:
            assert "general" in tagged.audiences

    def test_tag_statistics(self, sample_articles):
        tagged = tag_articles(sample_articles)
        stats = get_tag_statistics(tagged)
        assert stats["total_articles"] == len(sample_articles)
        assert isinstance(stats["tag_counts"], dict)
        assert isinstance(stats["audience_counts"], dict)


class TestDatabase:
    def test_insert_and_retrieve(self, tmp_db, sample_article):
        assert tmp_db.insert_article(sample_article)
        articles = tmp_db.get_articles(limit=10)
        assert len(articles) >= 1
        assert articles[0].title == sample_article.title

    def test_duplicate_insert_ignored(self, tmp_db, sample_article):
        assert tmp_db.insert_article(sample_article)
        assert not tmp_db.insert_article(sample_article)  # duplicate

    def test_insert_batch(self, tmp_db, sample_articles):
        inserted, dupes = tmp_db.insert_articles(sample_articles)
        assert inserted == len(sample_articles)
        assert dupes == 0
        assert tmp_db.get_article_count() == len(sample_articles)

    def test_filter_by_audience(self, tmp_db):
        dev_article = Article(
            title="Python Tutorial",
            url="https://example.com/python",
            source_name="Test",
        )
        dev_article.audiences = ["developers"]
        biz_article = Article(
            title="AI Funding Round",
            url="https://example.com/funding",
            source_name="Test",
        )
        biz_article.audiences = ["business"]

        tmp_db.insert_article(dev_article)
        tmp_db.insert_article(biz_article)

        dev_results = tmp_db.get_articles(audience="developers")
        assert len(dev_results) >= 1
        assert all("developers" in a.audiences for a in dev_results)

    def test_scrape_log(self, tmp_db):
        result = ScrapeResult(
            source_name="Test",
            source_url="https://example.com",
            status="success",
            articles_found=10,
            articles_new=8,
        )
        tmp_db.log_scrape(result)
        logs = tmp_db.get_recent_scrape_logs(limit=5)
        assert len(logs) >= 1
        assert logs[0]["source_name"] == "Test"

    def test_stats(self, tmp_db, sample_articles):
        tmp_db.insert_articles(sample_articles)
        stats = tmp_db.get_scrape_stats()
        assert stats["total_articles"] == len(sample_articles)

    def test_existing_hashes(self, tmp_db, sample_articles):
        tmp_db.insert_articles(sample_articles)
        hashes = tmp_db.get_existing_hashes()
        assert len(hashes) == len(sample_articles)

    def test_existing_urls(self, tmp_db, sample_articles):
        tmp_db.insert_articles(sample_articles)
        urls = tmp_db.get_existing_urls()
        assert len(urls) == len(sample_articles)


class TestTapriExport:
    """tapri.json feeds tensortapri.org/brewing: one entry per story, India split out, no jobs."""

    def test_week_pick(self):
        from datetime import timedelta, timezone
        from scraper.export_json import _source_counts, _story_clusters, _tapri_pick

        now = datetime(2026, 10, 25, 12, tzinfo=timezone.utc)

        def art(i, title, source, hours_ago=5):
            at = (now - timedelta(hours=hours_ago)).replace(tzinfo=None).isoformat()
            return {"id": str(i), "title": title, "url": f"https://x.in/{i}", "source_name": source, "published_at": at}

        arts = [
            art(1, "Mistral introduces Duet, a proactive AI agent for teams", "The Decoder"),
            art(2, "Mistral takes on Muse with Duet, its new AI agent for teams", "The Verge"),
            art(3, "Duet is an always-on AI agent for teams from Mistral", "TechCrunch"),
            art(4, "Sarvam AI launches a Gujarati voice model", "Inc42"),
            art(5, "Zepto is hiring 500 AI engineers", "Inc42"),  # jobs content: never shown
            art(6, "The best phones under Rs 20,000", "Mint Technology"),  # general tech, no AI in title
            art(8, "OnePlus 15 gets new AI features in OxygenOS update", "Mint Technology"),  # gadget news
            art(9, "Mistral Duet arrives for Indian teams as an AI agent", "Analytics India Magazine"),  # global story
            art(7, "Older AI news", "The Decoder", hours_ago=24 * 8),  # outside the week
        ]
        roots = _story_clusters(arts, now, 24 * 7)
        out = _tapri_pick(arts, roots, _source_counts(arts, roots), now)

        assert [(a["source"], a["n"]) for a in out["world"]] == [("The Decoder", 4)]  # 4 headlines, 1 story
        # India gets only what no outlet outside India covered: not the Duet reprint, not the phone update
        assert [a["title"] for a in out["india"]] == ["Sarvam AI launches a Gujarati voice model"]
        # the pulse counts every kept headline (jobs, gadgets, non-AI and old ones excluded), by IST day; 12:30 IST is today
        p = out["pulse"]
        assert (p["headlines"], p["outlets"], p["india"]) == (5, 5, 2)
        assert p["days"][-1] == "2026-10-25" and len(p["days"]) == 7
        assert p["names"] == [{"name": "Mistral", "days": [0] * 6 + [4]}, {"name": "Sarvam", "days": [0] * 6 + [1]}]

    def test_bench_records(self):
        import io
        import zipfile
        from datetime import date
        from scraper.export_json import _bench

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as z:
            z.writestr("model_metadata.csv", "model_version,display_name\nm-a_high,Model A (high)\nm-b,Model B\n")
            z.writestr("hle_external.csv", "Model version,Accuracy,Release date\n"
                       "m-a_high,0.10,2025-01-01\n"      # first record
                       "m-x,0.05,2025-03-01\n"           # worse than the record: not a point
                       "m-b,0.30,2026-01-01\n"
                       "m-y,0.20,2026-06-01\n"           # same day as the next one, which is higher
                       "m-z,0.40,2026-06-01\n")
            z.writestr("swe_bench_verified.csv", "Model version,mean_score,Release date\nm-b,0.5,2026-02-01\n")
            z.writestr("metr_time_horizons_external.csv", "Model version,Time horizon,Release date,METR version\n"
                       "m-a_high,30,2025-01-01,METR-Horizon-v1.1\n"
                       "m-b,600,2026-01-01,METR-Horizon-v1.0\n"  # other method version: left out
                       "m-b,120,2026-01-01,METR-Horizon-v1.1\n")
            z.writestr("gpqa_diamond.csv", "Model version,mean_score,Release date\n")
            z.writestr("epoch_capabilities_index/eci_scores.csv",
                       "Display name,eci,date,Organization,Country (of organization),Accessibility group\n"
                       "Gem 1,140,2025-06-01,Google DeepMind,United States of America,Other\n"
                       "Gem 2,160.04,2026-09-01,Google,United States of America,Closed weights\n"  # same lab, other name
                       "Seek 1,150,2026-09-09,\"DeepSeek,Peking University\",\"China,China\",Open weights\n"  # first lab named
                       "Mystery,170,2026-01-01,,,Other\n")                                  # no lab: skipped
        bench = _bench(buf.getvalue(), date(2026, 10, 26))
        assert bench["labs"] == [
            {"lab": "Google", "country": "United States of America", "eci": 160.0, "model": "Gem 2", "date": "2026-09-01",
             "open": False, "eci_ago": 140.0, "model_ago": "Gem 1"},
            {"lab": "DeepSeek", "country": "China", "eci": 150.0, "model": "Seek 1", "date": "2026-09-09",
             "open": True, "eci_ago": None, "model_ago": None},
        ]
        out = {t["key"]: t for t in bench["tests"]}

        assert out["hle"]["line"] == [["2025-01-01", 10.0, "Model A"], ["2026-01-01", 30.0, "Model B"], ["2026-06-01", 40.0, "m-z"]]
        assert out["hle"]["year_ago"] == 10.0                          # the record standing on 2025-10-26
        assert out["swe"]["year_ago"] is None                         # no record that old
        assert out["horizon"]["line"] == [["2025-01-01", 0.5, "Model A"], ["2026-01-01", 2.0, "Model B"]]  # minutes -> hours
        assert out["gpqa"]["line"] == []
