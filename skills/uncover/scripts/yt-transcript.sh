#!/bin/bash
# YouTube transcript extraction script — tiered fallback
# Usage: bash yt-transcript.sh "https://youtube.com/watch?v=VIDEO_ID"
#
# Tries in order:
#   1. Firecrawl scrape (returns transcript + metadata)
#   2. youtube-transcript-api via uvx (clean text)
#   3. yt-dlp subtitle download (SRT, needs post-processing)

VIDEO_URL="$1"
OUTPUT_DIR="/tmp/yt-transcripts"

if [ -z "$VIDEO_URL" ]; then
  echo "Usage: bash yt-transcript.sh \"https://youtube.com/watch?v=VIDEO_ID\""
  exit 1
fi

# Extract video ID for filename
VIDEO_ID=$(echo "$VIDEO_URL" | sed -n 's/.*v=\([a-zA-Z0-9_-]*\).*/\1/p')
if [ -z "$VIDEO_ID" ]; then
  VIDEO_ID=$(echo "$VIDEO_URL" | sed -n 's/.*youtu\.be\/\([a-zA-Z0-9_-]*\).*/\1/p')
fi
if [ -z "$VIDEO_ID" ]; then
  echo "Error: Could not extract video ID from URL"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
OUTPUT_FILE="$OUTPUT_DIR/${VIDEO_ID}.txt"
INFO_FILE="$OUTPUT_DIR/${VIDEO_ID}_info.txt"

# ─── Method 1: Firecrawl (preferred — transcript + metadata) ───
if command -v firecrawl &> /dev/null; then
  echo "=== Trying Firecrawl scrape ==="
  FIRECRAWL_OUT=$(firecrawl scrape "$VIDEO_URL" --format markdown 2>/dev/null)

  if echo "$FIRECRAWL_OUT" | grep -q "## Transcript"; then
    # Extract transcript section: between "## Transcript" and the next "## " heading (or "### " or end-of-content markers)
    echo "$FIRECRAWL_OUT" | sed -n '/^## Transcript$/,/^##[# ]/p' | sed '1d;$d' | \
      grep -v '^[0-9][0-9]*:[0-9][0-9]$' | \
      grep -v '^\s*$' > "$OUTPUT_FILE"

    # If the sed range didn't close (no next heading), extract and strip trailing YouTube UI cruft
    if [ ! -s "$OUTPUT_FILE" ]; then
      echo "$FIRECRAWL_OUT" | sed -n '/^## Transcript$/,$p' | sed '1d' | \
        grep -v '^[0-9][0-9]*:[0-9][0-9]$' | \
        grep -v '^\[.*\](https://' | \
        grep -v '^\!\[' | \
        grep -v '^\s*$' | \
        grep -v ' views' | \
        grep -v '^\*\*' | \
        grep -v '^No results found' | \
        grep -v '^TAP TO RETRY' | \
        grep -v '^NaN' | \
        grep -v 'auto-generated' | \
        grep -v '\\\\$' > "$OUTPUT_FILE"
    fi

    # Also clean up the primary extraction path — strip trailing YouTube UI elements
    if [ -s "$OUTPUT_FILE" ]; then
      # Remove lines that are YouTube UI artifacts (appear after transcript ends)
      sed -i '' '/^No results found$/,$d' "$OUTPUT_FILE" 2>/dev/null
      sed -i '' '/^TAP TO RETRY$/,$d' "$OUTPUT_FILE" 2>/dev/null
      sed -i '' '/^NaN/,$d' "$OUTPUT_FILE" 2>/dev/null
      sed -i '' '/^English (auto-generated)/,$d' "$OUTPUT_FILE" 2>/dev/null
    fi

    # Extract metadata (everything before transcript)
    echo "$FIRECRAWL_OUT" | sed '/^## Transcript$/,$d' > "$INFO_FILE"

    LINES=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
    if [ "$LINES" -gt 5 ]; then
      echo "=== Transcript saved to ${OUTPUT_FILE} (via Firecrawl) ==="
      echo "=== Video info saved to ${INFO_FILE} ==="
      echo "=== Lines: $LINES ==="
      exit 0
    else
      echo "Warning: Firecrawl transcript extraction yielded too few lines. Trying fallback..."
    fi
  else
    echo "Warning: Firecrawl did not return a transcript section. Trying fallback..."
  fi
fi

# ─── Method 2: youtube-transcript-api via uvx ───
if command -v uvx &> /dev/null; then
  echo "=== Trying youtube-transcript-api via uvx ==="
  TRANSCRIPT=$(uvx --from youtube-transcript-api youtube_transcript_api "$VIDEO_ID" --format text 2>/dev/null)

  if [ -n "$TRANSCRIPT" ] && [ "$(echo "$TRANSCRIPT" | wc -l)" -gt 2 ]; then
    echo "$TRANSCRIPT" > "$OUTPUT_FILE"
    echo "Video ID: $VIDEO_ID" > "$INFO_FILE"
    echo "URL: $VIDEO_URL" >> "$INFO_FILE"

    echo "=== Transcript saved to ${OUTPUT_FILE} (via youtube-transcript-api) ==="
    echo "=== Video info saved to ${INFO_FILE} ==="
    echo "=== Lines: $(wc -l < "$OUTPUT_FILE") ==="
    exit 0
  else
    echo "Warning: youtube-transcript-api failed or returned empty. Trying fallback..."
  fi
fi

# ─── Method 3: yt-dlp subtitle download ───
if command -v yt-dlp &> /dev/null; then
  YTDLP="yt-dlp"
elif python3 -m yt_dlp --version &> /dev/null 2>&1; then
  YTDLP="python3 -m yt_dlp"
else
  echo "Error: No transcript extraction method available."
  echo "Install one of:"
  echo "  - firecrawl (npm install -g @mendable/firecrawl-cli)"
  echo "  - uv (for uvx + youtube-transcript-api)"
  echo "  - yt-dlp (uv tool install yt-dlp)"
  exit 1
fi

echo "=== Trying yt-dlp subtitle download ==="

# Get video title and description
$YTDLP --print title --print description --skip-download "$VIDEO_URL" 2>/dev/null > "$INFO_FILE"

# Get auto-generated subtitles (use default client, NOT web client)
SRT_BASE="$OUTPUT_DIR/${VIDEO_ID}_srt"
$YTDLP --write-auto-sub --sub-lang en --skip-download --sub-format srt \
  -o "$SRT_BASE" "$VIDEO_URL" 2>/dev/null

SRT_FILE="${SRT_BASE}.en.srt"
if [ -f "$SRT_FILE" ]; then
  # Convert SRT to clean text (strip timestamps, sequence numbers, formatting)
  grep -v "^[0-9]*$" "$SRT_FILE" | \
  grep -v "^$" | \
  grep -v "^[0-9][0-9]:[0-9][0-9]" | \
  grep -v "^\-\->" | \
  sed 's/<[^>]*>//g' | \
  awk '!seen[$0]++' > "$OUTPUT_FILE"

  rm -f "$SRT_FILE"

  echo "=== Transcript saved to ${OUTPUT_FILE} (via yt-dlp) ==="
  echo "=== Video info saved to ${INFO_FILE} ==="
  echo "=== Lines: $(wc -l < "$OUTPUT_FILE") ==="
else
  echo "Error: No auto-generated subtitles found for this video."
  echo "The video may not have captions available."
  exit 1
fi
