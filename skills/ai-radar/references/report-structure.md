# Report Structure

The fast-mode report has 7 sections. Aim for 10-15 items total across all sections. Quality over quantity.

---

## Section 1: HEADLINES

3-5 one-sentence summaries of the biggest things this period. This is the "if you only read one thing" section.

**Format per headline:**
- One crisp sentence
- Bold the subject (model name, tool, company)
- Note significance briefly

**Example:**
- **Anthropic** released Claude Sonnet 4.6 with 1M context and major coding improvements — most builders are switching defaults.
- **MCP** ecosystem hit 200+ servers; Notion, Slack, GitHub now have official ones in Claude Code.

---

## Section 2: NEW MODELS & CAPABILITIES

New model releases, major capability updates, benchmark shifts.

**Per item:**
- **Title** (Model name + version)
- **What changed:** 1-2 sentences
- **What it enables:** 1 sentence
- **Why it matters to you:** 1 sentence specific to BraindAI's stack/clients
- **Source:** URL

**Filter:** Only include models you'd actually consider switching to or using. Skip incremental academic improvements.

---

## Section 3: TOOLS & LAUNCHES

New developer tools, platforms, SDKs, APIs, products relevant to building with AI.

**Per item:**
- **Title** (Product name)
- **What it is:** 1-2 sentences
- **What it does for builders:** 1 sentence
- **Why it matters to you:** 1 sentence (especially if it touches Claude/Notion/Vercel/Supabase/n8n)
- **Pricing note:** if relevant
- **Source:** URL

**Filter:** Shipped products only. No vaporware. No "coming soon" announcements unless it's from a major player and timing is firm.

---

## Section 4: INFRASTRUCTURE & DEVELOPER

Framework updates, MCP servers, integration patterns, deployment tools, things that affect HOW you build.

**Per item:**
- **Title**
- **What changed:** 1-2 sentences
- **Why it matters:** 1 sentence
- **Source:** URL

**Examples of what fits here:**
- Claude Code update with new feature
- New MCP server worth installing
- Vercel AI SDK update
- New Notion AI agent capability
- New Claude Agent SDK pattern
- n8n new node or integration

---

## Section 5: HOW PEOPLE ARE USING IT

Real practitioner workflows, patterns, architectures that are working. Sourced primarily from X (builders) and Reddit (deeper discussions).

**Per item:**
- **The pattern:** 1 sentence describing the workflow
- **Who's doing it:** brief credibility note (e.g., "shipped agents at scale", "100K MRR AI product")
- **Why it works:** 1-2 sentences
- **Adaptable for BraindAI:** if relevant, 1 sentence on how this could apply to your work or clients
- **Source:** URL (tweet, Reddit thread, YouTube video)

**Filter:** Only patterns from people actually shipping. Skip influencer "here's how to use AI" content with no production behind it.

---

## Section 6: BUSINESS & MARKET

Funding, acquisitions, partnerships, market shifts, regulation, things that affect the AI business landscape — especially for AI agencies/consultancies.

**Per item:**
- **What happened:** 1-2 sentences
- **Why it matters to AI agencies:** 1 sentence
- **Source:** URL

**Filter:** Skip routine funding announcements. Only include if it changes the competitive landscape, signals a market shift, or affects how clients buy.

---

## Section 7: WHAT TO WATCH

2-3 things that aren't mainstream YET but could matter in the next 30-60 days. Early signal stuff.

**Per item:**
- **The signal:** 1-2 sentences
- **Why this could matter:** 1 sentence
- **Source:** URL

This is the speculative section but grounded in real movement (e.g., a tool gaining traction with builders, an emerging pattern showing up across multiple sources).

---

## Section 8: WHAT TO IGNORE (optional, only if relevant)

1-2 things that look big but aren't actionable for the user. Helps cut through hype.

**Per item:**
- **The hype:** 1 sentence
- **Why ignore:** 1 sentence
- **Source:** URL

This is short. Use only when there's clearly something the user might think matters but doesn't.

---

## In-Chat Output Format

After the PDF is generated, this is what goes in chat:

```
📡 AI RADAR — [Date]
PDF: output/ai-radar/ai-radar-[date].pdf

📍 TOP 3 HEADLINES:
1. [Headline 1]
2. [Headline 2]
3. [Headline 3]

🎯 START HERE:
→ [Most important item] — [why it matters to YOU]
→ [Second priority item] — [why it matters to YOU]

Want to go deeper on any of these? Just say "go deeper on [item]".
```

Keep this tight. The PDF has the depth — chat is just the orientation.
