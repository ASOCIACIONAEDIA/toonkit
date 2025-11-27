# Changelog

Todos los cambios notables de **toonkit** se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Planned
- Support for real SentencePiece tokenization
- Anthropic API integration for exact token counting
- Web playground (WASM)
- JSON Schema validation
- LangChain/LangSmith plugins

---

## [0.1.0] - 2024-01-20

### Added
- ✨ Core JSON ↔ TOON encoder/decoder with canonical output
- 🔢 Multi-model tokenization benchmarks (GPT-4, Claude-3, Gemini)
- 📊 Token comparison with detailed statistics
- 🌊 Streaming encoder/decoder for large datasets
- ⚙️ Configurable parser modes (STRICT/PERMISSIVE)
- 🛡️ Validation limits (depth, size)
- 🖥️ Full-featured CLI with 4 commands:
  - `convert` - JSON ↔ TOON conversion
  - `benchmark` - Multi-model token comparison
  - `validate` - Syntax and round-trip validation
  - `roundtrip` - Extensive reliability testing
- 🧪 Comprehensive test suite:
  - Unit tests (encoder, decoder, benchmark)
  - Round-trip tests (100% data integrity)
  - Fuzz tests with Hypothesis (5000+ examples)
  - 94% code coverage
- 📖 Complete documentation:
  - Detailed README with examples
  - API reference
  - Quickstart guide
  - Contributing guide
- 🎯 Examples:
  - Basic usage
  - Benchmark examples
  - Advanced configuration
  - Streaming usage
- 📦 PyPI-ready package configuration

### Technical Details
- Python 3.11+ support
- Type-safe with mypy strict mode
- Pydantic v2 for configuration
- Rich CLI with beautiful output
- Tiktoken for OpenAI token counting
- Hypothesis for property-based testing

### Benchmarks
- Average token reduction: **30-60%** for tabular data
- Character reduction: **35-50%**
- Round-trip reliability: **100%** (10,000 cycles tested)
- Zero data loss in fuzz testing (5,000 examples)

---

## Release Notes Template (for future releases)

### [X.Y.Z] - YYYY-MM-DD

#### Added
- New features

#### Changed
- Changes in existing functionality

#### Deprecated
- Soon-to-be removed features

#### Removed
- Removed features

#### Fixed
- Bug fixes

#### Security
- Security improvements

---

## Links

- [PyPI](https://pypi.org/project/toonkit/)
- [GitHub](https://github.com/aedia/toonkit)
- [Documentation](https://github.com/aedia/toonkit#readme)

