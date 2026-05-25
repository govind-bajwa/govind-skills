# YouTube Research Strategy

YouTube has the deepest content — 30-60 minute tutorials, walkthroughs, and expert breakdowns that don't exist anywhere else. The transcript is the gold mine; the video description often has linked resources.

## Getting Transcripts

**Three methods available (tiered fallback — the script tries all automatically):**

### Method 1: Firecrawl scrape (preferred)
```bash
firecrawl scrape "https://www.youtube.com/watch?v=VIDEO_ID" --format markdown
```
Returns transcript + full metadata (title, channel, views, description, endscreen links) in one call. Parse the `## Transcript` section from the markdown output.

### Method 2: youtube-transcript-api via uvx
```bash
uvx --from youtube-transcript-api youtube_transcript_api VIDEO_ID --format text
```
Clean plain text, no dependencies to maintain. Fast and reliable.

### Method 3: yt-dlp (installed via uv)
```bash
yt-dlp --write-auto-sub --sub-lang en --sub-format srt --skip-download -o "/tmp/yt-VIDEO_ID" "URL"
```
Do NOT use `--extractor-args "youtube:player_client=web"` — it requires a PO token and will fail.

### Bundled script (auto-fallback across all methods):
```bash
bash .claude/skills/uncover/scripts/yt-transcript.sh "https://youtube.com/watch?v=VIDEO_ID"

# Output goes to /tmp/yt-transcripts/VIDEO_ID.txt
# Video info goes to /tmp/yt-transcripts/VIDEO_ID_info.txt
```

## Finding the Right Videos

YouTube video URLs are tricky to find via normal web search. Use this sequence:

**Step 1: Find video URLs via Firecrawl** (most reliable):
```bash
firecrawl search "[topic] tutorial site:youtube.com" --json -o .firecrawl/yt-search.json
```

**Step 2: If Firecrawl doesn't return YouTube URLs, use WebSearch with specific formatting:**
```
WebSearch("[topic] youtube.com/watch tutorial 2025 2026")
```

**Step 3: If you still don't have video URLs, ask Grok** — it can find specific YouTube videos discussed on Twitter:
```
"What YouTube videos are builders recommending about [topic]? I need the actual video URLs."
```

**Step 4: Once you have a URL, pull the transcript:**
```bash
bash .claude/skills/uncover/scripts/yt-transcript.sh "https://youtube.com/watch?v=VIDEO_ID"
```

The script auto-detects yt-dlp whether it's installed via pip (`python3 -m yt_dlp`) or as a standalone binary.

**What makes a video worth pulling the transcript for:**
- 10K+ views (enough people found it valuable)
- Recent (within 12 months for tech topics — older content decays fast)
- From a channel known for depth, not clickbait
- Title suggests hands-on experience, not just overview

## Processing Transcripts

Auto-generated transcripts are messy. Focus on extracting:
- **Key arguments and positions** — the author's main claims
- **Specific tools, commands, configurations** mentioned
- **"The thing most people get wrong is..."** moments — these are gold
- **Linked resources** mentioned verbally ("check out [tool] at [url]")

Skip: intros, sponsor segments, outros, filler. For long videos (30+ min), focus on the first 5 minutes (thesis) and sections with high information density.

## Video Description Mining

Always check descriptions for:
- GitHub repos, docs, tools linked
- Timestamps (navigate to relevant sections)
- Show notes with additional resources
- These linked resources are often more valuable than the video itself

## Quality Scoring

| Signal | Score | Why |
|--------|-------|-----|
| Deep technical tutorial from practitioner | ★★★★★ | Highest depth |
| Conference talk from recognized expert | ★★★★★ | Authority + depth |
| Comparison with real testing | ★★★★☆ | Practical evaluation |
| Walkthrough with code/demo | ★★★★☆ | Verifiable |
| Overview/explainer (no hands-on) | ★★★☆☆ | Surface |
| Listicle ("Top 10...") | ★★☆☆☆ | Low depth |
