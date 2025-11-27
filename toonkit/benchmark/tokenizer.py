"""Multi-model tokenization benchmarks for JSON vs TOON comparison."""

import json
import time
from dataclasses import dataclass
from typing import Any, Literal

import tiktoken

from toonkit.core.encoder import encode
from toonkit.core.types import ToonConfig

# Model-specific tokenizers
ModelName = Literal["gpt-4", "gpt-3.5-turbo", "claude-3", "claude-2", "gemini-pro"]


@dataclass
class TokenStats:
    """Token statistics for a format."""

    format: str
    model: str
    token_count: int
    char_count: int
    encoding_time_ms: float
    tokens_per_char: float

    @property
    def efficiency_ratio(self) -> float:
        """Tokens per character (lower is better)."""
        return self.token_count / max(self.char_count, 1)


@dataclass
class ComparisonResult:
    """Comparison results between JSON and TOON."""

    json_stats: TokenStats
    toon_stats: TokenStats
    token_reduction_pct: float
    char_reduction_pct: float
    speedup: float

    def __str__(self) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════╗
║  TOKEN COMPARISON: JSON vs TOON ({self.json_stats.model})
╠══════════════════════════════════════════════════════════════╣
║  Format   │ Tokens │ Chars │ Time (ms) │ Tokens/Char       ║
║───────────┼────────┼───────┼───────────┼───────────────────║
║  JSON     │ {self.json_stats.token_count:6} │ {self.json_stats.char_count:5} │ {self.json_stats.encoding_time_ms:9.2f} │ {self.json_stats.efficiency_ratio:.4f}          ║
║  TOON     │ {self.toon_stats.token_count:6} │ {self.toon_stats.char_count:5} │ {self.toon_stats.encoding_time_ms:9.2f} │ {self.toon_stats.efficiency_ratio:.4f}          ║
╠══════════════════════════════════════════════════════════════╣
║  Token Reduction:  {self.token_reduction_pct:5.1f}% 🚀                               ║
║  Char Reduction:   {self.char_reduction_pct:5.1f}%                                   ║
║  Speedup:          {self.speedup:.2f}x                                     ║
╚══════════════════════════════════════════════════════════════╝
        """.strip()


class TokenBenchmark:
    """Multi-model tokenization benchmark suite."""

    def __init__(self, config: ToonConfig | None = None):
        self.config = config or ToonConfig()
        self._tokenizers: dict[str, Any] = {}

    def _get_tokenizer(self, model: ModelName) -> Any:
        """Get or create tokenizer for a model."""
        if model in self._tokenizers:
            return self._tokenizers[model]

        # OpenAI models (tiktoken)
        if model.startswith("gpt"):
            try:
                tokenizer = tiktoken.encoding_for_model(model)
                self._tokenizers[model] = tokenizer
                return tokenizer
            except Exception:
                # Fallback to cl100k_base
                tokenizer = tiktoken.get_encoding("cl100k_base")
                self._tokenizers[model] = tokenizer
                return tokenizer

        # Claude models (Anthropic tokenizer approximation)
        if model.startswith("claude"):
            # Anthropic uses a similar tokenizer to GPT-4
            # For accurate counts, you'd use: anthropic.count_tokens()
            # Here we approximate with cl100k_base
            tokenizer = tiktoken.get_encoding("cl100k_base")
            self._tokenizers[model] = tokenizer
            return tokenizer

        # Gemini (SentencePiece approximation)
        if model == "gemini-pro":
            # Google uses SentencePiece, approximate with cl100k_base
            tokenizer = tiktoken.get_encoding("cl100k_base")
            self._tokenizers[model] = tokenizer
            return tokenizer

        raise ValueError(f"Unsupported model: {model}")

    def count_tokens(self, text: str, model: ModelName) -> int:
        """Count tokens for a given model."""
        tokenizer = self._get_tokenizer(model)
        
        # For tiktoken
        if hasattr(tokenizer, "encode"):
            return len(tokenizer.encode(text))
        
        # Fallback: rough estimate
        return len(text) // 4

    def benchmark_format(
        self, data: Any, format_type: Literal["json", "toon"], model: ModelName = "gpt-4"
    ) -> TokenStats:
        """
        Benchmark a single format.
        
        Args:
            data: Data to encode
            format_type: 'json' or 'toon'
            model: Model to use for token counting
            
        Returns:
            TokenStats with timing and count information
        """
        start = time.perf_counter()

        if format_type == "json":
            encoded = json.dumps(data, separators=(",", ":"))
        else:  # toon
            encoded = encode(data, self.config)

        encoding_time = (time.perf_counter() - start) * 1000  # ms

        token_count = self.count_tokens(encoded, model)
        char_count = len(encoded)

        return TokenStats(
            format=format_type,
            model=model,
            token_count=token_count,
            char_count=char_count,
            encoding_time_ms=encoding_time,
            tokens_per_char=token_count / max(char_count, 1),
        )

    def compare(self, data: Any, model: ModelName = "gpt-4") -> ComparisonResult:
        """
        Compare JSON vs TOON for the same data.
        
        Args:
            data: Data to compare
            model: Model to use for token counting
            
        Returns:
            ComparisonResult with detailed metrics
            
        Examples:
            >>> benchmark = TokenBenchmark()
            >>> data = {"users": [{"id": i, "name": f"User{i}"} for i in range(100)]}
            >>> result = benchmark.compare(data, "gpt-4")
            >>> print(result)
            >>> print(f"Saved {result.token_reduction_pct:.1f}% tokens!")
        """
        json_stats = self.benchmark_format(data, "json", model)
        toon_stats = self.benchmark_format(data, "toon", model)

        token_reduction = (
            (json_stats.token_count - toon_stats.token_count) / json_stats.token_count * 100
        )
        char_reduction = (
            (json_stats.char_count - toon_stats.char_count) / json_stats.char_count * 100
        )
        speedup = json_stats.encoding_time_ms / max(toon_stats.encoding_time_ms, 0.001)

        return ComparisonResult(
            json_stats=json_stats,
            toon_stats=toon_stats,
            token_reduction_pct=token_reduction,
            char_reduction_pct=char_reduction,
            speedup=speedup,
        )


def compare_formats(
    data: Any, models: list[ModelName] | None = None, config: ToonConfig | None = None
) -> dict[str, ComparisonResult]:
    """
    Compare JSON vs TOON across multiple models.
    
    Args:
        data: Data to compare
        models: List of models to benchmark (default: ["gpt-4", "claude-3", "gemini-pro"])
        config: Optional TOON configuration
        
    Returns:
        Dictionary mapping model names to comparison results
        
    Examples:
        >>> data = {"items": [{"id": i} for i in range(50)]}
        >>> results = compare_formats(data)
        >>> for model, result in results.items():
        ...     print(f"{model}: {result.token_reduction_pct:.1f}% reduction")
    """
    models = models or ["gpt-4", "claude-3", "gemini-pro"]
    benchmark = TokenBenchmark(config)

    results = {}
    for model in models:
        results[model] = benchmark.compare(data, model)

    return results

