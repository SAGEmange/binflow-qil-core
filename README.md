# Binflow QIL Core

Minimal Python package for **pattern-based engines** (Binflow).
Implements deterministic "pattern nodes" and a small scheduler you can extend into games, analytics, or AI tools.

## Features
- Deterministic node updates (no RNG by default)
- Pluggable states (F, S, L, P, T) for Binflow cycles
- Simple JSON **Data Pass** export (hash + timestamp) shared with chatbot/Spaces

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
python examples/run_demo.py
