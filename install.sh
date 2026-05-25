#!/usr/bin/env bash
# Install Govind's Claude Code skills to ~/.claude/skills/
# Usage: bash install.sh [skill1 skill2 ...]  (or no args to install all 4)

set -e

SKILLS_SRC="$(cd "$(dirname "$0")/skills" && pwd)"
SKILLS_DEST="$HOME/.claude/skills"
ALL_SKILLS=(uncover crystallize eli12 ai-radar)

REQUESTED=("$@")
if [ ${#REQUESTED[@]} -eq 0 ]; then
  REQUESTED=("${ALL_SKILLS[@]}")
fi

mkdir -p "$SKILLS_DEST"

for skill in "${REQUESTED[@]}"; do
  SRC="$SKILLS_SRC/$skill"
  DEST="$SKILLS_DEST/$skill"

  if [ ! -d "$SRC" ]; then
    echo "  [skip] $skill — not found in package"
    continue
  fi

  if [ -d "$DEST" ]; then
    echo "  [update] $skill → $DEST"
  else
    echo "  [install] $skill → $DEST"
  fi

  cp -r "$SRC/" "$DEST/"
done

echo ""
echo "Done. Skills available as:"
for skill in "${REQUESTED[@]}"; do
  echo "  /$skill"
done
echo ""
echo "Note: uncover and ai-radar use the Grok API for Twitter/X search."
echo "Add your key:  export GROK_API_KEY=your_key_here  (or put it in .env)"
