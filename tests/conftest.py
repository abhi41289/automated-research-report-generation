"""
Pytest configuration and shared fixtures for testing the research report generation system.

This file provides:
- Mock LLM fixtures for cost-free, deterministic testing
- Sample test data (analysts, topics, etc.)
- Async event loop configuration
- Test environment setup
"""

import pytest
import asyncio
from typing import Generator
from research_and_analyst.schemas.models import Analyst


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers for organizing tests."""
    config.addinivalue_line(
        "markers", "demo: marks tests as demo tests (fast, impressive for interviews)"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (use real LLM calls)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


# ============================================================================
# ASYNC TESTING FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """
    Create an event loop for async tests.
    
    Interview Talking Point:
    "I configure a session-scoped event loop to support async/await testing
    of FastAPI endpoints and LangGraph workflows."
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# SAMPLE TEST DATA
# ============================================================================

@pytest.fixture
def sample_topic() -> str:
    """
    Standard test topic for consistent testing.
    
    Interview Talking Point:
    "I use consistent test data to ensure reproducible results and
    make it easy to compare tests across runs."
    """
    return "Impact of AI on Healthcare"


@pytest.fixture
def sample_analyst() -> Analyst:
    """
    Pre-built analyst for testing without LLM calls.
    
    Interview Talking Point:
    "Rather than generating analysts with expensive LLM calls in every test,
    I use fixtures to provide pre-built test data."
    """
    return Analyst(
        name="Dr. Sarah Chen",
        role="AI Ethics Researcher",
        affiliation="Stanford University",
        description="Expert in AI ethics, healthcare AI systems, and patient data privacy"
    )


@pytest.fixture
def sample_analysts() -> list[Analyst]:
    """
    List of 3 analysts for testing parallel workflows.
    
    Interview Talking Point:
    "This fixture simulates the multi-analyst setup we use in production,
    allowing me to test parallel interview workflows without API costs."
    """
    return [
        Analyst(
            name="Dr. Sarah Chen",
            role="AI Ethics Researcher",
            affiliation="Stanford University",
            description="Expert in AI ethics and healthcare systems"
        ),
        Analyst(
            name="Dr. Michael Torres",
            role="Healthcare Technology Specialist",
            affiliation="Mayo Clinic",
            description="20+ years implementing AI in clinical settings"
        ),
        Analyst(
            name="Dr. Amara Okafor",
            role="Health Policy Analyst",
            affiliation="WHO",
            description="Focus on global health AI regulation and equity"
        )
    ]


# ============================================================================
# MOCK LLM FIXTURES
# ============================================================================

@pytest.fixture
def mock_analyst_response() -> dict:
    """
    Mock LLM response for analyst generation (structured output).
    
    Interview Talking Point:
    "I mock LLM structured outputs to test schema validation without
    consuming API tokens. This validates my Pydantic models work correctly."
    """
    return {
        "analysts": [
            {
                "name": "Dr. Test Analyst",
                "role": "Test Specialist",
                "affiliation": "Test University",
                "description": "Expert in testing LLM systems"
            }
        ]
    }


@pytest.fixture
def mock_search_results() -> list[dict]:
    """
    Mock Tavily search results for testing without API calls.
    
    Interview Talking Point:
    "I mock external API calls (like Tavily) to keep tests fast and independent
    of external services. This prevents flaky tests due to network issues."
    """
    return [
        {
            "title": "AI in Healthcare: A Comprehensive Review",
            "url": "https://example.com/ai-healthcare-review",
            "content": "AI is transforming healthcare through diagnostic tools, personalized medicine, and operational efficiency.",
            "score": 0.98
        },
        {
            "title": "Ethical Considerations for Medical AI",
            "url": "https://example.com/medical-ai-ethics",
            "content": "Key ethical concerns include patient privacy, algorithmic bias, and clinical validation requirements.",
            "score": 0.95
        }
    ]


# ============================================================================
# TEST ENVIRONMENT CONFIGURATION
# ============================================================================

@pytest.fixture(scope="session")
def test_config() -> dict:
    """
    Test environment configuration.
    
    Interview Talking Point:
    "I isolate test configuration from production to prevent accidentally
    calling real APIs or modifying production data during testing."
    """
    return {
        "TEST_MODE": True,
        "USE_MOCK_LLM": True,
        "MOCK_TAVILY_SEARCH": True,
        "MAX_ANALYSTS": 2,  # Smaller for faster tests
        "MAX_INTERVIEW_TURNS": 1  # Fewer turns for speed
    }
