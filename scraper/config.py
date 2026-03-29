"""
AI Pulse Scraper Configuration
"""
import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "ai_pulse.db"

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# Scraper Settings
SCRAPE_INTERVAL_MINUTES = 15
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 5
USER_AGENT = "AI-Pulse-Bot/1.0 (+https://aipulse.dev)"
DELAY_BETWEEN_REQUESTS = 1.0

# Content Settings
MAX_SUMMARY_LENGTH = 500
MAX_ARTICLES_PER_SOURCE = 50
DEDUP_SIMILARITY_THRESHOLD = 0.85

# ============================================================
# RSS SOURCES - 60+ verified working feeds
# Removed: ZDNet AI, Engadget, Gizmodo, The Next Web (too noisy)
# Added: CB Insights, AI Business, Emerj, Weights & Biases
# ============================================================
RSS_SOURCES = [
    # --- Official AI Company Blogs (Priority 1) ---
    {"name": "HuggingFace Blog", "url": "https://huggingface.co/blog/feed.xml", "priority": 1},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "priority": 1},
    {"name": "DeepMind Blog", "url": "https://deepmind.com/blog/feed/basic/", "priority": 1},
    {"name": "Google AI Blog", "url": "http://googleaiblog.blogspot.com/atom.xml", "priority": 1},
    {"name": "NVIDIA AI Blog", "url": "https://developer.nvidia.com/blog/feed", "priority": 1},
    {"name": "Microsoft Research", "url": "https://www.microsoft.com/en-us/research/feed/", "priority": 1},

    # --- AI-Focused Publications (Priority 2) ---
    {"name": "The Decoder", "url": "https://the-decoder.com/feed/", "priority": 2},
    {"name": "MarkTechPost", "url": "https://www.marktechpost.com/feed", "priority": 2},
    {"name": "Synced Review", "url": "https://syncedreview.com/feed", "priority": 2},
    {"name": "AI News", "url": "https://www.artificialintelligence-news.com/feed/rss/", "priority": 2},
    {"name": "AI Business", "url": "https://aibusiness.com/rss.xml", "priority": 2},
    {"name": "CB Insights AI", "url": "https://www.cbinsights.com/research/feed/", "priority": 2},
    {"name": "Emerj AI", "url": "https://emerj.com/feed/", "priority": 2},

    # --- Major Tech News (Priority 3) ---
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "priority": 3},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "priority": 3},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "priority": 3},
    {"name": "Wired AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss", "priority": 3},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "priority": 3},
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/", "priority": 3},
    {"name": "Bloomberg Technology", "url": "https://feeds.bloomberg.com/technology/news.rss", "priority": 3},

    # --- Newsletters & Substacks (Priority 4) ---
    {"name": "Last Week in AI", "url": "https://lastweekin.ai/feed", "priority": 4},
    {"name": "Latent Space", "url": "https://www.latent.space/feed", "priority": 4},
    {"name": "Ahead of AI", "url": "https://magazine.sebastianraschka.com/feed", "priority": 4},
    {"name": "The Gradient", "url": "https://thegradient.pub/rss/", "priority": 4},
    {"name": "AI Snake Oil", "url": "https://aisnakeoil.substack.com/feed", "priority": 4},
    {"name": "Interconnects", "url": "https://www.interconnects.ai/feed", "priority": 4},
    {"name": "SemiAnalysis", "url": "https://www.semianalysis.com/feed", "priority": 4},
    {"name": "Import AI", "url": "https://jack-clark.net/feed/", "priority": 4},
    {"name": "TheSequence", "url": "https://thesequence.substack.com/feed", "priority": 4},
    {"name": "One Useful Thing", "url": "https://www.oneusefulthing.org/feed", "priority": 4},

    # --- Developer Resources (Priority 5) ---
    {"name": "KDnuggets", "url": "https://www.kdnuggets.com/feed", "priority": 5},
    {"name": "Machine Learning Mastery", "url": "https://machinelearningmastery.com/blog/feed", "priority": 5},
    {"name": "LangChain Blog", "url": "https://blog.langchain.dev/rss/", "priority": 5},
    {"name": "Towards Data Science", "url": "https://towardsdatascience.com/feed", "priority": 5},
    {"name": "Stack Overflow Blog", "url": "https://stackoverflow.blog/feed/", "priority": 5},
    {"name": "DEV Community", "url": "https://dev.to/feed", "priority": 5},
    {"name": "Hacker Noon AI", "url": "https://hackernoon.com/tagged/ai/feed", "priority": 5},
    {"name": "Replicate Blog", "url": "https://replicate.com/blog/rss", "priority": 5},
    {"name": "Weights & Biases", "url": "https://wandb.ai/fully-connected/rss.xml", "priority": 5},

    # --- Research (Priority 5) ---
    {"name": "arXiv cs.CV", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=25", "priority": 5},
    {"name": "MIT News ML", "url": "https://news.mit.edu/topic/mitmachine-learning-rss.xml", "priority": 5},
    {"name": "Berkeley BAIR", "url": "https://bair.berkeley.edu/blog/feed.xml", "priority": 5},
    {"name": "ScienceDaily AI", "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml", "priority": 5},
    {"name": "Google Research", "url": "https://blog.research.google/feeds/posts/default?alt=rss", "priority": 5},

    # --- Other Tech (Priority 6) ---
    {"name": "IEEE Spectrum AI", "url": "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss", "priority": 6},
    {"name": "The Guardian AI", "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss", "priority": 6},
    {"name": "The Register AI", "url": "https://www.theregister.com/software/ai_ml/headlines.atom", "priority": 6},
    {"name": "SiliconANGLE AI", "url": "https://siliconangle.com/category/ai/feed", "priority": 6},
    {"name": "Crunchbase News", "url": "https://news.crunchbase.com/feed", "priority": 6},

    # --- Reddit Communities (Priority 7) ---
    {"name": "r/MachineLearning", "url": "https://www.reddit.com/r/MachineLearning/.rss", "priority": 7},
    {"name": "r/LocalLLaMA", "url": "https://www.reddit.com/r/LocalLLaMA/.rss", "priority": 7},
    {"name": "r/artificial", "url": "https://www.reddit.com/r/artificial/.rss", "priority": 7},
    {"name": "r/deeplearning", "url": "https://www.reddit.com/r/deeplearning/.rss", "priority": 7},
    {"name": "r/datascience", "url": "https://www.reddit.com/r/datascience/.rss", "priority": 7},
    {"name": "r/ChatGPT", "url": "https://www.reddit.com/r/ChatGPT/.rss", "priority": 7},

    # --- Personal Blogs (Priority 7) ---
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "priority": 7},
    {"name": "Chip Huyen", "url": "https://huyenchip.com/feed", "priority": 7},
    {"name": "Eugene Yan", "url": "https://eugeneyan.com/rss/", "priority": 7},
    {"name": "R-bloggers", "url": "https://feeds.feedburner.com/RBloggers", "priority": 7},
]

# HTML Sources (for sites without RSS)
HTML_SOURCES = [
    {
        "name": "Anthropic News",
        "url": "https://www.anthropic.com/news",
        "selectors": {
            "article_container": "article, .news-item, [data-testid='news-card']",
            "title": "h2, h3, .title",
            "link": "a",
            "date": "time, .date, [datetime]",
            "summary": "p, .description, .excerpt",
        },
        "priority": 1,
    },
]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
