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
REQUESTS_PER_DOMAIN_PER_MINUTE = 10
DELAY_BETWEEN_REQUESTS = 1.0

# Content Settings
MAX_SUMMARY_LENGTH = 500
MAX_ARTICLES_PER_SOURCE = 50
DEDUP_SIMILARITY_THRESHOLD = 0.85

# Tagging Keywords
TAG_KEYWORDS = {
    "llm": [
        "gpt", "claude", "gemini", "llama", "mistral", "transformer",
        "language model", "chatbot", "large language", "foundation model",
        "anthropic", "openai", "deepmind", "perplexity", "copilot",
        "phi-4", "grok", "deepseek", "qwen", "command r", "cohere",
        "prompt", "token", "inference", "fine-tun", "instruct",
    ],
    "computer-vision": [
        "image recognition", "object detection", "computer vision",
        "image generation", "stable diffusion", "midjourney", "dall-e",
        "image classification", "semantic segmentation", "yolo",
        "video generation", "sora", "flux", "imagen",
    ],
    "robotics": [
        "robot", "robotics", "humanoid", "self-driving",
        "drones", "boston dynamics", "figure", "tesla bot",
        "physical intelligence", "waymo",
    ],
    "research": [
        "paper", "arxiv", "researchers", "study", "experiment", "benchmark",
        "dataset", "evaluation", "sota", "state-of-the-art", "novel approach",
        "ablation", "outperforms", "surpasses",
    ],
    "funding": [
        "raised", "funding", "series a", "series b", "series c", "series d",
        "investment", "valuation", "acquired", "acquisition", "ipo",
        "investors", "venture capital", "vc", "billion", "million round",
        "backed by", "capital", "fundraise",
    ],
    "open-source": [
        "open source", "open-source", "github", "huggingface", "weights",
        "apache license", "mit license", "gpl", "repository",
    ],
    "tutorial": [
        "how to", "guide", "tutorial", "step-by-step", "implementation",
        "walkthrough", "hands-on", "getting started", "introduction to",
        "build a", "building a", "implement", "learn to",
    ],
    "product-launch": [
        "launches", "announces", "release", "introduces", "unveil",
        "now available", "rolling out", "preview", "generally available",
        "new feature", "update", "upgrade",
    ],
    "hardware": [
        "gpu", "tpu", "chip", "nvidia", "amd", "intel", "h100", "h200",
        "a100", "b200", "compute", "data center", "server",
        "semiconductor", "silicon",
    ],
    "regulation": [
        "regulation", "policy", "legislation", "eu ai act",
        "compliance", "ethics", "safety", "bias", "fairness", "government",
        "ban", "lawsuit", "copyright", "privacy", "gdpr",
    ],
    "agents": [
        "ai agent", "agentic", "tool use", "function calling",
        "mcp", "model context protocol", "orchestration", "workflow",
        "multi-agent", "autonomous agent",
    ],
    "rag": [
        "rag", "retrieval augmented", "vector database", "embedding",
        "semantic search", "knowledge base", "chunking", "reranking",
        "pinecone", "chroma", "weaviate", "qdrant",
    ],
    "data": [
        "data pipeline", "data engineering", "etl", "data lake",
        "data warehouse", "spark", "airflow", "dbt", "snowflake",
        "databricks", "big data", "analytics", "data science",
    ],
    "finance-ai": [
        "banking", "fintech", "financial", "trading", "hedge fund",
        "credit", "insurance", "wealth management", "risk",
        "payment", "fraud detection", "algorithmic trading",
    ],
}

# Audience Mapping - tags that route to each audience
AUDIENCE_TAG_MAPPING = {
    "developers": [
        "tutorial", "open-source", "agents", "rag", "data", "llm",
    ],
    "business": [
        "funding", "product-launch",
    ],
    "finance": [
        "funding", "finance-ai",
    ],
    "research": [
        "research",
    ],
}

# Additional keyword matching for audience (beyond tags)
AUDIENCE_KEYWORDS = {
    "developers": [
        "implementation", "code", "api", "sdk", "library", "framework",
        "python", "javascript", "docker", "deploy", "debug", "cli",
        "developer", "programming", "engineering", "open source",
        "github", "npm", "pip", "rust", "typescript",
    ],
    "business": [
        "enterprise", "adoption", "roi", "case study", "deployment",
        "solution", "platform", "strategy", "market", "revenue",
        "startup", "company", "ceo", "cto", "partnership",
        "customer", "saas", "b2b", "industry",
    ],
    "finance": [
        "investment", "valuation", "ipo", "market cap", "stock",
        "revenue", "growth", "acquisition", "merger", "billion",
        "banking", "fintech", "financial", "trading", "wall street",
        "softbank", "sequoia", "a16z", "investors",
    ],
    "research": [
        "paper", "arxiv", "benchmark", "dataset", "evaluation",
        "sota", "experiment", "novel", "methodology", "ablation",
        "university", "professor", "phd", "lab",
    ],
}

# ============================================================
# ALL RSS SOURCES - 60+ verified working feeds
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

    # --- Major Tech News (Priority 3) ---
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "priority": 3},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "priority": 3},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "priority": 3},
    {"name": "Wired AI", "url": "https://www.wired.com/feed/tag/ai/latest/rss", "priority": 3},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index", "priority": 3},
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/", "priority": 3},
    {"name": "Engadget", "url": "https://www.engadget.com/rss.xml", "priority": 3},
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

    # --- Research (Priority 5) ---
    {"name": "arXiv cs.AI", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=25", "priority": 5},
    {"name": "arXiv cs.LG", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.LG&sortBy=submittedDate&sortOrder=descending&max_results=25", "priority": 5},
    {"name": "arXiv cs.CL", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=25", "priority": 5},
    {"name": "arXiv cs.CV", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.CV&sortBy=submittedDate&sortOrder=descending&max_results=25", "priority": 5},
    {"name": "MIT News ML", "url": "https://news.mit.edu/topic/mitmachine-learning-rss.xml", "priority": 5},
    {"name": "Berkeley BAIR", "url": "https://bair.berkeley.edu/blog/feed.xml", "priority": 5},
    {"name": "ScienceDaily AI", "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml", "priority": 5},

    # --- Other Tech (Priority 6) ---
    {"name": "IEEE Spectrum AI", "url": "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss", "priority": 6},
    {"name": "The Guardian AI", "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss", "priority": 6},
    {"name": "ZDNet AI", "url": "https://www.zdnet.com/topic/artificial-intelligence/rss.xml", "priority": 6},
    {"name": "The Register AI", "url": "https://www.theregister.com/software/ai_ml/headlines.atom", "priority": 6},
    {"name": "The Next Web", "url": "https://thenextweb.com/neural/feed", "priority": 6},
    {"name": "SiliconANGLE AI", "url": "https://siliconangle.com/category/ai/feed", "priority": 6},

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

    # --- Business & Finance (Priority 6) ---
    {"name": "Crunchbase News", "url": "https://news.crunchbase.com/feed", "priority": 6},
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
