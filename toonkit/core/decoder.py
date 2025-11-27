"""TOON to JSON decoder with strict and permissive modes."""

import re
import sys
from collections.abc import Iterator
from typing import Any

from toonkit.core.types import (
    JsonValue,
    ParserMode,
    ToonConfig,
    ToonDecodingError,
    ToonValidationError,
)


def decode(toon_str: str, config: ToonConfig | None = None) -> JsonValue:
    """
    Convert TOON string to JSON data.
    
    Args:
        toon_str: TOON-formatted string
        config: Optional configuration
        
    Returns:
        Python dict/list/primitive
        
    Raises:
        ToonDecodingError: If parsing fails
        ToonValidationError: If data exceeds limits
        
    Examples:
        >>> decode("name: Alice\\nage: 30")
        {'age': 30, 'name': 'Alice'}
        
        >>> decode("users[2]{id,name}:\\n  1,Alice\\n  2,Bob")
        {'users': [{'id': 1, 'name': 'Alice'}, {'id': 2, 'name': 'Bob'}]}
    """
    config = config or ToonConfig()
    
    # Check size
    size_mb = sys.getsizeof(toon_str) / (1024 * 1024)
    if size_mb > config.max_size_mb:
        raise ToonValidationError(
            f"Input size {size_mb:.2f}MB exceeds limit {config.max_size_mb}MB"
        )
    
    decoder = _ToonDecoder(config)
    return decoder.decode(toon_str)


def decode_streaming(lines: Iterator[str], config: ToonConfig | None = None) -> JsonValue:
    """
    Decode TOON from streaming line input.
    
    Args:
        lines: Iterator of TOON lines
        config: Optional configuration
        
    Returns:
        Decoded JSON data
    """
    config = config or ToonConfig()
    toon_str = "\n".join(lines)
    return decode(toon_str, config)


