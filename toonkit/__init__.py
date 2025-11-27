"""
Toonkit - Production-grade JSON ↔ TOON converter with benchmarking.

A comprehensive toolkit for converting between JSON and TOON (Token-Oriented Object Notation),
with multi-model tokenization benchmarks, streaming support, and robust validation.
"""

from toonkit.core.decoder import decode, decode_streaming
from toonkit.core.encoder import encode, encode_streaming
from toonkit.benchmark.tokenizer import TokenBenchmark, compare_formats
from toonkit.core.types import (
    ToonConfig,
    ParserMode,
    ToonError,
    ToonEncodingError,
    ToonDecodingError,
    ToonValidationError,
)

__version__ = "0.1.0"
__all__ = [
    # Core functions
    "encode",
    "decode",
    "encode_streaming",
    "decode_streaming",
    # Benchmarking
    "TokenBenchmark",
    "compare_formats",
    # Types & Config
    "ToonConfig",
    "ParserMode",
    # Errors
    "ToonError",
    "ToonEncodingError",
    "ToonDecodingError",
    "ToonValidationError",
]

