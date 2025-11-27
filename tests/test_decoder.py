"""Tests for TOON decoder."""

import pytest

from toonkit.core.decoder import decode
from toonkit.core.types import ParserMode, ToonConfig, ToonDecodingError


class TestBasicDecoding:
    """Test basic decoding functionality."""

    def test_decode_simple_object(self, strict_config: ToonConfig) -> None:
        """Decode simple key-value pairs."""
        toon = "age: 30\nname: Alice"
        result = decode(toon, strict_config)
        assert result == {"age": 30, "name": "Alice"}

    def test_decode_primitives(self, strict_config: ToonConfig) -> None:
        """Decode different primitive types."""
        toon = """
null_val: null
bool_true: true
bool_false: false
integer: 42
float_val: 3.14
string: hello
        """.strip()
        
        result = decode(toon, strict_config)
        assert result["null_val"] is None
        assert result["bool_true"] is True
        assert result["bool_false"] is False
        assert result["integer"] == 42
        assert result["float_val"] == 3.14
        assert result["string"] == "hello"

    def test_decode_quoted_string(self, strict_config: ToonConfig) -> None:
        """Decode quoted strings with escapes."""
        toon = 'message: "She said \\"hello\\""'
        result = decode(toon, strict_config)
        assert result["message"] == 'She said "hello"'


class TestTabularDecoding:
    """Test tabular array decoding."""

    def test_decode_tabular_array(self, strict_config: ToonConfig) -> None:
        """Decode tabular array format."""
        toon = """
users[3]{id,name,role}:
  1,Alice,admin
  2,Bob,user
  3,Charlie,user
        """.strip()
        
        result = decode(toon, strict_config)
        assert "users" in result
        assert len(result["users"]) == 3
        assert result["users"][0] == {"id": 1, "name": "Alice", "role": "admin"}
        assert result["users"][1] == {"id": 2, "name": "Bob", "role": "user"}

    def test_decode_pipe_delimiter(self, strict_config: ToonConfig) -> None:
        """Decode tabular array with pipe delimiter."""
        toon = """
addresses[2]{street,city}|:
  123 Main St, Suite 100|Boston
  456 Oak Ave, Apt 5B|Seattle
        """.strip()
        
        result = decode(toon, strict_config)
        assert len(result["addresses"]) == 2
        assert result["addresses"][0]["street"] == "123 Main St, Suite 100"
        assert result["addresses"][0]["city"] == "Boston"

    def test_decode_mismatched_columns(self, strict_config: ToonConfig) -> None:
        """Mismatched column count in strict mode fails."""
        toon = """
items[2]{id,name}:
  1,Alice
  2,Bob,extra
        """.strip()
        
        with pytest.raises(ToonDecodingError, match="values"):
            decode(toon, strict_config)

    def test_decode_mismatched_columns_permissive(self, permissive_config: ToonConfig) -> None:
        """Permissive mode handles mismatched columns."""
        toon = """
items[2]{id,name}:
  1,Alice
  2,Bob,extra
        """.strip()
        
        result = decode(toon, permissive_config)
        # Should pad/truncate to match
        assert len(result["items"]) == 2


class TestNestedDecoding:
    """Test nested structure decoding."""

    def test_decode_nested_object(self, strict_config: ToonConfig) -> None:
        """Decode nested objects."""
        toon = """
user:
  name: Alice
  contact:
    email: alice@example.com
    phone: 555-1234
        """.strip()
        
        result = decode(toon, strict_config)
        assert result["user"]["name"] == "Alice"
        assert result["user"]["contact"]["email"] == "alice@example.com"
        assert result["user"]["contact"]["phone"] == "555-1234"


class TestParserModes:
    """Test strict vs permissive parsing."""

    def test_strict_rejects_bad_indent(self) -> None:
        """Strict mode rejects incorrect indentation."""
        config = ToonConfig(mode=ParserMode.STRICT)
        toon = """
key1: value1
   key2: value2
        """.strip()
        
        with pytest.raises(ToonDecodingError):
            decode(toon, config)

    def test_permissive_accepts_bad_indent(self) -> None:
        """Permissive mode tolerates indentation issues."""
        config = ToonConfig(mode=ParserMode.PERMISSIVE)
        toon = """
key1: value1
   key2: value2
        """.strip()
        
        result = decode(toon, config)
        # Should parse what it can
        assert "key1" in result


class TestEdgeCases:
    """Test edge cases."""

    def test_decode_empty_input(self, strict_config: ToonConfig) -> None:
        """Empty input decodes to None or empty dict."""
        result = decode("", strict_config)
        assert result is None or result == {}

    def test_decode_whitespace_only(self, strict_config: ToonConfig) -> None:
        """Whitespace-only input."""
        result = decode("   \n  \n  ", strict_config)
        assert result is None or result == {}

    def test_size_limit(self) -> None:
        """Size limit validation."""
        from toonkit.core.types import ToonValidationError
        
        config = ToonConfig(max_size_mb=0.001)
        large_toon = "key: " + ("x" * 10000)
        
        with pytest.raises(ToonValidationError):
            decode(large_toon, config)

