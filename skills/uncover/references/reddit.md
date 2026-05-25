# Reddit Research Strategy

Reddit is where people are honest. No personal brand to protect, no algorithm to game. The comment sections often contain more value than the original posts — especially for "should I use X?" questions.

## How to Search and Scrape

**Use Firecrawl CLI for Reddit — NOT WebSearch.** WebSearch with `site:reddit.com` does not reliably return actual Reddit thread URLs. Firecrawl's search and scrape functions work much better for Reddit content.

```bash
# Step 1: Search for relevant threads (use Firecrawl CLI, not WebSearch)
firecrawl search "site:reddit.com r/[subreddit] [topic]" -o .firecrawl/reddit-results.json --json

# Step 2: Scrape a specific thread (gets post + all comments)
firecrawl scrape "https://reddit.com/r/[sub]/comments/[id]/[title]" -o .firecrawl/reddit-thread.json --json

# Step 3: If Firecrawl search doesn't return Reddit URLs, try scraping known subreddit search pages directly:
firecrawl scrape "https://www.reddit.com/r/[subreddit]/search/?q=[topic]&sort=relevance&t=year" -o .firecrawl/reddit-search.json --json
```

**Fallback if Firecrawl is unavailable:** Use WebSearch to find Reddit content indirectly through articles that cite Reddit discussions. Many comparison articles aggregate Reddit sentiment.

## Subreddit Targeting

| Domain | Subreddits |
|--------|-----------|
| AI/ML tools | r/LocalLLaMA, r/ClaudeAI, r/ChatGPT, r/MachineLearning |
| Web dev | r/webdev, r/nextjs, r/reactjs, r/frontend |
| DevOps/infra | r/devops, r/selfhosted, r/kubernetes |
| Startups/SaaS | r/SaaS, r/startups, r/Entrepreneur, r/indiehackers |
| Marketing | r/digital_marketing, r/SEO, r/socialmedia |
| General tech | r/programming, r/technology, r/ExperiencedDevs |
| Claude Code | r/ClaudeAI, r/AnthropicAI |

## Query Strategies

| Need | Query Pattern |
|------|--------------|
| Opinions | `"[tool] worth it"` or `"[tool] experience"` |
| Comparisons | `"[tool A] vs [tool B]"` or `"switched from [A] to [B]"` |
| Problems | `"[tool] issues"` or `"[tool] frustrating"` |
| Alternatives | `"[tool] alternative"` or `"instead of [tool]"` |

## What to Extract

- The original question/post (sets context)
- Top 3-5 comments by upvotes (community consensus)
- Contrarian comments that still got upvoted (valuable dissent)
- Specific tools, repos, resources mentioned in comments

## Quality Scoring

| Signal | Score | Why |
|--------|-------|-----|
| 50+ upvotes + deep thread | ★★★★★ | Community-validated |
| Comment from someone who built with it | ★★★★☆ | First-hand |
| Detailed comparison with data | ★★★★☆ | Evidence-based |
| Recent post (< 6 months) with discussion | ★★★☆☆ | Current |
| Old post (> 1 year) | ★★☆☆☆ | May be outdated |
| No comments | ★☆☆☆☆ | No validation |
