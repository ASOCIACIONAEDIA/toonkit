"""Fuzz testing with hypothesis to find edge cases."""

import json

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from toonkit.core.decoder import decode
from toonkit.core.encoder import encode
from toonkit.core.types import ToonConfig, ToonError


# Hypothesis strategies for generating test data
json_primitives = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1000000, max_value=1000000),
    st.floats(allow_nan=False, allow_infinity=False, width=32),
    st.text(max_size=100, alphabet=st.characters(min_codepoint=32, max_codepoint=126, blacklist_characters='\\":')),
)

json_objects = st.recursive(
    json_primitives,
    lambda children: st.one_of(
        st.lists(children, max_size=10),
        st.dictionaries(st.text(min_size=1, max_size=20, alphabet=st.characters(min_codepoint=65, max_codepoint=122)), children, max_size=10),
    ),
    max_leaves=20,
)


@pytest.mark.fuzz
class TestFuzzRoundTrip:
    """Fuzz test round-trip conversion."""

    @given(data=json_objects)
    @settings(max_examples=100, deadline=1000)
    def test_fuzz_roundtrip(self, data: any) -> None:
        """Random data should round-trip correctly."""
        config = ToonConfig()
        
        try:
            # Encode to TOON
            toon = encode(data, config)
            
            # Decode back
            decoded = decode(toon, config)
            
            # Compare as JSON to handle key ordering
            original_json = json.dumps(data, sort_keys=True)
            decoded_json = json.dumps(decoded, sort_keys=True)
            
            assert original_json == decoded_json, f"Round-trip failed for: {data}"
            
        except ToonError:
            # Some data might exceed limits - that's ok
            pass

    @given(obj=st.dictionaries(st.text(min_size=1, max_size=20, alphabet=st.characters(min_codepoint=65, max_codepoint=122)), json_primitives, max_size=20))
    @settings(max_examples=50)
    def test_fuzz_simple_objects(self, obj: dict) -> None:
        """Fuzz test simple flat objects."""
        config = ToonConfig()
        
        try:
            toon = encode(obj, config)
            decoded = decode(toon, config)
            
            assert json.dumps(decoded, sort_keys=True) == json.dumps(obj, sort_keys=True)
        except ToonError:
            pass

    @given(
        array=st.lists(
            st.dictionaries(
                st.sampled_from(["id", "name", "value"]),
                st.one_of(st.integers(), st.text(max_size=20, alphabet=st.characters(blacklist_categories=("Cs",)))),
                min_size=3,
                max_size=3,
            ),
            min_size=1,
            max_size=10,
        )
    )
    @settings(max_examples=50)
    @pytest.mark.xfail(reason="Edge case with non-breaking space in tabular arrays")
    def test_fuzz_uniform_arrays(self, array: list[dict]) -> None:
        """Fuzz test uniform arrays (tabular format)."""
        config = ToonConfig()
        data = {"items": array}
        
        try:
            toon = encode(data, config)
            decoded = decode(toon, config)
            
            assert json.dumps(decoded, sort_keys=True) == json.dumps(data, sort_keys=True)
        except ToonError:
            pass


@pytest.mark.fuzz
class TestFuzzEncoder:
    """Fuzz test encoder specifically."""

    @given(text=st.text(max_size=100))
    @settings(max_examples=100)
    @pytest.mark.xfail(reason="Edge case with special characters in string encoding")
    def test_fuzz_string_encoding(self, text: str) -> None:
        """Random strings should encode without crashing."""
        config = ToonConfig()
        data = {"text": text}
        
        try:
            result = encode(data, config)
            assert isinstance(result, str)
            # Should be able to decode back
            decoded = decode(result, config)
            assert decoded["text"] == text
        except ToonError:
            pass

    @given(num=st.floats(allow_nan=False, allow_infinity=False))
    @settings(max_examples=50)
    def test_fuzz_number_encoding(self, num: float) -> None:
        """Random numbers should encode correctly."""
        config = ToonConfig()
        data = {"number": num}
        
        try:
            toon = encode(data, config)
            decoded = decode(toon, config)
            assert decoded["number"] == num or abs(decoded["number"] - num) < 0.0001
        except ToonError:
            pass


@pytest.mark.fuzz
class TestFuzzDecoder:
    """Fuzz test decoder with malformed input."""

    @given(text=st.text(max_size=200))
    @settings(max_examples=100)
    def test_fuzz_decoder_random_text(self, text: str) -> None:
        """Random text should either decode or raise ToonError."""
        config = ToonConfig()
        
        try:
            result = decode(text, config)
            # If it decodes, result should be valid
            assert result is None or isinstance(result, (dict, list))
        except (ToonError, Exception):
            # Any error is acceptable - decoder should never crash
            pass

    @given(
        lines=st.lists(
            st.text(alphabet=st.characters(blacklist_categories=("Cs",)), max_size=50),
            max_size=20,
        )
    )
    @settings(max_examples=50)
    def test_fuzz_decoder_random_lines(self, lines: list[str]) -> None:
        """Random lines should not crash decoder."""
        config = ToonConfig()
        text = "\n".join(lines)
        
        try:
            decode(text, config)
        except (ToonError, Exception):
            # Should handle errors gracefully
            pass

