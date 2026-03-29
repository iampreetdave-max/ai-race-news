"""
AI Pulse Tagger - 2-tier audience scoring with AI/Data/ML relevance gate
"""
import logging
import re
from typing import Optional

from .models import Article

logger = logging.getLogger(__name__)

# ============================================================
# RELEVANCE GATE - Article must be about AI, Data, or ML
# ============================================================
RELEVANCE_KEYWORDS = [
    # AI core
    " ai ", " ai-", "artificial intelligence", "machine learning", "deep learning",
    "neural net", "llm", "gpt", "claude", "gemini", "chatbot", "generative",
    "nlp", "language model", "computer vision", "transformer",
    "diffusion", "training data", "fine-tun", "reinforcement learning",
    "embedding", "tokeniz", "prompt", "retrieval augment", "vector database",
    "ai agent", "openai", "anthropic", "deepmind", "hugging face", "huggingface",
    "mistral", "llama", "deepseek", "copilot", "midjourney", "stable diffusion",
    "chatgpt", "ai model", "ai tool", "ai-powered", "ai system",
    "benchmark", "inference", "foundation model",
    "robotics", "humanoid", "self-driving", "autonomous vehicle",
    # Data
    "data pipeline", "data engineering", "data warehouse", "data lake",
    "etl", "analytics", "business intelligence", "big data",
    "spark", "airflow", "dbt", "snowflake", "databricks",
    "data science", "data analyst", "data-driven",
    "database", "sql", "nosql", "postgresql", "mongodb",
    # ML/Tech
    "algorithm", "dataset", "gpu", "nvidia", "tpu",
    "cloud computing", "aws", "azure", "gcp",
    "model training", "model deploy", "mlops",
    "api", "sdk", "saas", "devops", "kubernetes",
]

# Sources that are always relevant (AI/Data/ML focused)
TRUSTED_SOURCES = {
    "HuggingFace Blog", "OpenAI Blog", "DeepMind Blog", "The Decoder",
    "MarkTechPost", "AI News", "Synced Review",
    "arXiv cs.AI", "arXiv cs.LG", "arXiv cs.CL", "arXiv cs.CV",
    "LangChain Blog", "KDnuggets", "Machine Learning Mastery",
    "Ahead of AI", "Latent Space", "Last Week in AI",
    "r/MachineLearning", "r/LocalLLaMA", "r/deeplearning",
    "Berkeley BAIR", "MIT News ML", "ScienceDaily AI",
    "AI Snake Oil", "Interconnects", "SemiAnalysis", "TheSequence",
    "Wired AI", "VentureBeat AI", "Google AI Blog", "NVIDIA AI Blog",
    "Replicate Blog", "Import AI", "One Useful Thing", "The Gradient",
    "Towards Data Science", "AI Business", "CB Insights AI", "Emerj AI",
    "Weights & Biases", "Chip Huyen", "Eugene Yan", "Simon Willison",
    "IEEE Spectrum AI", "R-bloggers",
}

# ============================================================
# AUDIENCE SCORING - 2 tiers per audience
# Tier 1 (strong signal): 1 match = definitely this audience
# Tier 2 (weak signal): need 3+ matches
# ============================================================

# --- DEVELOPERS ---
DEV_TIER1 = [
    "code generation", "coding model", "coding assistant", "humaneval",
    "copilot", "cursor", "claude code", "codex", "code interpreter",
    "developer tool", "open-source model", "model weights",
    "fine-tuning guide", "fine-tune", "langchain", "llamaindex",
    "function calling", "tool use", "mcp server", "agent framework",
    "context window", "inference speed", "swe-bench", "coding benchmark",
    "api release", "sdk release", "new framework", "developer preview",
    "open source release", "data pipeline", "data engineering",
    "etl", "mlops", "devops", "kubernetes", "docker",
    "python library", "npm package", "rust crate",
]
DEV_TIER2 = [
    "python", "javascript", "typescript", "rust", "api", "sdk",
    "framework", "library", "open source", "benchmark", "deploy",
    "cli", "implementation", "tutorial", "build", "code",
    "training", "inference", "model", "gpu", "developer",
    "engineering", "github", "database", "sql",
]

