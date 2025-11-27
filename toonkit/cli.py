"""Command-line interface for toonkit."""

import json
import sys
from pathlib import Path
from typing import Any

import click
from rich.console import Console
from rich.table import Table

from toonkit import __version__
from toonkit.benchmark.tokenizer import ModelName, TokenBenchmark, compare_formats
from toonkit.core.decoder import decode
from toonkit.core.encoder import encode
from toonkit.core.types import ParserMode, ToonConfig

console = Console()


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """🚀 Toonkit - JSON ↔ TOON converter with multi-model benchmarking."""
    pass


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output file (default: stdout)")
@click.option(
    "-f",
    "--format",
    type=click.Choice(["toon", "json"], case_sensitive=False),
    help="Output format (auto-detected from file extension if not specified)",
)
@click.option("--sort-keys/--no-sort-keys", default=True, help="Sort keys in TOON output")
@click.option(
    "--mode",
    type=click.Choice(["strict", "permissive"], case_sensitive=False),
    default="strict",
    help="Parser mode",
)
def convert(
    input_file: str, output: str | None, format: str | None, sort_keys: bool, mode: str
) -> None:
    """Convert between JSON and TOON formats.
    
    Auto-detects input format and converts to the other format.
    
    Examples:
    
        \b
        # JSON → TOON
        toonkit convert data.json -o data.toon
        
        \b
        # TOON → JSON
        toonkit convert data.toon -o data.json
        
        \b
        # To stdout
        toonkit convert data.json
    """
    input_path = Path(input_file)
    input_text = input_path.read_text(encoding="utf-8")

    # Auto-detect input format
    is_json_input = input_path.suffix.lower() == ".json" or input_text.strip().startswith("{")

    # Determine output format
    if format:
        output_format = format.lower()
    elif output:
        output_format = "json" if Path(output).suffix.lower() == ".json" else "toon"
    else:
        output_format = "toon" if is_json_input else "json"

    config = ToonConfig(sort_keys=sort_keys, mode=ParserMode(mode))

    try:
        if is_json_input:
            # JSON → TOON or JSON (identity)
            data = json.loads(input_text)
            if output_format == "toon":
                result = encode(data, config)
            else:
                result = json.dumps(data, indent=2)
        else:
            # TOON → JSON or TOON (identity)
            data = decode(input_text, config)
            if output_format == "json":
                result = json.dumps(data, indent=2)
            else:
                result = encode(data, config)

        if output:
            Path(output).write_text(result, encoding="utf-8")
            console.print(f"✅ Converted to {output}", style="green")
        else:
            console.print(result)

    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "-m",
    "--model",
    type=click.Choice(["gpt-4", "gpt-3.5-turbo", "claude-3", "claude-2", "gemini-pro"]),
    default="gpt-4",
    help="LLM model for token counting",
)
@click.option("--all-models", is_flag=True, help="Benchmark across all supported models")
def benchmark(input_file: str, model: str, all_models: bool) -> None:
    """Benchmark JSON vs TOON token usage.
    
    Shows token counts, character counts, and reduction percentages
    for different LLM models.
    
    Examples:
    
        \b
        # Single model
        toonkit benchmark data.json -m gpt-4
        
        \b
        # All models
        toonkit benchmark data.json --all-models
    """
    input_path = Path(input_file)
    input_text = input_path.read_text(encoding="utf-8")

    try:
        # Parse input
        if input_path.suffix.lower() == ".json" or input_text.strip().startswith("{"):
            data = json.loads(input_text)
        else:
            data = decode(input_text)

        if all_models:
            models: list[ModelName] = ["gpt-4", "gpt-3.5-turbo", "claude-3", "gemini-pro"]
            results = compare_formats(data, models)

            # Create comparison table
            table = Table(title="🔬 Multi-Model Token Comparison", show_header=True)
            table.add_column("Model", style="cyan")
            table.add_column("JSON Tokens", justify="right")
            table.add_column("TOON Tokens", justify="right")
            table.add_column("Reduction", justify="right", style="green")
            table.add_column("Speedup", justify="right")

            for model_name, result in results.items():
                table.add_row(
                    model_name,
                    str(result.json_stats.token_count),
                    str(result.toon_stats.token_count),
                    f"{result.token_reduction_pct:.1f}%",
                    f"{result.speedup:.2f}x",
                )

            console.print(table)
        else:
            # Single model detailed output
            bench = TokenBenchmark()
            result = bench.compare(data, model)  # type: ignore
            console.print(result)

    except Exception as e:
        console.print(f"❌ Error: {e}", style="red")
        sys.exit(1)


