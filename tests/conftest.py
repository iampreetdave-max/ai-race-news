"""
Test fixtures for AI Pulse
"""
import pytest
import tempfile
from pathlib import Path

from scraper.database import Database
from scraper.models import Article


@pytest.fixture
def tmp_db():
    """Create a temporary database for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = Database(db_path=db_path)
        yield db


@pytest.fixture
def sample_article():
    """Create a sample article for testing."""
    return Article(
        title="OpenAI Releases GPT-5 with Breakthrough Reasoning",
        url="https://example.com/gpt5-release",
        summary="OpenAI has released GPT-5, featuring significant improvements in reasoning and code generation.",
        source_name="TechCrunch",
        author="John Doe",
    )


@pytest.fixture
def sample_articles():
    """Create multiple sample articles for testing."""
    return [
        Article(
            title="OpenAI Releases GPT-5 with Breakthrough Reasoning",
            url="https://example.com/gpt5-release",
            summary="OpenAI has released GPT-5 with major reasoning improvements.",
            source_name="TechCrunch",
        ),
        Article(
            title="Anthropic Raises $5B in Series D Funding",
            url="https://example.com/anthropic-funding",
            summary="Anthropic has raised $5 billion in Series D funding led by investors.",
            source_name="Crunchbase News",
        ),
        Article(
            title="How to Build a RAG Pipeline with LangChain",
            url="https://example.com/rag-tutorial",
            summary="Step-by-step guide to building a RAG pipeline using LangChain and vector embeddings.",
            source_name="LangChain Blog",
        ),
        Article(
            title="New Computer Vision Model Achieves SOTA on ImageNet",
            url="https://example.com/cv-sota",
            summary="Researchers publish paper on arxiv showing state-of-the-art image classification results.",
            source_name="arXiv cs.CV",
        ),
        Article(
            title="NVIDIA H200 GPU Benchmarks Show 2x Inference Speed",
            url="https://example.com/h200-benchmarks",
            summary="NVIDIA's new H200 GPU delivers 2x faster inference for large language models.",
            source_name="NVIDIA AI Blog",
        ),
    ]
