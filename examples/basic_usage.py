"""Example: Basic usage of toonkit."""

from toonkit import encode, decode

# Sample data
data = {
    "users": [
        {"id": 1, "name": "Alice", "role": "admin", "active": True},
        {"id": 2, "name": "Bob", "role": "user", "active": False},
        {"id": 3, "name": "Charlie", "role": "user", "active": True},
    ]
}

# Convert to TOON
toon_string = encode(data)
print("TOON format:")
print(toon_string)
print()

# Convert back to JSON
decoded_data = decode(toon_string)
print("Decoded back to JSON:")
print(decoded_data)
print()

# Verify round-trip
assert decoded_data == data
print("✅ Round-trip successful!")

