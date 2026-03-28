"""
AI PULSE NEWS SCRAPER - 110+ AI/ML/Data Sources
Complete catalog of all sources organized by category.
Use this to expand RSS_SOURCES and HTML_SOURCES in scraper/config.py.
"""

SOURCES = {
    "official_blogs": [
        {"name": "OpenAI Blog", "url": "https://openai.com/blog", "rss": "https://openai.com/blog/rss/", "type": "rss"},
        {"name": "Google AI Blog", "url": "https://ai.googleblog.com/", "rss": "http://googleaiblog.blogspot.com/atom.xml", "type": "rss"},
        {"name": "DeepMind Blog", "url": "https://deepmind.com/blog", "rss": "https://deepmind.com/blog/feed/basic/", "type": "rss"},
        {"name": "Anthropic News", "url": "https://www.anthropic.com/news", "type": "html"},
        {"name": "Meta AI Blog", "url": "https://ai.meta.com/blog/", "type": "html"},
        {"name": "HuggingFace Blog", "url": "https://huggingface.co/blog", "rss": "https://huggingface.co/blog/feed.xml", "type": "rss"},
        {"name": "NVIDIA AI Blog", "url": "https://developer.nvidia.com/blog", "rss": "https://developer.nvidia.com/blog/feed", "type": "rss"},
        {"name": "Microsoft Research", "url": "https://www.microsoft.com/en-us/research/", "rss": "https://www.microsoft.com/en-us/research/feed/", "type": "rss"},
        {"name": "Stability AI", "url": "https://stability.ai/blog", "rss": "https://stability.ai/blog?format=rss", "type": "rss"},
        {"name": "Cohere Blog", "url": "https://txt.cohere.ai/", "rss": "https://txt.cohere.ai/rss/", "type": "rss"},
        {"name": "Mistral AI Blog", "url": "https://mistral.ai/news/", "type": "html"},
    ],
    "ai_publications": [
        {"name": "The Decoder", "rss": "https://the-decoder.com/feed/", "type": "rss"},
        {"name": "MarkTechPost", "rss": "https://www.marktechpost.com/feed", "type": "rss"},
        {"name": "Unite AI", "rss": "https://www.unite.ai/feed/", "type": "rss"},
        {"name": "AI Business", "rss": "https://aibusiness.com/rss.xml", "type": "rss"},
        {"name": "AI News", "rss": "https://www.artificialintelligence-news.com/feed/rss/", "type": "rss"},
        {"name": "Synced Review", "rss": "https://syncedreview.com/feed", "type": "rss"},
        {"name": "Analytics India Magazine", "rss": "https://analyticsindiamag.com/feed/", "type": "rss"},
        {"name": "AIhub", "rss": "https://aihub.org/feed?cat=-473", "type": "rss"},
    ],
    "tech_news": [
        {"name": "TechCrunch", "rss": "https://techcrunch.com/feed/", "type": "rss"},
        {"name": "VentureBeat AI", "rss": "https://venturebeat.com/category/ai/feed/", "type": "rss"},
        {"name": "Wired AI", "rss": "https://www.wired.com/feed/tag/ai/latest/rss", "type": "rss"},
        {"name": "The Verge", "rss": "https://www.theverge.com/rss/index.xml", "type": "rss"},
        {"name": "Ars Technica", "rss": "https://feeds.arstechnica.com/arstechnica/index", "type": "rss"},
        {"name": "MIT Technology Review", "rss": "https://www.technologyreview.com/feed/", "type": "rss"},
        {"name": "IEEE Spectrum AI", "rss": "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss", "type": "rss"},
        {"name": "The Guardian AI", "rss": "https://www.theguardian.com/technology/artificialintelligenceai/rss", "type": "rss"},
        {"name": "ZDNet AI", "rss": "https://www.zdnet.com/topic/artificial-intelligence/rss.xml", "type": "rss"},
        {"name": "The Register AI", "rss": "https://www.theregister.com/software/ai_ml/headlines.atom", "type": "rss"},
        {"name": "Engadget", "rss": "https://www.engadget.com/rss.xml", "type": "rss"},
        {"name": "Gizmodo", "rss": "https://gizmodo.com/rss", "type": "rss"},
        {"name": "The Next Web", "rss": "https://thenextweb.com/neural/feed", "type": "rss"},
        {"name": "TechMonitor", "rss": "https://techmonitor.ai/feed", "type": "rss"},
        {"name": "SiliconANGLE AI", "rss": "https://siliconangle.com/category/ai/feed", "type": "rss"},
        {"name": "Silicon Republic", "rss": "https://www.siliconrepublic.com/feed", "type": "rss"},
    ],
    "research": [
        {"name": "arXiv cs.AI", "rss": "https://arxiv.org/rss/cs.AI", "type": "rss"},
        {"name": "arXiv cs.LG", "rss": "https://arxiv.org/rss/cs.LG", "type": "rss"},
        {"name": "arXiv cs.CL", "rss": "https://arxiv.org/rss/cs.CL", "type": "rss"},
        {"name": "arXiv cs.CV", "rss": "https://arxiv.org/rss/cs.CV", "type": "rss"},
        {"name": "arXiv stat.ML", "rss": "https://arxiv.org/rss/stat.ML", "type": "rss"},
        {"name": "MIT News ML", "rss": "https://news.mit.edu/topic/mitmachine-learning-rss.xml", "type": "rss"},
        {"name": "Berkeley BAIR", "rss": "https://bair.berkeley.edu/blog/feed.xml", "type": "rss"},
        {"name": "Stanford CRFM", "rss": "https://crfm.stanford.edu/feed", "type": "rss"},
        {"name": "CMU ML Blog", "rss": "https://blog.ml.cmu.edu/feed", "type": "rss"},
        {"name": "EleutherAI Blog", "rss": "https://blog.eleuther.ai/index.xml", "type": "rss"},
        {"name": "Nature Machine Learning", "rss": "https://www.nature.com/subjects/machine-learning.rss", "type": "rss"},
        {"name": "ScienceDaily AI", "rss": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml", "type": "rss"},
    ],
    "newsletters": [
        {"name": "Ahead of AI", "rss": "https://magazine.sebastianraschka.com/feed", "type": "rss"},
        {"name": "Latent Space", "rss": "https://www.latent.space/feed", "type": "rss"},
        {"name": "The Gradient", "rss": "https://thegradient.pub/rss/", "type": "rss"},
        {"name": "AI Snake Oil", "rss": "https://aisnakeoil.substack.com/feed", "type": "rss"},
        {"name": "Interconnects", "rss": "https://www.interconnects.ai/feed", "type": "rss"},
        {"name": "The Algorithmic Bridge", "rss": "https://thealgorithmicbridge.substack.com/feed", "type": "rss"},
        {"name": "SemiAnalysis", "rss": "https://www.semianalysis.com/feed", "type": "rss"},
        {"name": "Last Week in AI", "rss": "https://lastweekin.ai/feed", "type": "rss"},
        {"name": "The Rundown AI", "rss": "https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml", "type": "rss"},
        {"name": "Data Machina", "rss": "https://datamachina.substack.com/feed", "type": "rss"},
        {"name": "TheSequence", "rss": "https://thesequence.substack.com/feed", "type": "rss"},
        {"name": "One Useful Thing", "rss": "https://www.oneusefulthing.org/feed", "type": "rss"},
        {"name": "Import AI", "rss": "https://jack-clark.net/feed/", "type": "rss"},
    ],
    "developer": [
        {"name": "KDnuggets", "rss": "https://www.kdnuggets.com/feed", "type": "rss"},
        {"name": "Machine Learning Mastery", "rss": "https://machinelearningmastery.com/blog/feed", "type": "rss"},
        {"name": "Towards Data Science", "rss": "https://towardsdatascience.com/feed", "type": "rss"},
        {"name": "PyImageSearch", "rss": "https://pyimagesearch.com/blog/feed", "type": "rss"},
        {"name": "neptune.ai Blog", "rss": "https://neptune.ai/blog/feed", "type": "rss"},
        {"name": "LangChain Blog", "rss": "https://blog.langchain.dev/rss/", "type": "rss"},
        {"name": "Weights & Biases", "rss": "https://wandb.ai/fully-connected/rss.xml", "type": "rss"},
        {"name": "Replicate Blog", "rss": "https://replicate.com/blog/rss", "type": "rss"},
        {"name": "Databricks Blog", "rss": "https://www.databricks.com/feed", "type": "rss"},
        {"name": "Stack Overflow Blog", "rss": "https://stackoverflow.blog/feed/", "type": "rss"},
        {"name": "DEV Community", "rss": "https://dev.to/feed", "type": "rss"},
        {"name": "Hacker Noon AI", "rss": "https://hackernoon.com/tagged/ai/feed", "type": "rss"},
        {"name": "InfoQ AI", "rss": "https://feed.infoq.com/ai-ml-data-eng/", "type": "rss"},
        {"name": "TensorFlow Blog", "rss": "https://blog.tensorflow.org/feeds/posts/default?alt=rss", "type": "rss"},
        {"name": "AssemblyAI Blog", "rss": "https://www.assemblyai.com/blog/rss/", "type": "rss"},
    ],
    "community": [
        {"name": "r/MachineLearning", "rss": "https://www.reddit.com/r/MachineLearning/.rss", "type": "rss"},
        {"name": "r/artificial", "rss": "https://www.reddit.com/r/artificial/.rss", "type": "rss"},
        {"name": "r/deeplearning", "rss": "https://www.reddit.com/r/deeplearning/.rss", "type": "rss"},
        {"name": "r/datascience", "rss": "https://www.reddit.com/r/datascience/.rss", "type": "rss"},
        {"name": "r/LocalLLaMA", "rss": "https://www.reddit.com/r/LocalLLaMA/.rss", "type": "rss"},
        {"name": "r/ChatGPT", "rss": "https://www.reddit.com/r/ChatGPT/.rss", "type": "rss"},
        {"name": "r/StableDiffusion", "rss": "https://www.reddit.com/r/StableDiffusion/.rss", "type": "rss"},
        {"name": "r/LanguageTechnology", "rss": "https://www.reddit.com/r/LanguageTechnology/.rss", "type": "rss"},
        {"name": "r/computervision", "rss": "https://www.reddit.com/r/computervision/.rss", "type": "rss"},
        {"name": "r/MLNews", "rss": "https://www.reddit.com/r/machinelearningnews/.rss", "type": "rss"},
    ],
    "personal_blogs": [
        {"name": "Simon Willison", "rss": "https://simonwillison.net/atom/everything/", "type": "rss"},
        {"name": "Chip Huyen", "rss": "https://huyenchip.com/feed", "type": "rss"},
        {"name": "Eugene Yan", "rss": "https://eugeneyan.com/rss/", "type": "rss"},
        {"name": "Nicholas Carlini", "rss": "https://nicholas.carlini.com/writing/feed.xml", "type": "rss"},
        {"name": "Max Woolf", "rss": "https://minimaxir.com/post/index.xml", "type": "rss"},
        {"name": "Phil Schmid", "rss": "https://www.philschmid.de/feed.xml", "type": "rss"},
        {"name": "Eric Hartford", "rss": "https://erichartford.com/rss.xml", "type": "rss"},
    ],
    "business_finance": [
        {"name": "Crunchbase News", "rss": "https://news.crunchbase.com/feed", "type": "rss"},
        {"name": "Bloomberg Technology", "rss": "https://feeds.bloomberg.com/technology/news.rss", "type": "rss"},
        {"name": "Reuters Tech", "rss": "https://www.reutersagency.com/feed/?best-topics=tech", "type": "rss"},
        {"name": "Business Insider", "rss": "https://feeds.businessinsider.com/custom/all", "type": "rss"},
        {"name": "The Information", "rss": "https://www.theinformation.com/feed", "type": "rss"},
        {"name": "Sifted EU", "rss": "https://sifted.eu/feed/?post_type=article", "type": "rss"},
        {"name": "Tech.eu", "rss": "https://tech.eu/category/deep-tech/feed", "type": "rss"},
        {"name": "The Stack", "rss": "https://www.thestack.technology/latest/rss/", "type": "rss"},
    ],
    "data": [
        {"name": "Datanami", "rss": "https://www.datanami.com/feed/", "type": "rss"},
        {"name": "insideBIGDATA", "rss": "https://insidebigdata.com/feed", "type": "rss"},
        {"name": "Datafloq", "rss": "https://datafloq.com/feed/?post_type=post", "type": "rss"},
        {"name": "Gradient Flow", "rss": "https://gradientflow.com/feed/", "type": "rss"},
        {"name": "R-bloggers", "rss": "https://feeds.feedburner.com/RBloggers", "type": "rss"},
        {"name": "Python Insider", "rss": "https://feeds.feedburner.com/PythonInsider", "type": "rss"},
    ],
}


def get_all_rss_sources() -> list[dict]:
    """Get all RSS sources as a flat list ready for the scraper."""
    all_sources = []
    priority_map = {
        "official_blogs": 1,
        "ai_publications": 2,
        "tech_news": 3,
        "research": 4,
        "newsletters": 4,
        "developer": 5,
        "community": 6,
        "personal_blogs": 6,
        "business_finance": 3,
        "data": 5,
    }
    for category, sources in SOURCES.items():
        priority = priority_map.get(category, 5)
        for source in sources:
            if source["type"] == "rss":
                rss_url = source.get("rss", source.get("url"))
                if rss_url:
                    all_sources.append({
                        "name": source["name"],
                        "url": rss_url,
                        "priority": priority,
                        "category": category,
                    })
    return all_sources


def count_sources():
    total = 0
    for category, sources in SOURCES.items():
        count = len(sources)
        total += count
        print(f"{category}: {count} sources")
    print(f"\nTOTAL: {total} sources")
    rss_sources = get_all_rss_sources()
    print(f"RSS sources: {len(rss_sources)}")
    return total


if __name__ == "__main__":
    count_sources()
