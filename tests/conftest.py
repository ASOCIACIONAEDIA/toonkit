"""Pytest configuration and shared fixtures."""

from typing import Any

import pytest

from toonkit.core.types import ParserMode, ToonConfig


@pytest.fixture
def strict_config() -> ToonConfig:
    """Strict parser configuration."""
    return ToonConfig(mode=ParserMode.STRICT)


@pytest.fixture
def permissive_config() -> ToonConfig:
    """Permissive parser configuration."""
    return ToonConfig(mode=ParserMode.PERMISSIVE)


@pytest.fixture
def sample_users() -> list[dict[str, Any]]:
    """Sample user data for testing."""
    return [
        {"id": 1, "name": "Alice", "role": "admin", "active": True},
        {"id": 2, "name": "Bob", "role": "user", "active": False},
        {"id": 3, "name": "Charlie", "role": "user", "active": True},
    ]


@pytest.fixture
def sample_nested() -> dict[str, Any]:
    """Sample nested data structure."""
    return {
        "company": "ACME Corp",
        "employees": [
            {"id": 1, "name": "Alice", "salary": 75000},
            {"id": 2, "name": "Bob", "salary": 65000},
        ],
        "metadata": {
            "created": "2024-01-01",
            "version": 2,
            "tags": ["production", "verified"],
        },
    }


__all__ = ["strict_config", "permissive_config", "sample_users", "sample_nested"]

