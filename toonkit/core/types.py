"""Type definitions and configuration for toonkit."""

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class ParserMode(str, Enum):
    """Parser strictness mode."""

    STRICT = "strict"
    PERMISSIVE = "permissive"


class ToonConfig(BaseModel):
    """Configuration for TOON encoding/decoding.
    
    Attributes:
        mode: Parser mode (strict or permissive)
        max_depth: Maximum nesting depth (default: 10)
        max_size_mb: Maximum input size in MB (default: 50)
        indent_size: Number of spaces per indent level (default: 2)
        sort_keys: Sort object keys alphabetically for canonical output (default: True)
        delimiter: Default delimiter for tabular arrays (default: ',')
        allow_custom_delimiter: Allow custom delimiters like | or tab (default: True)
    """

    mode: ParserMode = Field(default=ParserMode.STRICT)
    max_depth: int = Field(default=10, ge=1, le=100)
    max_size_mb: float = Field(default=50.0, gt=0, le=1000)
    indent_size: int = Field(default=2, ge=1, le=8)
    sort_keys: bool = Field(default=True)
    delimiter: str = Field(default=",")
    allow_custom_delimiter: bool = Field(default=True)

    model_config = {"frozen": True}


# Error hierarchy
class ToonError(Exception):
    """Base exception for all toonkit errors."""

    pass


class ToonEncodingError(ToonError):
    """Error during JSON → TOON encoding."""

    pass


class ToonDecodingError(ToonError):
    """Error during TOON → JSON decoding."""

    pass


class ToonValidationError(ToonError):
    """Validation error (depth, size limits, etc.)."""

    pass


# Type aliases
JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None
ToonDelimiter = Literal[",", "|", "\t"]