# --- BUSINESS ---
BIZ_TIER1 = [
    "enterprise ai", "ai adoption", "ai strategy", "business intelligence",
    "workflow automation", "ai productivity", "ai workforce",
    "digital transformation", "ai customer service", "ai operations",
    "competitive advantage", "ai market size", "ai industry report",
    "business use case", "enterprise deployment", "ai roi",
    "ai platform", "ai solution", "data analytics platform",
    "business analytics", "data-driven decision",
]
BIZ_TIER2 = [
    "enterprise", "adoption", "startup", "partnership", "partner",
    "market", "industry", "customer", "revenue", "growth",
    "launch", "efficiency", "workforce", "company",
    "deploy", "solution", "platform", "service", "product",
    "business", "strategy", "competitive",
]

# --- FINANCE ---
FIN_TIER1 = [
    "funding round", "series a", "series b", "series c", "series d",
    "ipo", "valuation", "venture capital", "wall street",
    "goldman sachs", "jpmorgan", "morgan stanley",
    "hedge fund", "algorithmic trading", "ai trading",
    "stock price", "market cap", "quarterly earnings",
    "acquisition of", "acquired by", "merger",
    "ai in banking", "ai in finance", "fintech",
]
FIN_TIER2 = [
    "billion", "million", "investor", "capital", "revenue",
    "funding", "investment", "raised", "profit", "shares",
]

# --- RESEARCH ---
RES_TIER1 = [
    "arxiv", "state-of-the-art", "sota", "novel approach",
    "outperforms", "surpasses", "ablation study", "peer-reviewed",
    "research paper", "new architecture", "benchmark results",
    "mmlu", "gpqa", "evaluation results",
    "researchers found", "researchers show", "researchers demonstrate",
]
RES_TIER2 = [
    "researchers", "paper", "experiment", "dataset",
    "evaluation", "university", "study", "methodology",
    "scientific", "academic", "laboratory",
]

# ============================================================
# TAG KEYWORDS (for topic tags, separate from audience)
# ============================================================
TAG_KEYWORDS = {
    "llm": [
        "gpt", "claude", "gemini", "llama", "mistral", "transformer",
        "language model", "chatbot", "large language", "foundation model",
        "anthropic", "openai", "deepmind", "perplexity", "copilot",
        "grok", "deepseek", "qwen", "cohere",
    ],
    "computer-vision": [
        "image recognition", "object detection", "computer vision",
        "image generation", "stable diffusion", "midjourney", "dall-e",
        "video generation", "sora", "flux", "imagen",
    ],
    "robotics": [
        "robotics", "humanoid", "self-driving",
        "boston dynamics", "figure ai", "tesla bot",
        "physical intelligence", "waymo", "robotic",
    ],
    "research": [
        "arxiv", "researchers found", "state-of-the-art",
        "novel approach", "outperforms", "surpasses", "ablation",
    ],
    "funding": [
        "funding round", "series a", "series b", "series c",
        "valuation", "venture capital", "fundraising", "ipo",
    ],
    "open-source": [
        "open source", "open-source", "huggingface", "model weights",
        "apache license", "mit license",
    ],
    "tutorial": [
        "how to build", "how to create", "how to implement",
        "step-by-step", "tutorial", "walkthrough", "hands-on guide",
        "getting started with", "introduction to",
    ],
    "product-launch": [
        "launches", "announces", "introduces", "unveils",
        "generally available", "new feature",
    ],
    "hardware": [
        "gpu", "tpu", "nvidia", "h100", "h200",
        "a100", "b200", "data center", "semiconductor",
    ],
    "regulation": [
        "ai regulation", "eu ai act", "ai policy",
        "ai ethics", "ai safety", "ai governance", "ai ban",
    ],
    "agents": [
        "ai agent", "agentic", "tool use", "function calling",
        "model context protocol", "multi-agent",
    ],
    "rag": [
        "retrieval augmented", "vector database", "embedding model",
        "semantic search", "knowledge base", "chunking",
        "pinecone", "chroma", "weaviate", "qdrant",
    ],
    "data": [
        "data pipeline", "data engineering", "etl",
        "data warehouse", "spark", "airflow", "databricks",
        "data science", "analytics", "big data",
    ],
    "finance-ai": [
        "ai in banking", "ai in finance", "fintech ai",
        "algorithmic trading", "fraud detection",
    ],
}


