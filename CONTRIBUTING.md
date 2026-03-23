# Contributing to AutoForge

Thanks for your interest in contributing to AutoForge!

## Ways to Contribute

- **Report bugs** — open an issue with steps to reproduce
- **Suggest features** — open an issue describing the use case
- **Add indicators** — extend `prepare.py` with new technical indicators
- **Improve fill logic** — make `backtest.py` more realistic for specific platforms
- **Add examples** — contribute toy strategies that demonstrate different patterns
- **Write tests** — help improve test coverage
- **Fix docs** — typos, clarifications, better examples

## Getting Started

```bash
git clone https://github.com/saikodi/AutoForge.git
cd AutoForge
pip install -e ".[dev]"
```

## Guidelines

- **Keep it simple.** AutoForge is intentionally minimal. Don't add complexity unless it earns its place.
- **No proprietary strategies.** Example strategies should use well-known, publicly documented concepts (SMA crossover, RSI, etc.).
- **Match the existing style.** Look at how the current code is structured and follow the same patterns.
- **Test your changes.** Run existing examples to make sure nothing breaks.
- **One thing per PR.** Small, focused pull requests are easier to review.

## Code Style

- Python 3.10+
- No type annotations on internal code unless they clarify intent
- Docstrings on public functions
- Keep dependencies minimal (numpy + pandas core)

## What We Won't Merge

- Framework-ification — AutoForge is a few files, not a framework
- Heavy dependencies — keep the dep tree minimal
- Proprietary strategy logic or specific parameter values
- Features that only work on one platform (keep it platform-agnostic)

## Questions?

Open an issue. We're happy to help.
