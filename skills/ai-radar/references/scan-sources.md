# Scan Sources — Per-Source Strategies

Use these query templates and search strategies when running each parallel scan.

---

## 1. Twitter/X Scan (via Grok API)

**Tool:** `bash /Users/govindbajwa/.claude/skills/uncover/scripts/grok-search.sh "<query>"`

**Why:** Grok with x_search has real-time access to X posts. Best signal for what builders are actually doing/launching/reacting to RIGHT NOW.

### Default queries (general scan)

Run 3-4 of these in parallel:

```bash
bash grok-search.sh "What are the most important AI tool launches, model releases, and announcements in the last 7 days from people actually shipping production AI applications? Focus on Claude, Anthropic, OpenAI, Notion AI, MCP servers, AI agents, and developer tooling. Include URLs, dates, and what builders are saying about each one."
```

```bash
bash grok-search.sh "What new AI workflows, prompt techniques, or agent architectures are practitioners (people building real production systems) sharing on X this week? I want concrete patterns being shipped, not hot takes. Include tweet URLs and the specific patterns described."
```

```bash
bash grok-search.sh "What are the biggest recent updates to Claude (Anthropic), Claude Code, MCP servers, Notion AI, and the AI developer ecosystem in the last 7 days? I'm looking for things that affect people who build AI products with Claude as their primary LLM."
```

```bash
bash grok-search.sh "What are AI builders complaining about, fixing workarounds for, or excited about this week on X? I want the practitioner pain and excitement, not influencer marketing posts."
```

### Topic-focused queries

If user specified a topic (e.g. "agents", "models", "mcp"), use these patterns:

- **agents:** "What are the latest AI agent frameworks, agent patterns, and agent products launching this week? Focus on builders shipping real production agents. Include Claude Agent SDK, custom agents, multi-agent systems."
- **models:** "What are the latest LLM model releases, benchmark updates, and capability jumps in the last 7 days? Include pricing, context window, and performance changes."
- **mcp:** "What are the newest MCP (Model Context Protocol) server launches, integrations, and patterns this week? Who is shipping interesting MCP servers and what are they used for?"
- **notion-ai:** "What are people building with Notion AI agents and custom agents this week? Include workflow examples, automation patterns, and integration ideas."

### What to extract

For each item Grok returns, capture:
- Tweet URL (the actual link)
- Author handle and brief credibility note (builder vs influencer)
- Date
- 1-2 sentence summary of what was said/launched
- Why this matters to a builder

---

## 2. Web/Launches Scan (via Firecrawl + WebSearch)

**Tools:** `firecrawl search` and WebSearch

**Why:** Catches official product launches, blog posts, changelogs from the major AI companies. These are the source-of-truth announcements.

### Sites to scan

Run firecrawl search with these targeted queries:

```bash
firecrawl search "Anthropic new release announcement" --limit 5
firecrawl search "Claude Code update changelog 2026" --limit 5
firecrawl search "Notion AI agent launch announcement" --limit 5
firecrawl search "OpenAI new model release this week" --limit 5
firecrawl search "AI developer tools launched this week" --limit 5
firecrawl search "MCP server launch new" --limit 5
firecrawl search "Vercel AI SDK update" --limit 5
firecrawl search "Supabase AI feature launch" --limit 5
```

Also use WebSearch for queries that need recency filtering (firecrawl is sometimes stale).

### Key sources to prioritize when ranking results

| Source | What it has |
|--------|-------------|
| anthropic.com/news | Claude releases, API changes, capability updates |
| platform.openai.com | OpenAI changelog |
| notion.com/releases | Notion product releases including AI |
| vercel.com/changelog | Vercel + Next.js + AI SDK |
| supabase.com/blog | Supabase features |
| github.com/trending | What's gaining traction in code |
| Hacker News (news.ycombinator.com) | Developer signal on what matters |

### What to extract

- Source URL
- Date of post
- 2-3 sentence summary
- Direct relevance to Claude/Notion/Vercel/Supabase stack if any

---

## 3. Reddit Scan (via Firecrawl)

**Tool:** `firecrawl search` (NOT WebSearch — site:reddit.com doesn't work in WebSearch)

**Why:** Reddit has the deepest practitioner discussions. People share what's actually working, what broke, what they're excited about.

### Subreddits to scan

```bash
firecrawl search "site:reddit.com/r/ClaudeAI [topic or recent week]" --limit 10
firecrawl search "site:reddit.com/r/LocalLLaMA [topic]" --limit 10
firecrawl search "site:reddit.com/r/MachineLearning [topic]" --limit 10
firecrawl search "site:reddit.com/r/ChatGPT [topic]" --limit 10
firecrawl search "site:reddit.com/r/singularity [topic]" --limit 10
firecrawl search "site:reddit.com/r/artificial [topic]" --limit 10
firecrawl search "site:reddit.com/r/Notion [AI agents]" --limit 5
```

Default topic if no user-specified: "this week" or recent dates.

### What to extract

For top-upvoted, recent threads:
- Thread URL
- Subreddit
- Date
- Topic / title
- The 2-3 most insightful comments (paraphrased, not pasted)
- What practitioners are concluding

Filter: skip pure complaint threads, skip threads with no shipping practitioners commenting.

---

## 4. YouTube Scan

**Tools:**
- WebSearch or Firecrawl to find recent relevant videos
- `bash /Users/govindbajwa/.claude/skills/uncover/scripts/yt-transcript.sh <video-url>` to pull transcripts

**Why:** Demos, deep-dives, and walkthroughs of new tools often hit YouTube within days. Good for visual things you can't get from text.

### Search queries

```
"Claude Code tutorial 2026"
"Notion AI agents tutorial"
"new AI tool launch demo this week"
"MCP server tutorial"
"Claude API new feature walkthrough"
```

For top 3-5 videos found, pull transcripts with the yt-transcript script.

### What to extract

- Video URL
- Channel name + brief credibility note
- Upload date
- 2-3 sentence summary of what was demonstrated
- Key insight or technique shown
- Why this is worth watching (or what to skip to)

---

## Source Quality Hierarchy

When two sources conflict or you have to pick what to include:

1. **Official source** (anthropic.com, notion.com/releases, etc.) — source of truth
2. **Builder on X** with concrete code/demo + recent track record
3. **Reddit thread** with multiple practitioners corroborating
4. **YouTube tutorial** from credible channel
5. **Blog post** from established AI publication
6. **Hot take from big account** — only if it's saying something new and being widely discussed

Avoid: speculation threads, AI futurism, "AI is going to..." takes, marketing-only launch posts with no shipped product.
