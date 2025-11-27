"""Example: Streaming large datasets."""

from toonkit import encode_streaming, decode_streaming

# Generate large dataset
print("🌊 Streaming Example\n")

large_data = {
    "records": [
        {"id": i, "value": f"record_{i}", "score": i * 1.5}
        for i in range(1000)
    ]
}

print("1. Streaming encoder (line-by-line):")
print("-" * 60)

lines = []
chunk_count = 0

for line in encode_streaming(large_data):
    lines.append(line)
    chunk_count += 1
    
    # Print first few and last few lines
    if chunk_count <= 5:
        print(f"  Line {chunk_count}: {line[:60]}...")

print(f"  ... ({chunk_count - 10} more lines) ...")

# Show last few lines
for i, line in enumerate(lines[-5:], start=chunk_count-4):
    print(f"  Line {i}: {line[:60]}...")

print(f"\n✅ Streamed {chunk_count} lines")

print("\n2. Streaming decoder (from iterator):")
print("-" * 60)

decoded_data = decode_streaming(iter(lines))
print(f"✅ Decoded {len(decoded_data['records'])} records")
print(f"   First record: {decoded_data['records'][0]}")
print(f"   Last record: {decoded_data['records'][-1]}")

print("\n3. Use case - Processing chunks from API:")
print("-" * 60)

def fetch_data_chunks():
    """Simulate API that returns data in chunks."""
    for i in range(5):
        yield {
            "batch": i,
            "items": [{"id": i*10 + j, "name": f"Item {i*10+j}"} for j in range(10)]
        }

# Stream encode each chunk
print("Processing chunks:")
for chunk in fetch_data_chunks():
    lines = list(encode_streaming(chunk))
    print(f"  Batch {chunk['batch']}: {len(lines)} lines encoded")

print("\n✅ All chunks processed")

