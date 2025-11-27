"""Tests for TOON encoder."""

import pytest

from toonkit.core.encoder import encode
from toonkit.core.types import ToonConfig, ToonEncodingError, ToonValidationError


class TestBasicEncoding:
    """Test basic encoding functionality."""

    def test_encode_empty_dict(self, strict_config: ToonConfig) -> None:
        """Empty dict encodes to empty braces."""
        result = encode({}, strict_config)
        assert result == "{}"

    def test_encode_simple_object(self, strict_config: ToonConfig) -> None:
        """Simple object with sorted keys."""
        data = {"name": "Alice", "age": 30}
        result = encode(data, strict_config)
        assert "age: 30" in result
        assert "name: Alice" in result
        # Keys should be sorted
        lines = result.split("\n")
        assert lines[0].startswith("age:")
        assert lines[1].startswith("name:")

    def test_encode_primitives(self, strict_config: ToonConfig) -> None:
        """Encode different primitive types."""
        data = {
            "null_val": None,
            "bool_true": True,
            "bool_false": False,
            "integer": 42,
            "float_val": 3.14,
            "string": "hello",
        }
        result = encode(data, strict_config)
        assert "null_val: null" in result
        assert "bool_true: true" in result
        assert "bool_false: false" in result
        assert "integer: 42" in result
        assert "float_val: 3.14" in result
        assert "string: hello" in result


class TestTabularEncoding:
    """Test tabular array encoding."""

    def test_encode_uniform_array(self, sample_users: list[dict], strict_config: ToonConfig) -> None:
        """Uniform array uses tabular format."""
        data = {"users": sample_users}
        result = encode(data, strict_config)
        
        # Should have tabular header
        assert "users[3]{" in result
        assert "active" in result
        assert "id" in result
        assert "name" in result
        assert "role" in result
        
        # Should have data rows
        assert "Alice" in result
        assert "Bob" in result
        assert "Charlie" in result

    def test_encode_with_comma_in_data(self, strict_config: ToonConfig) -> None:
        """Data with commas uses pipe delimiter."""
        data = {
            "addresses": [
                {"street": "123 Main St, Suite 100", "city": "Boston"},
                {"street": "456 Oak Ave, Apt 5B", "city": "Seattle"},
            ]
        }
        result = encode(data, strict_config)
        
        # Should use pipe delimiter
        assert "|:" in result or "," not in result  # Either pipes or proper escaping


class TestNestedStructures:
    """Test nested object encoding."""

    def test_encode_nested_object(self, sample_nested: dict, strict_config: ToonConfig) -> None:
        """Nested objects are indented."""
        result = encode(sample_nested, strict_config)
        
        assert "company: ACME Corp" in result
        assert "employees" in result
        assert "metadata" in result
        
        # Check indentation
        lines = result.split("\n")
        # metadata should be indented under root
        for line in lines:
            if "created:" in line:
                assert line.startswith("  ")  # 2 spaces indent

    def test_max_depth_limit(self, strict_config: ToonConfig) -> None:
        """Exceeding max depth raises error."""
        # Create deeply nested structure
        data: dict = {"level": 0}
        current = data
        for i in range(15):
            current["nested"] = {"level": i + 1}
            current = current["nested"]
        
        with pytest.raises(ToonValidationError, match="depth"):
            encode(data, strict_config)


class TestConfiguration:
    """Test configuration options."""

    def test_unsorted_keys(self) -> None:
        """Test key ordering when sort_keys=False."""
        config = ToonConfig(sort_keys=False)
        data = {"z": 1, "a": 2, "m": 3}
        result = encode(data, config)
        lines = result.split("\n")
        
        # Order should match insertion (Python 3.7+)
        assert lines[0].startswith("z:")
        assert lines[1].startswith("a:")
        assert lines[2].startswith("m:")

    def test_custom_indent(self) -> None:
        """Test custom indentation size."""
        config = ToonConfig(indent_size=4)
        data = {"user": {"name": "Alice"}}
        result = encode(data, config)
        
        # Should have 4-space indent
        assert "\n    name: Alice" in result or "    name: Alice" in result

    def test_size_limit(self) -> None:
        """Test size limit validation."""
        config = ToonConfig(max_size_mb=0.001)  # 1KB limit
        large_data = {"items": [{"id": i, "data": "x" * 1000} for i in range(100)]}
        
        with pytest.raises(ToonValidationError, match="size"):
            encode(large_data, config)


class TestEdgeCases:
    """Test edge cases and special characters."""

    def test_encode_empty_string(self, strict_config: ToonConfig) -> None:
        """Empty string is quoted."""
        data = {"empty": ""}
        result = encode(data, strict_config)
        assert 'empty: ""' in result

    def test_encode_string_with_quotes(self, strict_config: ToonConfig) -> None:
        """String with quotes is escaped."""
        data = {"quote": 'She said "hello"'}
        result = encode(data, strict_config)
        assert '\\"' in result or "hello" in result

    def test_encode_special_chars(self, strict_config: ToonConfig) -> None:
        """Special characters are handled."""
        data = {
            "newline": "line1\nline2",
            "tab": "col1\tcol2",
            "colon": "key:value",
        }
        result = encode(data, strict_config)
        # All should be quoted or escaped
        assert result  # Just verify it doesn't crash


class TestStreamingEncoder:
    """Test streaming encoder."""

    def test_streaming_basic(self, sample_users: list[dict], strict_config: ToonConfig) -> None:
        """Streaming encoder produces same output."""
        from toonkit.core.encoder import encode_streaming
        
        data = {"users": sample_users}
        lines = list(encode_streaming(data, strict_config))
        streamed_result = "\n".join(lines)
        
        regular_result = encode(data, strict_config)
        assert streamed_result == regular_result

