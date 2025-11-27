"""JSON to TOON encoder with canonical output and streaming support."""

import sys
from collections.abc import Iterator
from typing import Any

from toonkit.core.types import (
    JsonValue,
    ToonConfig,
    ToonDelimiter,
    ToonEncodingError,
    ToonValidationError,
)


def encode(data: JsonValue, config: ToonConfig | None = None) -> str:
    """
    Convert JSON data to TOON format.
    
    Args:
        data: JSON-compatible data (dict, list, primitives)
        config: Optional configuration (defaults to strict mode with canonical ordering)
        
    Returns:
        TOON-formatted string
        
    Raises:
        ToonEncodingError: If encoding fails
        ToonValidationError: If data exceeds limits
        
    Examples:
        >>> encode({"name": "Alice", "age": 30})
        'age: 30\\nname: Alice'
        
        >>> encode({"users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]})
        'users[2]{id,name}:\\n  1,Alice\\n  2,Bob'
    """
    config = config or ToonConfig()
    
    # Estimate size (rough heuristic)
    estimated_size_mb = sys.getsizeof(str(data)) / (1024 * 1024)
    if estimated_size_mb > config.max_size_mb:
        raise ToonValidationError(
            f"Input size {estimated_size_mb:.2f}MB exceeds limit {config.max_size_mb}MB"
        )
    
    encoder = _ToonEncoder(config)
    return encoder.encode_value(data, depth=0)


def encode_streaming(data: JsonValue, config: ToonConfig | None = None) -> Iterator[str]:
    """
    Stream TOON encoding line-by-line for large datasets.
    
    Useful for very large arrays or when you want to process chunks progressively.
    
    Args:
        data: JSON-compatible data
        config: Optional configuration
        
    Yields:
        Lines of TOON output
        
    Examples:
        >>> for line in encode_streaming({"items": [{"id": i} for i in range(1000)]}):
        ...     print(line)
    """
    config = config or ToonConfig()
    encoder = _ToonEncoder(config)
    yield from encoder.encode_streaming(data, depth=0)


