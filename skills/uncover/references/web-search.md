# Web Search Strategy

Official documentation, authoritative blog posts, benchmarks, and structured knowledge. The foundation of any research — but rarely the full picture on its own.

## Tools

```bash
# Firecrawl search (returns results with optional full-page scraping)
firecrawl search "[query]" -o .firecrawl/results.json --json
firecrawl search "[query]" --scrape -o .firecrawl/scraped.json --json

# WebSearch (Claude's built-in)
# Just use WebSearch("[query]") directly

# Scrape a specific page for full content
firecrawl scrape "[url]" -o .firecrawl/page.json --json
```

## Query Strategies

| Need | Query Pattern |
|------|--------------|
| Documentation | `"[tool] documentation [specific feature]"` |
| Guides | `"[topic] guide 2025 OR 2026"` or `"[topic] best practices"` |
| Comparisons | `"[tool A] vs [tool B] benchmark"` |
| Recent developments | `"[tool] changelog"` or `"[tool] new features 2026"` |
| GitHub repos | `"[topic] github" site:github.com` |

## Quality Scoring

| Signal | Score | Why |
|--------|-------|-----|
| Official documentation | ★★★★★ | Primary source |
| In-depth practitioner blog | ★★★★☆ | Depth + experience |
| Well-cited benchmark | ★★★★☆ | Data-driven |
| Recent blog with code examples | ★★★☆☆ | Practical |
| Generic overview/listicle | ★★☆☆☆ | Surface |
| SEO content farm | ★☆☆☆☆ | Skip |

## When Web Search Is Enough

For well-documented topics with stable answers (established frameworks, mature tools), web search alone may suffice. The other platforms add value mainly when:
- The topic is emerging (docs lag behind practice)
- You need opinions, not facts
- You need implementation details docs don't cover
