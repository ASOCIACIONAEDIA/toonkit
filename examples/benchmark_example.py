"""Example: Benchmarking JSON vs TOON across models."""

from toonkit.benchmark import TokenBenchmark, compare_formats

# Create realistic API response data
data = {
    "products": [
        {
            "id": i,
            "name": f"Product {i}",
            "description": f"High-quality product number {i}",
            "price": 99.99 + i * 10,
            "in_stock": i % 2 == 0,
            "category": "electronics" if i % 3 == 0 else "accessories",
        }
        for i in range(50)
    ],
    "metadata": {
        "total": 50,
        "page": 1,
        "per_page": 50,
    }
}

print("🔬 Benchmarking JSON vs TOON\n")

# Single model comparison
print("1. GPT-4 Comparison:")
print("-" * 60)
benchmark = TokenBenchmark()
result = benchmark.compare(data, model="gpt-4")
print(result)
print()

# Multi-model comparison
print("\n2. Multi-Model Comparison:")
print("-" * 60)
results = compare_formats(data, models=["gpt-4", "claude-3", "gemini-pro"])

for model, result in results.items():
    print(f"\n{model.upper()}:")
    print(f"  JSON:  {result.json_stats.token_count:,} tokens")
    print(f"  TOON:  {result.toon_stats.token_count:,} tokens")
    print(f"  Saved: {result.token_reduction_pct:.1f}% ({result.json_stats.token_count - result.toon_stats.token_count:,} tokens)")
    
# Calculate cost savings (assuming $0.03 per 1K tokens for GPT-4)
gpt4_result = results["gpt-4"]
tokens_saved = gpt4_result.json_stats.token_count - gpt4_result.toon_stats.token_count
cost_per_1k = 0.03
cost_saved = (tokens_saved / 1000) * cost_per_1k

print(f"\n💰 Cost Savings (GPT-4 @ ${cost_per_1k}/1K tokens):")
print(f"   Tokens saved: {tokens_saved:,}")
print(f"   Cost saved per request: ${cost_saved:.4f}")
print(f"   Cost saved per 1M requests: ${cost_saved * 1_000_000:,.2f}")

