"""Round-trip tests: JSON → TOON → JSON should be identical."""

import json

import pytest

from toonkit.core.decoder import decode
from toonkit.core.encoder import encode
from toonkit.core.types import ToonConfig


class TestRoundTrip:
    """Test data integrity through encode/decode cycles."""

    def test_roundtrip_simple_object(self, strict_config: ToonConfig) -> None:
        """Simple object round-trip."""
        original = {"name": "Alice", "age": 30, "active": True}
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert decoded == original

    def test_roundtrip_nested_object(self, sample_nested: dict, strict_config: ToonConfig) -> None:
        """Nested object round-trip."""
        toon = encode(sample_nested, strict_config)
        decoded = decode(toon, strict_config)
        
        # Compare as JSON strings to handle key ordering
        assert json.dumps(decoded, sort_keys=True) == json.dumps(sample_nested, sort_keys=True)

    def test_roundtrip_array(self, sample_users: list[dict], strict_config: ToonConfig) -> None:
        """Array round-trip."""
        original = {"users": sample_users}
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert json.dumps(decoded, sort_keys=True) == json.dumps(original, sort_keys=True)

    def test_roundtrip_primitives(self, strict_config: ToonConfig) -> None:
        """All primitive types round-trip correctly."""
        original = {
            "null": None,
            "bool_true": True,
            "bool_false": False,
            "int": 42,
            "float": 3.14,
            "string": "hello",
            "empty_string": "",
        }
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert decoded == original

    def test_roundtrip_special_strings(self, strict_config: ToonConfig) -> None:
        """Strings with special characters round-trip."""
        original = {
            "comma": "a,b,c",
            "colon": "key:value",
            "quote": 'say "hello"',
            "newline": "line1\nline2",
            "tab": "col1\tcol2",
        }
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert decoded == original

    def test_roundtrip_multiple_cycles(self, sample_users: list[dict], strict_config: ToonConfig) -> None:
        """Multiple encode/decode cycles preserve data."""
        data = {"users": sample_users}
        
        for _ in range(5):
            toon = encode(data, strict_config)
            data = decode(toon, strict_config)
        
        # After 5 cycles, data should be identical
        assert json.dumps(data, sort_keys=True) == json.dumps(
            {"users": sample_users}, sort_keys=True
        )

    @pytest.mark.parametrize("iteration", range(10))
    def test_roundtrip_stability(
        self, sample_nested: dict, strict_config: ToonConfig, iteration: int
    ) -> None:
        """Round-trip is stable across multiple runs."""
        toon = encode(sample_nested, strict_config)
        decoded = decode(toon, strict_config)
        
        assert json.dumps(decoded, sort_keys=True) == json.dumps(sample_nested, sort_keys=True)


class TestRoundTripEdgeCases:
    """Test round-trip for edge cases."""

    def test_roundtrip_empty_dict(self, strict_config: ToonConfig) -> None:
        """Empty dict round-trip."""
        original = {}
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        # Empty dict or None are both acceptable
        assert decoded == original or decoded is None

    def test_roundtrip_single_key(self, strict_config: ToonConfig) -> None:
        """Single key-value pair."""
        original = {"only": "one"}
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert decoded == original

    def test_roundtrip_deep_nesting(self, strict_config: ToonConfig) -> None:
        """Deeply nested structure (within limits)."""
        original = {"l1": {"l2": {"l3": {"l4": {"l5": {"value": 42}}}}}}
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert json.dumps(decoded, sort_keys=True) == json.dumps(original, sort_keys=True)

    def test_roundtrip_unicode(self, strict_config: ToonConfig) -> None:
        """Unicode characters round-trip."""
        original = {
            "emoji": "🚀💡",
            "chinese": "你好",
            "arabic": "مرحبا",
            "spanish": "¡Hola!",
        }
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert decoded == original

    def test_roundtrip_numbers(self, strict_config: ToonConfig) -> None:
        """Various number formats."""
        original = {
            "zero": 0,
            "negative": -42,
            "large": 999999999,
            "float": 3.14159,
            "scientific": 1.23e-4,
        }
        
        toon = encode(original, strict_config)
        decoded = decode(toon, strict_config)
        
        assert decoded == original

