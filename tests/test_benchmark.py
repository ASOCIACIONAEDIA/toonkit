"""Tests for benchmarking functionality."""

import pytest

from toonkit.benchmark.tokenizer import TokenBenchmark, compare_formats


class TestTokenBenchmark:
    """Test token counting and benchmarking."""

    def test_benchmark_json_format(self, sample_users: list[dict]) -> None:
        """Benchmark JSON format."""
        benchmark = TokenBenchmark()
        data = {"users": sample_users}
        
        stats = benchmark.benchmark_format(data, "json", "gpt-4")
        
        assert stats.format == "json"
        assert stats.model == "gpt-4"
        assert stats.token_count > 0
        assert stats.char_count > 0
        assert stats.encoding_time_ms >= 0

    def test_benchmark_toon_format(self, sample_users: list[dict]) -> None:
        """Benchmark TOON format."""
        benchmark = TokenBenchmark()
        data = {"users": sample_users}
        
        stats = benchmark.benchmark_format(data, "toon", "gpt-4")
        
        assert stats.format == "toon"
        assert stats.token_count > 0
        assert stats.char_count > 0

    def test_compare_formats(self, sample_users: list[dict]) -> None:
        """Compare JSON vs TOON."""
        benchmark = TokenBenchmark()
        data = {"users": sample_users}
        
        result = benchmark.compare(data, "gpt-4")
        
        assert result.json_stats.token_count > result.toon_stats.token_count
        assert result.token_reduction_pct > 0
        assert result.char_reduction_pct > 0

    def test_compare_formats_multimodel(self, sample_users: list[dict]) -> None:
        """Compare across multiple models."""
        data = {"users": sample_users}
        
        results = compare_formats(data, ["gpt-4", "claude-3"])
        
        assert "gpt-4" in results
        assert "claude-3" in results
        
        for result in results.values():
            assert result.token_reduction_pct > 0

    def test_token_reduction_realistic(self) -> None:
        """Test realistic data shows expected reduction."""
        # Create typical API response
        data = {
            "products": [
                {"id": i, "name": f"Product {i}", "price": 99.99 + i, "in_stock": True}
                for i in range(20)
            ]
        }
        
        benchmark = TokenBenchmark()
        result = benchmark.compare(data, "gpt-4")
        
        # Should see 30-60% reduction for tabular data
        assert 20 < result.token_reduction_pct < 70


class TestTokenStats:
    """Test TokenStats dataclass."""

    def test_efficiency_ratio(self) -> None:
        """Efficiency ratio calculation."""
        from toonkit.benchmark.tokenizer import TokenStats
        
        stats = TokenStats(
            format="json",
            model="gpt-4",
            token_count=100,
            char_count=500,
            encoding_time_ms=10.0,
            tokens_per_char=0.2,
        )
        
        assert stats.efficiency_ratio == 0.2


class TestComparisonResult:
    """Test ComparisonResult output."""

    def test_comparison_string_output(self, sample_users: list[dict]) -> None:
        """String representation is formatted nicely."""
        benchmark = TokenBenchmark()
        result = benchmark.compare({"users": sample_users}, "gpt-4")
        
        output = str(result)
        
        assert "TOKEN COMPARISON" in output
        assert "gpt-4" in output
        assert "%" in output

