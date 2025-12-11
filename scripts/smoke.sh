#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[SMOKE] running functional smoke pytest..."
PYTHONPATH=src pytest -q tests/test_functional.py

echo "[SMOKE] running in-memory transport smoke..."
PYTHONPATH=src pytest -q tests/test_inmemory_two_nodes.py::test_inmemory_transport_dispatch

echo "[SMOKE] done."
