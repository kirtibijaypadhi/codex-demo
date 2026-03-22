#!/usr/bin/env bash
# One-command demo server: starts the PHP built-in server for src/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

HOST="${HOST:-localhost}"
PORT="${PORT:-8080}"

echo "codex-mcp-demo — starting PHP dev server"
echo "  URL:  http://${HOST}:${PORT}/index.php"
echo "  Stop: Ctrl+C"
echo ""
echo "Quick test (in another terminal):"
echo "  curl \"http://${HOST}:${PORT}/index.php\""
echo "  curl \"http://${HOST}:${PORT}/index.php?user_id=2\""
echo ""

exec php -S "${HOST}:${PORT}" -t src
