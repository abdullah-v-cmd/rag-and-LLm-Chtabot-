"""
Test configuration.
"""
import pytest
import os
from pathlib import Path


@pytest.fixture(scope="session")
def test_data_dir():
    """Create and return test data directory."""
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    yield test_dir
    # Cleanup after tests
    import shutil
    if test_dir.exists():
        shutil.rmtree(test_dir)


@pytest.fixture
def sample_text_file(test_data_dir):
    """Create a sample text file for testing."""
    file_path = test_data_dir / "sample.txt"
    content = "This is a test document for RAG system testing."
    file_path.write_text(content)
    return file_path
