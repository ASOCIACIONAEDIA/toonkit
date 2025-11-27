"""Example: Advanced configuration options."""

from toonkit import encode, decode, ToonConfig, ParserMode

# Sample nested data
data = {
    "company": "ACME Corp",
    "departments": [
        {"id": 1, "name": "Engineering", "budget": 500000},
        {"id": 2, "name": "Sales", "budget": 300000},
    ],
    "metadata": {
        "version": 2,
        "updated": "2024-01-15",
        "tags": ["production", "verified"]
    }
}

print("1. Canonical encoding (sorted keys):")
print("-" * 60)
canonical_config = ToonConfig(sort_keys=True)
toon1 = encode(data, canonical_config)
toon2 = encode(data, canonical_config)
print(toon1)
print(f"\n✅ Same output every time: {toon1 == toon2}")

print("\n2. Unsorted keys (insertion order):")
print("-" * 60)
unsorted_config = ToonConfig(sort_keys=False)
toon_unsorted = encode(data, unsorted_config)
print(toon_unsorted)

print("\n3. Custom indentation (4 spaces):")
print("-" * 60)
indent_config = ToonConfig(indent_size=4)
toon_indented = encode(data, indent_config)
print(toon_indented)

print("\n4. Strict vs Permissive parsing:")
print("-" * 60)

# Malformed TOON (mismatched columns)
malformed_toon = """
items[2]{id,name}:
  1,Alice
  2,Bob,extra_column
"""

# Strict mode - will fail
strict_config = ToonConfig(mode=ParserMode.STRICT)
try:
    decode(malformed_toon, strict_config)
    print("❌ Strict: Should have failed")
except Exception as e:
    print(f"✅ Strict mode rejected: {e}")

# Permissive mode - will handle gracefully
permissive_config = ToonConfig(mode=ParserMode.PERMISSIVE)
try:
    result = decode(malformed_toon, permissive_config)
    print(f"✅ Permissive mode handled it: {result}")
except Exception as e:
    print(f"❌ Permissive failed: {e}")

print("\n5. Size and depth limits:")
print("-" * 60)
limited_config = ToonConfig(max_depth=3, max_size_mb=1)

# Deep nesting (will fail)
deep_data = {"l1": {"l2": {"l3": {"l4": {"l5": "too deep"}}}}}
try:
    encode(deep_data, limited_config)
    print("❌ Should have failed depth check")
except Exception as e:
    print(f"✅ Depth limit enforced: {e}")

