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
        "anthropic", "openai", "deepmind"
    ],
    "computer-vision": [
        "image recognition", "object detection", "computer vision",
        "image generation", "stable diffusion", "midjourney", "dall-e",
        "image classification", "semantic segmentation", "yolo"
    ],
    "robotics": [
        "robot", "robotics", "humanoid", "automation", "autonomous",
        "self-driving", "drones", "boston dynamics", "figure", "tesla bot"
    ],
    "research": [
        "paper", "arxiv", "research", "study", "experiment", "benchmark",
        "dataset", "evaluation", "sota", "state-of-the-art", "novel"
    ],
    "funding": [
        "raised", "funding", "series a", "series b", "series c", "series d",
        "investment", "valuation", "acquired", "acquisition", "ipo",
        "investors", "venture capital", "vc"
    ],
    "open-source": [
        "open source", "open-source", "github", "huggingface", "weights",
        "apache", "mit license", "gpl", "repository", "release"
    ],
    "tutorial": [
        "how to", "guide", "tutorial", "step-by-step", "implementation",
        "walkthrough", "hands-on", "getting started", "introduction"
    ],
    "product-launch": [
        "launch", "announce", "release", "introduces", "unveil",
        "now available", "rolling out", "beta", "preview", "ga"
    ],
    "hardware": [
        "gpu", "tpu", "chip", "nvidia", "amd", "intel", "h100", "a100",
        "inference", "training", "compute", "data center", "server"
    ],
    "regulation": [
        "regulation", "policy", "law", "legislation", "eu ai act",
        "compliance", "ethics", "safety", "bias", "fairness", "government"
    ],
    "agents": [
        "agent", "agentic", "tool use", "function calling", "autonomous",
        "mcp", "model context protocol", "orchestration", "workflow"
    ],
    "rag": [
        "rag", "retrieval", "vector", "embedding", "semantic search",
        "knowledge base", "chunking", "reranking", "context window"
    ],
}

# Audience Mapping
AUDIENCE_TAG_MAPPING = {
    "developers": [
        "tutorial", "open-source", "agents", "rag",
    ],
    "business": [
        "funding", "product-launch",
    ],
    "finance": [
        "funding",
    ],
    "research": [
        "research",
    ],
}

AUDIENCE_KEYWORDS = {
    "developers": [
        "implementation", "code", "api", "sdk", "library", "framework",
        "python", "javascript", "docker", "deploy", "debug", "cli",
    ],
    "business": [
        "enterprise", "adoption", "roi", "case study", "deployment",
        "solution", "platform", "strategy", "market", "revenue",
    ],
    "finance": [
        "investment", "valuation", "ipo", "market", "stock",
        "revenue", "growth", "acquisition", "merger", "billion",
    ],
    "research": [
        "paper", "arxiv", "benchmark", "dataset", "evaluation",
        "sota", "experiment", "novel", "methodology", "ablation",
    ],
}

# RSS Sources - 19 priority feeds
RSS_SOURCES = [
    {"name": "HuggingFace Blog", "url": "https://huggingface.co/blog/feed.xml", "priority": 1},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss/", "priority": 1},
    {"name": "DeepMind Blog", "url": "https://deepmind.com/blog/feed/basic/", "priority": 1},
    {"name": "The Decoder", "url": "https://the-decoder.com/feed/", "priority": 2},
    {"name": "MarkTechPost", "url": "https://www.marktechpost.com/feed", "priority": 2},
    {"name": "Unite AI", "url": "https://www.unite.ai/feed/", "priority": 2},
    {"name": "Synced Review", "url": "https://syncedreview.com/feed", "priority": 2},
    {"name": "AI News", "url": "https://www.artificialintelligence-news.com/feed/rss/", "priority": 2},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "priority": 3},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "priority": 3},
    {"name": "Last Week in AI", "url": "https://lastweekin.ai/feed", "priority": 4},
    {"name": "Latent Space", "url": "https://www.latent.space/feed", "priority": 4},
    {"name": "Ahead of AI", "url": "https://magazine.sebastianraschka.com/feed", "priority": 4},
    {"name": "KDnuggets", "url": "https://www.kdnuggets.com/feed", "priority": 5},
    {"name": "Machine Learning Mastery", "url": "https://machinelearningmastery.com/blog/feed", "priority": 5},
    {"name": "LangChain Blog", "url": "https://blog.langchain.dev/rss/", "priority": 5},
    {"name": "arXiv cs.AI", "url": "https://arxiv.org/rss/cs.AI", "priority": 6},
    {"name": "arXiv cs.LG", "url": "https://arxiv.org/rss/cs.LG", "priority": 6},
    {"name": "Crunchbase News", "url": "https://news.crunchbase.com/feed", "priority": 7},
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