class Tagger:
    """Tags articles with topics and scores audience relevance."""

    def __init__(self):
        self._compile_tag_patterns()

    def _compile_tag_patterns(self):
        self.tag_patterns = {}
        for tag, keywords in TAG_KEYWORDS.items():
            patterns = []
            for kw in keywords:
                patterns.append(re.compile(re.escape(kw), re.IGNORECASE))
            self.tag_patterns[tag] = patterns

    def is_relevant(self, article: Article) -> bool:
        """Check if article is about AI, Data, or ML."""
        if article.source_name in TRUSTED_SOURCES:
            return True
        text = f" {article.title} {article.summary or ''} ".lower()
        return any(kw in text for kw in RELEVANCE_KEYWORDS)

    def tag_article(self, article: Article) -> Article:
        """Assign topic tags and audience scores."""
        text = f"{article.title} {article.summary or ''}"
        text_lower = text.lower()

        # Topic tags
        tags = set()
        for tag, patterns in self.tag_patterns.items():
            for p in patterns:
                if p.search(text):
                    tags.add(tag)
                    break
        article.tags = list(tags)

        # Audience scoring
        audiences = set()

        def count_matches(text_val, phrases):
            found = []
            for p in phrases:
                if re.search(re.escape(p), text_val, re.IGNORECASE):
                    found.append(p)
            return found

        # Developers
        t1 = count_matches(text, DEV_TIER1)
        t2 = count_matches(text, DEV_TIER2)
        if t1 or len(t2) >= 3:
            audiences.add("developers")

        # Business
        t1 = count_matches(text, BIZ_TIER1)
        t2 = count_matches(text, BIZ_TIER2)
        if t1 or len(t2) >= 3:
            audiences.add("business")

        # Finance
        t1 = count_matches(text, FIN_TIER1)
        t2 = count_matches(text, FIN_TIER2)
        if t1 or len(t2) >= 3:
            audiences.add("finance")

        # Research
        t1 = count_matches(text, RES_TIER1)
        t2 = count_matches(text, RES_TIER2)
        if t1 or len(t2) >= 3:
            audiences.add("research")

        if not audiences:
            audiences.add("general")

        article.audiences = list(audiences)
        return article

    def tag_articles(self, articles: list[Article]) -> list[Article]:
        """Tag articles, filtering out irrelevant ones."""
        relevant = []
        filtered = 0

        for article in articles:
            if not self.is_relevant(article):
                filtered += 1
                continue
            self.tag_article(article)
            relevant.append(article)

        tag_counts = {}
        for a in relevant:
            for t in a.tags:
                tag_counts[t] = tag_counts.get(t, 0) + 1

        top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:5]
        logger.info(
            f"Tagged {len(relevant)} articles ({filtered} filtered as irrelevant). "
            f"Top tags: {top_tags}"
        )
        return relevant


def tag_articles(articles: list[Article]) -> list[Article]:
    tagger = Tagger()
    return tagger.tag_articles(articles)


def get_tag_statistics(articles: list[Article]) -> dict:
    tag_counts = {}
    audience_counts = {}
    for article in articles:
        for tag in article.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        for audience in article.audiences:
            audience_counts[audience] = audience_counts.get(audience, 0) + 1
    return {
        "total_articles": len(articles),
        "tag_counts": dict(sorted(tag_counts.items(), key=lambda x: -x[1])),
        "audience_counts": dict(sorted(audience_counts.items(), key=lambda x: -x[1])),
        "articles_without_tags": sum(1 for a in articles if not a.tags),
        "avg_tags_per_article": (
            sum(len(a.tags) for a in articles) / len(articles) if articles else 0
        ),
    }
