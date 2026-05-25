# Report JSON Schema

The PDF generator script (`scripts/generate_pdf.py`) reads a JSON file with this structure.

## Schema

```json
{
  "metadata": {
    "date": "2026-04-13",
    "period": "Apr 6 - Apr 13, 2026",
    "topic": "general",
    "generated_at": "2026-04-13T10:30:00Z"
  },
  "headlines": [
    {
      "text": "Anthropic released Claude Sonnet 4.6 with 1M context and major coding improvements.",
      "tag": "Models"
    }
  ],
  "sections": [
    {
      "id": "models",
      "title": "New Models & Capabilities",
      "icon": "◆",
      "items": [
        {
          "title": "Claude Sonnet 4.6",
          "what": "Anthropic released Sonnet 4.6 with a 1M token context window and major improvements on coding benchmarks.",
          "matters": "If you're using Sonnet 4.5 in Claude Code, you should test 4.6 immediately — coding tasks improved 12% on SWE-bench.",
          "your_lens": "Direct upgrade for all your Claude Code usage. Larger context means better Notion workspace operations.",
          "source_url": "https://anthropic.com/news/claude-sonnet-4-6",
          "source_label": "anthropic.com",
          "date": "2026-04-10"
        }
      ]
    },
    {
      "id": "tools",
      "title": "Tools & Launches",
      "icon": "▲",
      "items": []
    },
    {
      "id": "infra",
      "title": "Infrastructure & Developer",
      "icon": "■",
      "items": []
    },
    {
      "id": "patterns",
      "title": "How People Are Using It",
      "icon": "●",
      "items": [
        {
          "title": "Multi-agent code review pattern",
          "what": "Builders are deploying parallel Claude agents (one for security, one for performance, one for style) reviewing the same PR.",
          "matters": "Catches more issues than single-agent review. Pattern is being adopted by teams shipping production AI products.",
          "your_lens": "Could apply this to your Quality Gate (S19) for AI-generated code before peer review.",
          "source_url": "https://twitter.com/example/status/...",
          "source_label": "@builder on X",
          "date": "2026-04-11"
        }
      ]
    },
    {
      "id": "business",
      "title": "Business & Market",
      "icon": "◇",
      "items": []
    },
    {
      "id": "watch",
      "title": "What to Watch",
      "icon": "△",
      "items": []
    },
    {
      "id": "ignore",
      "title": "What to Ignore",
      "icon": "✕",
      "items": []
    }
  ],
  "footer": {
    "user_stack": "Claude · Notion · Slack · Next.js · Vercel · Supabase · n8n · Firecrawl",
    "sources_scanned": ["Twitter/X (Grok)", "YouTube", "Reddit", "Web (Firecrawl + WebSearch)"]
  }
}
```

## Field Notes

- `metadata.date` — report date (YYYY-MM-DD)
- `metadata.period` — human-readable date range covered
- `metadata.topic` — "general" or specific topic if focused scan
- `headlines` — 3-5 short one-sentence highlights for the cover
- `sections` — array of report sections, in order
- Each section has an `id`, `title`, optional `icon` (single character), and `items` array
- Empty sections (`items: []`) are skipped in the PDF
- Each item has:
  - `title` — bolded item heading
  - `what` — 1-2 sentences on what happened
  - `matters` — 1 sentence on why it matters generally
  - `your_lens` — 1 sentence on why it matters to BraindAI specifically (optional but recommended)
  - `source_url` — direct link
  - `source_label` — short display label (e.g., "anthropic.com" or "@user on X")
  - `date` — when the source was published (YYYY-MM-DD)

## Saving the Report

Save the JSON to: `output/ai-radar/ai-radar-<DATE>.json`

Then run:
```bash
python3 /Users/govindbajwa/.claude/skills/ai-radar/scripts/generate_pdf.py \
  --input output/ai-radar/ai-radar-<DATE>.json \
  --output output/ai-radar/ai-radar-<DATE>.pdf
```
