#!/usr/bin/env bash
# Govind's Skills — one-shot setup
# Run this script and it will install all skills + collect any API keys needed.
#
# Usage (after cloning):
#   bash setup.sh
#
# Or run directly without cloning first:
#   curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/govind-skills/main/setup.sh | bash

set -e

REPO_URL="https://github.com/govind-bajwa/govind-skills.git"
SKILLS_DEST="$HOME/.claude/skills"
ENV_FILE="$HOME/.claude/skills/.env"
SHELL_RC=""

# ── Detect shell rc file ───────────────────────────────
if [ -n "$ZSH_VERSION" ] || [ "$(basename "$SHELL")" = "zsh" ]; then
  SHELL_RC="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ] || [ "$(basename "$SHELL")" = "bash" ]; then
  SHELL_RC="$HOME/.bashrc"
fi

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║       Govind's Claude Code Skills Setup       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ── Step 1: Get the repo ───────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd)"
if [ -f "$SCRIPT_DIR/install.sh" ]; then
  REPO_DIR="$SCRIPT_DIR"
  echo "[1/4] Using local repo at: $REPO_DIR"
else
  REPO_DIR="$HOME/.govind-skills-tmp"
  echo "[1/4] Cloning repo..."
  rm -rf "$REPO_DIR"
  git clone "$REPO_URL" "$REPO_DIR"
fi

# ── Step 2: Install skills ─────────────────────────────
echo ""
echo "[2/4] Installing skills to $SKILLS_DEST..."
mkdir -p "$SKILLS_DEST"
bash "$REPO_DIR/install.sh"

# ── Step 3: Collect API credentials ───────────────────
echo ""
echo "[3/4] API credentials"
echo ""
echo "  The following skills use external APIs:"
echo "  • /uncover  — Twitter/X search via Grok API"
echo "  • /ai-radar — Twitter/X search via Grok API"
echo ""
echo "  You can skip any key by pressing Enter (skills work without it,"
echo "  Twitter/X results will just be skipped)."
echo ""

read -r -p "  Grok API key (from console.x.ai): " GROK_KEY

# ── Step 4: Save credentials ───────────────────────────
echo ""
echo "[4/4] Saving credentials..."

if [ -n "$GROK_KEY" ]; then
  # Write to ~/.claude/skills/.env
  mkdir -p "$(dirname "$ENV_FILE")"
  touch "$ENV_FILE"

  if grep -q "^GROK_API_KEY=" "$ENV_FILE" 2>/dev/null; then
    sed -i.bak "s|^GROK_API_KEY=.*|GROK_API_KEY=$GROK_KEY|" "$ENV_FILE"
    rm -f "${ENV_FILE}.bak"
  else
    echo "GROK_API_KEY=$GROK_KEY" >> "$ENV_FILE"
  fi

  # Also export in shell rc so it's available in new terminals
  if [ -n "$SHELL_RC" ]; then
    if ! grep -q "GROK_API_KEY" "$SHELL_RC" 2>/dev/null; then
      echo "" >> "$SHELL_RC"
      echo "# Govind Skills — Grok API" >> "$SHELL_RC"
      echo "export GROK_API_KEY=$(cat "$ENV_FILE" | grep GROK_API_KEY | cut -d= -f2)" >> "$SHELL_RC"
    fi
  fi

  echo "  Saved GROK_API_KEY to $ENV_FILE"
  [ -n "$SHELL_RC" ] && echo "  Exported in $SHELL_RC (restart terminal or: source $SHELL_RC)"
else
  echo "  Skipped Grok key — Twitter/X search will be unavailable."
fi

# ── Done ───────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║              Setup complete!                  ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "  Skills installed:"
echo "    /uncover     — deep multi-platform research"
echo "    /crystallize — turn ideas into structured plans"
echo "    /eli12       — explain anything like you're 12"
echo "    /ai-radar    — fast AI ecosystem scan"
echo ""
echo "  Use them in any Claude Code conversation by typing /skill-name"
echo ""

# Clean up temp clone if used
if [ "$REPO_DIR" = "$HOME/.govind-skills-tmp" ]; then
  rm -rf "$REPO_DIR"
fi