@main.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--mode",
    type=click.Choice(["strict", "permissive"], case_sensitive=False),
    default="strict",
    help="Validation mode",
)
def validate(input_file: str, mode: str) -> None:
    """Validate TOON syntax and test round-trip conversion.
    
    Tests:
    - TOON syntax validity
    - JSON → TOON → JSON round-trip consistency
    - Data integrity
    
    Examples:
    
        \b
        toonkit validate data.toon
        toonkit validate data.json --mode permissive
    """
    input_path = Path(input_file)
    input_text = input_path.read_text(encoding="utf-8")

    config = ToonConfig(mode=ParserMode(mode))

    try:
        # Determine format
        is_json = input_path.suffix.lower() == ".json" or input_text.strip().startswith("{")

        if is_json:
            original_data = json.loads(input_text)
            console.print("📄 Input: JSON", style="blue")
        else:
            original_data = decode(input_text, config)
            console.print("📄 Input: TOON", style="blue")

        # Round-trip test
        console.print("\n🔄 Testing round-trip conversion...", style="yellow")

        toon_encoded = encode(original_data, config)
        decoded_data = decode(toon_encoded, config)
        json_reencoded = json.dumps(decoded_data, sort_keys=True)
        original_json = json.dumps(original_data, sort_keys=True)

        if json_reencoded == original_json:
            console.print("✅ Round-trip PASSED - Data integrity preserved", style="green bold")
        else:
            console.print("❌ Round-trip FAILED - Data mismatch detected", style="red bold")
            console.print("\n🔍 Differences found:")
            console.print(f"Original keys: {set(original_data.keys())}")
            console.print(f"Decoded keys: {set(decoded_data.keys())}")
            sys.exit(1)

        # Show stats
        console.print("\n📊 Statistics:", style="blue")
        console.print(f"  Original size: {len(input_text)} chars")
        console.print(f"  TOON size: {len(toon_encoded)} chars")
        reduction = (len(input_text) - len(toon_encoded)) / len(input_text) * 100
        console.print(f"  Reduction: {reduction:+.1f}%")

    except Exception as e:
        console.print(f"❌ Validation failed: {e}", style="red bold")
        sys.exit(1)


@main.command()
@click.argument("json_file", type=click.Path(exists=True))
@click.option("-n", "--iterations", default=100, help="Number of test iterations")
def roundtrip(json_file: str, iterations: int) -> None:
    """Run extensive round-trip tests to verify encoding stability.
    
    Performs multiple encode/decode cycles and reports any inconsistencies.
    
    Examples:
    
        \b
        toonkit roundtrip data.json -n 1000
    """
    input_path = Path(json_file)
    data = json.loads(input_path.read_text(encoding="utf-8"))

    console.print(f"🔁 Running {iterations} round-trip tests...\n", style="yellow")

    config = ToonConfig()
    errors = 0

    with console.status("[bold green]Testing...") as status:
        for i in range(iterations):
            try:
                toon = encode(data, config)
                decoded = decode(toon, config)

                if json.dumps(decoded, sort_keys=True) != json.dumps(data, sort_keys=True):
                    errors += 1
                    console.print(f"❌ Iteration {i + 1}: Data mismatch", style="red")

                if (i + 1) % 10 == 0:
                    status.update(f"[bold green]Completed {i + 1}/{iterations} tests")

            except Exception as e:
                errors += 1
                console.print(f"❌ Iteration {i + 1}: {e}", style="red")

    if errors == 0:
        console.print(
            f"\n✅ All {iterations} round-trips PASSED - 100% reliability!", style="green bold"
        )
    else:
        console.print(
            f"\n❌ {errors}/{iterations} tests FAILED ({errors/iterations*100:.1f}% error rate)",
            style="red bold",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()