class _ToonDecoder:
    """Internal decoder with line-by-line parsing."""

    def __init__(self, config: ToonConfig):
        self.config = config

    def _decode_key(self, key: str) -> str:
        """Decode a potentially quoted key."""
        if key.startswith('"') and key.endswith('"'):
            # Unescape quoted key
            unquoted = key[1:-1]
            result = []
            i = 0
            while i < len(unquoted):
                if unquoted[i] == '\\' and i + 1 < len(unquoted):
                    next_char = unquoted[i + 1]
                    if next_char == 'n':
                        result.append('\n')
                    elif next_char == 'r':
                        result.append('\r')
                    elif next_char == 't':
                        result.append('\t')
                    elif next_char == '"':
                        result.append('"')
                    elif next_char == '\\':
                        result.append('\\')
                    else:
                        result.append(next_char)
                    i += 2
                else:
                    result.append(unquoted[i])
                    i += 1
            return ''.join(result)
        return key

    def decode(self, toon_str: str) -> JsonValue:
        """Parse TOON string into JSON."""
        stripped = toon_str.strip()
        
        # Handle special cases
        if stripped == "{}":
            return {}
        if stripped == "[]":
            return []
        if not stripped:
            return None
            
        lines = stripped.split("\n")
        result, _ = self._parse_lines(lines, 0, 0)
        return result

    def _parse_lines(
        self, lines: list[str], start_idx: int, base_indent: int
    ) -> tuple[Any, int]:
        """
        Parse lines starting from start_idx with expected indentation.
        
        Returns:
            (parsed_value, next_line_index)
        """
        if start_idx >= len(lines):
            return None, start_idx

        result: dict[str, Any] = {}
        idx = start_idx

        while idx < len(lines):
            line = lines[idx]
            
            if not line.strip():
                idx += 1
                continue

            indent = len(line) - len(line.lstrip())
            
            if indent < base_indent:
                # Dedent - return to parent
                break

            if indent > base_indent:
                # Over-indented - error in strict mode
                if self.config.mode == ParserMode.STRICT:
                    raise ToonDecodingError(f"Unexpected indentation at line {idx + 1}")
                # In permissive mode, skip
                idx += 1
                continue

            # Parse this line
            stripped = line.strip()

            # Check for tabular array: [N]{cols}: (without key - direct array)
            tabular_no_key_match = re.match(
                r"^\[(\d+)\]\{([^}]+)\}([,|\t])?:$", stripped
            )
            if tabular_no_key_match:
                count = int(tabular_no_key_match.group(1))
                columns = [c.strip() for c in tabular_no_key_match.group(2).split(",")]
                delimiter = tabular_no_key_match.group(3) or ","
                
                # Parse rows
                array_data, idx = self._parse_tabular_rows(
                    lines, idx + 1, indent + self.config.indent_size, columns, delimiter, count
                )
                return array_data, idx

            # Check for tabular array: key[N]{cols}:
            tabular_match = re.match(
                r"^(\w+)\[(\d+)\]\{([^}]+)\}([,|\t])?:$", stripped
            )
            if tabular_match:
                key = tabular_match.group(1)
                count = int(tabular_match.group(2))
                columns = [c.strip() for c in tabular_match.group(3).split(",")]
                delimiter = tabular_match.group(4) or ","
                
                # Parse rows
                array_data, idx = self._parse_tabular_rows(
                    lines, idx + 1, indent + self.config.indent_size, columns, delimiter, count
                )
                result[key] = array_data
                continue

            # Regular key-value: "key: value" or "key:" (value on next lines)
            # Also handle quoted keys: "\"key\": value"
            if ": " in stripped or stripped.endswith(":"):
                if ": " in stripped:
                    key, value_part = stripped.split(": ", 1)
                    key = self._decode_key(key.strip())
                    value_part = value_part.strip()
                else:
                    # "key:" format - value is on next lines
                    key = self._decode_key(stripped[:-1].strip())
                    value_part = ""

                if value_part:
                    # Inline value
                    result[key] = self._parse_value(value_part)
                    idx += 1
                else:
                    # Nested value on next lines
                    nested_val, idx = self._parse_lines(
                        lines, idx + 1, indent + self.config.indent_size
                    )
                    result[key] = nested_val
                continue

            # Array item: "- value"
            if stripped.startswith("- "):
                # This is an array element - should be handled by parent
                break

            # Unknown format
            if self.config.mode == ParserMode.STRICT:
                raise ToonDecodingError(f"Invalid TOON syntax at line {idx + 1}: {stripped}")
            
            idx += 1

        # If result is empty and we're at an array, parse array
        if not result and start_idx < len(lines):
            line = lines[start_idx].strip()
            if line.startswith("- "):
                return self._parse_array(lines, start_idx, base_indent)

        return result if result else None, idx

    def _parse_tabular_rows(
        self,
        lines: list[str],
        start_idx: int,
        expected_indent: int,
        columns: list[str],
        delimiter: str,
        expected_count: int,
    ) -> tuple[list[dict[str, Any]], int]:
        """Parse tabular array rows."""
        rows: list[dict[str, Any]] = []
        idx = start_idx

        while idx < len(lines) and len(rows) < expected_count:
            line = lines[idx]
            if not line.strip():
                idx += 1
                continue

            indent = len(line) - len(line.lstrip())
            if indent < expected_indent:
                break

            if indent == expected_indent:
                stripped = line.strip()
                values = self._split_by_delimiter(stripped, delimiter)
                
                if len(values) != len(columns):
                    if self.config.mode == ParserMode.STRICT:
                        raise ToonDecodingError(
                            f"Row at line {idx + 1} has {len(values)} values, expected {len(columns)}"
                        )
                    # Permissive: pad or truncate
                    values = (values + [""] * len(columns))[:len(columns)]

                row = {col: self._parse_value(val) for col, val in zip(columns, values)}
                rows.append(row)

            idx += 1

        return rows, idx

    def _split_by_delimiter(self, line: str, delimiter: str) -> list[str]:
        """Split line by delimiter, respecting quoted strings."""
        if delimiter == "\t":
            return line.split("\t")
        
        # Handle quoted strings - preserve quotes in output for _parse_value
        parts: list[str] = []
        current = ""
        in_quotes = False
        escape = False

        for char in line:
            if escape:
                current += char
                escape = False
            elif char == "\\":
                current += char  # Preserve escape character
                escape = True
            elif char == '"':
                current += char  # Preserve quote character
                in_quotes = not in_quotes
            elif char == delimiter and not in_quotes:
                parts.append(current.strip())
                current = ""
            else:
                current += char

        if current or line.endswith(delimiter):
            parts.append(current.strip())

        return parts

    def _parse_value(self, value_str: str) -> Any:
        """Parse a primitive value."""
        value_str = value_str.strip()

        if not value_str or value_str == "null":
            return None
        if value_str == "true":
            return True
        if value_str == "false":
            return False
        if value_str == "[]":
            return []
        if value_str == "{}":
            return {}
        
        # Remove quotes if present
        if value_str.startswith('"') and value_str.endswith('"'):
            # Unescape - order matters!
            unquoted = value_str[1:-1]
            result = []
            i = 0
            while i < len(unquoted):
                if unquoted[i] == '\\' and i + 1 < len(unquoted):
                    next_char = unquoted[i + 1]
                    if next_char == 'n':
                        result.append('\n')
                    elif next_char == 'r':
                        result.append('\r')
                    elif next_char == 't':
                        result.append('\t')
                    elif next_char == 'f':
                        result.append('\f')
                    elif next_char == 'b':
                        result.append('\b')
                    elif next_char == '"':
                        result.append('"')
                    elif next_char == '\\':
                        result.append('\\')
                    elif next_char == 'u' and i + 5 < len(unquoted):
                        # Unicode escape: \uXXXX
                        try:
                            hex_str = unquoted[i+2:i+6]
                            code_point = int(hex_str, 16)
                            result.append(chr(code_point))
                            i += 4  # Skip ahead to account for 4 hex digits
                        except (ValueError, OverflowError):
                            result.append(next_char)
                    else:
                        result.append(next_char)
                    i += 2
                else:
                    result.append(unquoted[i])
                    i += 1
            return ''.join(result)

        # Try number (int, float, scientific notation)
        try:
            if "." in value_str or "e" in value_str.lower():
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            pass

        # Return as string
        return value_str

    def _parse_array(
        self, lines: list[str], start_idx: int, base_indent: int
    ) -> tuple[list[Any], int]:
        """Parse array with '- ' prefix."""
        result: list[Any] = []
        idx = start_idx

        while idx < len(lines):
            line = lines[idx]
            if not line.strip():
                idx += 1
                continue

            indent = len(line) - len(line.lstrip())
            if indent < base_indent:
                break

            stripped = line.strip()
            # Check for array item: "- value" or just "-" (multiline item)
            if stripped.startswith("- ") or stripped == "-":
                if stripped.startswith("- "):
                    value_str = stripped[2:].strip()
                else:
                    # Just "-" means value is on next lines
                    value_str = ""
                
                if value_str:
                    # Check if value_str starts with "- " which means nested array
                    if value_str.startswith("- "):
                        # Nested array on same line: "- - value"
                        # We need to process this as a nested array
                        # Create a virtual nested array by looking at following lines
                        nested_array = [self._parse_value(value_str[2:].strip())]
                        
                        # Look ahead for more nested items at same level
                        idx += 1
                        while idx < len(lines):
                            next_line = lines[idx]
                            if not next_line.strip():
                                idx += 1
                                continue
                            
                            next_indent = len(next_line) - len(next_line.lstrip())
                            next_stripped = next_line.strip()
                            
                            # If we find another "- -" at same indent, it's part of nested array
                            if next_indent == indent and next_stripped.startswith("- - "):
                                nested_value_str = next_stripped[4:].strip()
                                nested_array.append(self._parse_value(nested_value_str))
                                idx += 1
                            elif next_indent < indent:
                                # Dedent - end of array
                                break
                            else:
                                # Different indent or different prefix - end of nested array
                                break
                        
                        result.append(nested_array)
                        continue
                    else:
                        result.append(self._parse_value(value_str))
                else:
                    # Nested structure (object or array on next lines)
                    nested, idx = self._parse_lines(
                        lines, idx + 1, base_indent + self.config.indent_size
                    )
                    result.append(nested)
                    continue
            else:
                break

            idx += 1

        return result, idx

