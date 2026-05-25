# Grok / Twitter Research Strategy

Twitter is where builders share real-time experiences — what they're building, what broke, what actually worked. Grok has native access to Twitter data and can search/synthesize across conversations. This makes it uniquely valuable for cutting-edge topics where docs don't exist yet.

## API Setup

- **Endpoint:** `https://api.x.ai/v1/chat/completions`
- **Model:** `grok-3-latest` (or `grok-3-mini-latest` for lighter queries)
- **Auth:** Bearer token from env var `GROK_API_KEY`
- **Script:** Use `scripts/grok-search.sh` for standardized calls

## Using the Script

```bash
# Basic research query
bash .claude/skills/uncover/scripts/grok-search.sh "What are real builders saying about [TOPIC]? Find specific tweets, threads, and experiences — focus on practitioners, not influencers."

# Targeted person search
bash .claude/skills/uncover/scripts/grok-search.sh "Find tweets and threads from @username about [TOPIC]"

# Comparison research
bash .claude/skills/uncover/scripts/grok-search.sh "Find people who switched from [A] to [B]. What was their experience? Any threads about the migration?"
```

## Query Strategies

Shape your Grok prompts to find practitioners, not marketing:

| Research Need | Prompt Pattern |
|--------------|----------------|
| Builder experiences | "Find people who built with [X]. What worked, what didn't?" |
| Problems/gotchas | "What are developers struggling with when using [X]? Real complaints." |
| Comparisons | "Find people who switched from [A] to [B] or compared them. Threads preferred." |
| Cutting-edge takes | "What are the most insightful threads about [X] from the last month?" |
| Specific experts | "Find @[person]'s tweets about [X]" |

## Quality Scoring

| Signal | Score | Why |
|--------|-------|-----|
| Person is actively building with the tool | ★★★★★ | First-hand experience |
| Thread with follow-ups and discussion | ★★★★☆ | Depth + community validation |
| Recognized expert in the field | ★★★★☆ | Authority |
| High engagement from other builders | ★★★☆☆ | Community signal |
| Single tweet, no context | ★★☆☆☆ | Low depth |
| Marketing/promotional | ★☆☆☆☆ | Skip |

## Pass 2 Refinement

After Pass 1, you'll know key usernames and terminology. In Pass 2:
- Search for specific people's threads discovered in Pass 1
- Use the refined terminology practitioners actually use (often different from docs)
- Ask Grok about specific debates or tensions found in Pass 1
