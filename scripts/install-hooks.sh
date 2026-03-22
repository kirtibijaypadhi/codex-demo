#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

git -C "$ROOT" config core.hooksPath .githooks

echo "Installed repo-local Git hooks."
echo "Active hooks path: .githooks"
echo "The pre-push hook will refresh docs/push-summaries/latest.md and stop the push until you commit it."
