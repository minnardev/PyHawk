#!/usr/bin/env bash
# PyHawk Uninstaller (macOS / Linux)

echo "🗑  Uninstalling PyHawk..."
rm -f "$HOME/.local/bin/pyhawk"
rm -f "$HOME/.local/bin/hawk"
rm -rf "$HOME/.pyhawk"
echo "✓ PyHawk files removed."
echo "Note: If you want to remove PATH export, check ~/.zshrc or ~/.bashrc."
