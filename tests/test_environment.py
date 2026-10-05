"""Tests verifying the workspace structure, documentation files, and directories."""

from pathlib import Path


def test_directory_structure_exists():
    """Verify required top-level directories exist."""
    required_dirs = [
        Path("data/raw"),
        Path("data/processed"),
        Path("docs"),
        Path("src/copilot"),
        Path("src/copilot/db"),
        Path("src/copilot/data"),
        Path("src/copilot/models"),
        Path("src/copilot/rag"),
        Path("src/copilot/llm"),
        Path("src/copilot/agent"),
        Path("src/copilot/api"),
        Path("src/copilot/ui"),
        Path("eval"),
        Path("results"),
        Path("tests"),
    ]
    for directory in required_dirs:
        assert directory.exists(), f"Missing required directory: {directory}"
        assert directory.is_dir(), f"Path is not a directory: {directory}"


def test_documentation_files_exist():
    """Verify required documentation files exist."""
    required_docs = [
        Path("docs/architecture.md"),
        Path("docs/metric_dictionary.md"),
        Path("docs/commercial_playbook.md"),
        Path("docs/schema_reference.md"),
        Path("docs/llm_fundamentals.md"),
        Path("docs/safety.md"),
        Path("data/README.md"),
    ]
    for doc in required_docs:
        assert doc.exists(), f"Missing required documentation file: {doc}"
        assert doc.stat().st_size > 0, f"Documentation file is empty: {doc}"