class _ToonEncoder:
    """Internal encoder with canonical key ordering and tabular array optimization."""

    def __init__(self, config: ToonConfig):
        self.config = config

    def _looks_like_number(self, s: str) -> bool:
        """Check if string looks like a number (int, float, scientific notation)."""
        if not s:
            return False
        try:
            float(s)
            return True
        except ValueError:
            return False

    def encode_value(self, value: Any, depth: int, indent: str = "") -> str:
        """Encode a value recursively."""
        if depth > self.config.max_depth:
            raise ToonValidationError(f"Maximum depth {self.config.max_depth} exceeded")

        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return self._encode_string(value)
        elif isinstance(value, list):
            return self._encode_array(value, depth, indent)
        elif isinstance(value, dict):
            return self._encode_object(value, depth, indent)
        else:
            raise ToonEncodingError(f"Unsupported type: {type(value)}")

    def _encode_string(self, s: str) -> str:
        """Encode string, adding quotes if it contains special chars."""
        # Check for any control characters or special chars that need quoting
        needs_quotes = (
            not s  # Empty string
            or any(c in s for c in ',:\n\r\t')  # Basic special chars
            or any(ord(c) < 32 for c in s)  # All control characters
            or s.isspace()  # Only whitespace
            or s != s.strip()  # Has leading/trailing whitespace
            or s in ('true', 'false', 'null', '[]', '{}')  # Reserved literals
            or self._looks_like_number(s)  # Looks like a number
        )
        if needs_quotes:
            # Escape special characters
            escaped = s.replace("\\", "\\\\")  # Backslash first
            escaped = escaped.replace('"', '\\"')  # Quotes
            escaped = escaped.replace('\n', '\\n')  # Newlines
            escaped = escaped.replace('\r', '\\r')  # Carriage return
            escaped = escaped.replace('\t', '\\t')  # Tab
            escaped = escaped.replace('\f', '\\f')  # Form feed
            escaped = escaped.replace('\b', '\\b')  # Backspace
            return f'"{escaped}"'
        return s

    def _encode_key(self, key: str) -> str:
        """Encode object key, quoting if necessary."""
        # Quote keys with special chars or whitespace issues
        needs_quotes = (
            not key  # Empty key
            or key != key.strip()  # Has leading/trailing whitespace
            or key.isspace()  # Only whitespace
            or ':' in key  # Contains colon
            or '\n' in key or '\r' in key or '\t' in key  # Control chars
            or any(ord(c) < 32 for c in key)  # Other control chars
        )
        if needs_quotes:
            escaped = key.replace("\\", "\\\\")
            escaped = escaped.replace('"', '\\"')
            escaped = escaped.replace('\n', '\\n')
            escaped = escaped.replace('\r', '\\r')
            escaped = escaped.replace('\t', '\\t')
            return f'"{escaped}"'
        return key

    def _encode_object(self, obj: dict[str, Any], depth: int, indent: str) -> str:
        """Encode object with canonical key ordering."""
        if not obj:
            return "{}"

        keys = sorted(obj.keys()) if self.config.sort_keys else list(obj.keys())
        lines: list[str] = []
        next_indent = indent + " " * self.config.indent_size

        for key in keys:
            encoded_key = self._encode_key(key)
            value = obj[key]
            
            # Special handling for tabular arrays
            if isinstance(value, list) and self._is_tabular(value):
                tabular_encoded = self._encode_tabular_with_key(encoded_key, value, depth, indent)
                lines.append(tabular_encoded)
            else:
                encoded_val = self.encode_value(value, depth + 1, next_indent)
                
                # Check if value is multiline OR is a nested object or array
                is_nested_object = (
                    isinstance(value, dict) and value  # Non-empty dict
                )
                is_nested_array = (
                    isinstance(value, list) and value  # Non-empty list
                )
                if "\n" in encoded_val or is_nested_object or is_nested_array:
                    lines.append(f"{indent}{encoded_key}:\n{encoded_val}")
                else:
                    lines.append(f"{indent}{encoded_key}: {encoded_val}")

        return "\n".join(lines)

    def _encode_array(self, arr: list[Any], depth: int, indent: str) -> str:
        """Encode array, using tabular format for uniform objects."""
        if not arr:
            return "[]"

        # Check if all elements are dicts with the same keys (tabular format eligible)
        if self._is_tabular(arr):
            return self._encode_tabular(arr, depth, indent)
        else:
            # Encode as regular array
            return self._encode_regular_array(arr, depth, indent)

    def _is_tabular(self, arr: list[Any]) -> bool:
        """Check if array is eligible for tabular format."""
        if not arr or not isinstance(arr[0], dict):
            return False
        
        first_keys = set(arr[0].keys())
        # Empty dicts are not tabular (no columns to display)
        if not first_keys:
            return False
        # All items must be dicts with identical keys
        return all(isinstance(item, dict) and set(item.keys()) == first_keys for item in arr)

    def _encode_tabular_with_key(self, key: str, arr: list[dict[str, Any]], depth: int, indent: str) -> str:
        """Encode array in tabular format with key included: key[n]{col1,col2}:"""
        if not arr:
            return f"{indent}{key}: []"

        count = len(arr)
        keys = sorted(arr[0].keys()) if self.config.sort_keys else list(arr[0].keys())
        delimiter = self._choose_delimiter(arr, keys)
        
        # Header with key: key[count]{key1,key2}delimiter:
        header = f"{indent}{key}[{count}]{{{','.join(keys)}}}{delimiter if delimiter != ',' else ''}:"
        
        next_indent = indent + " " * self.config.indent_size
        rows: list[str] = [header]
        
        for item in arr:
            row_values = [self._encode_cell(item[k], delimiter) for k in keys]
            rows.append(f"{next_indent}{delimiter.join(row_values)}")
        
        return "\n".join(rows)

    def _encode_tabular(self, arr: list[dict[str, Any]], depth: int, indent: str) -> str:
        """Encode array in tabular TOON format: [n]{key1,key2}:"""
        if not arr:
            return "[]"

        count = len(arr)
        keys = sorted(arr[0].keys()) if self.config.sort_keys else list(arr[0].keys())
        delimiter = self._choose_delimiter(arr, keys)
        
        # Header: [count]{key1,key2}delimiter:
        header = f"[{count}]{{{','.join(keys)}}}{delimiter if delimiter != ',' else ''}:"
        
        next_indent = indent + " " * self.config.indent_size
        rows: list[str] = [header]
        
        for item in arr:
            row_values = [self._encode_cell(item[k], delimiter) for k in keys]
            rows.append(f"{next_indent}{delimiter.join(row_values)}")
        
        return "\n".join(rows)

    def _choose_delimiter(self, arr: list[dict[str, Any]], keys: list[str]) -> ToonDelimiter:
        """Choose delimiter based on data (comma, pipe, or tab)."""
        if not self.config.allow_custom_delimiter:
            return ","
        
        # Check if any value contains comma
        has_comma = any(
            "," in str(item[k]) for item in arr for k in keys if isinstance(item[k], str)
        )
        
        if has_comma:
            # Use pipe if data has commas
            return "|"
        
        return ","

    def _encode_cell(self, value: Any, delimiter: str) -> str:
        """Encode a single cell value for tabular format."""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Check if string would be ambiguous (looks like number, bool, null, or structure)
            needs_quotes = (
                not value  # Empty string
                or delimiter in value
                or any(c in value for c in '\n\r\t')
                or any(ord(c) < 32 or (128 <= ord(c) < 160) for c in value)  # Control chars and extended control chars
                or value in ('true', 'false', 'null', '[]', '{}')
                or self._looks_like_number(value)
            )
            if needs_quotes:
                escaped = value.replace("\\", "\\\\")
                escaped = escaped.replace('"', '\\"')
                escaped = escaped.replace('\n', '\\n')
                escaped = escaped.replace('\r', '\\r')
                escaped = escaped.replace('\t', '\\t')
                escaped = escaped.replace('\f', '\\f')
                escaped = escaped.replace('\b', '\\b')
                # Escape extended control characters as unicode
                result = []
                for c in escaped:
                    if 128 <= ord(c) < 160:
                        result.append(f'\\u{ord(c):04x}')
                    else:
                        result.append(c)
                return f'"{"".join(result)}"'
            return value
        else:
            # Nested structures - inline JSON (fallback)
            import json
            return json.dumps(value, separators=(",", ":"))

    def _encode_regular_array(self, arr: list[Any], depth: int, indent: str) -> str:
        """Encode non-tabular array."""
        # indent is already the correct level for array items
        # Only add extra indent for nested content within items
        item_content_indent = indent + " " * self.config.indent_size
        items: list[str] = []
        for item in arr:
            encoded_item = self.encode_value(item, depth + 1, item_content_indent)
            # If item is a non-empty dict/object or multiline, put it on next line(s)
            # Empty dicts/arrays are fine inline
            is_nonempty_dict = isinstance(item, dict) and item
            is_nonempty_array = isinstance(item, list) and item
            if (is_nonempty_dict or is_nonempty_array) or "\n" in encoded_item:
                items.append(f"{indent}- \n{encoded_item}")
            else:
                items.append(f"{indent}- {encoded_item}")
        return "\n".join(items)

    def encode_streaming(self, value: Any, depth: int, indent: str = "") -> Iterator[str]:
        """Stream encoding line-by-line."""
        # For simplicity, yield full encoding split by lines
        # In production, this could be optimized to yield as we encode
        result = self.encode_value(value, depth, indent)
        for line in result.split("\n"):
            yield line

