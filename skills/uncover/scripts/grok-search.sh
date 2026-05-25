#!/bin/bash
# Grok API search script for Twitter/X research
# Usage: bash grok-search.sh "your research query"

QUERY="$1"

if [ -z "$QUERY" ]; then
  echo "Usage: bash grok-search.sh \"your research query\""
  exit 1
fi

if [ -z "$GROK_API_KEY" ]; then
  # Try loading from .env in project root
  if [ -f ".env" ]; then
    export $(grep GROK_API_KEY .env | xargs)
  fi
  if [ -z "$GROK_API_KEY" ]; then
    echo "Error: GROK_API_KEY not set. Add it to .env or export it."
    exit 1
  fi
fi

curl -s https://api.x.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GROK_API_KEY" \
  -d "$(cat <<EOF
{
  "model": "grok-3-latest",
  "messages": [
    {
      "role": "system",
      "content": "You are a research assistant with access to Twitter/X. Search for real practitioner experiences and insights. Focus on builders and people with hands-on experience, not influencers or marketing accounts. Include specific tweets, threads, usernames, and dates where possible. Prioritize threads over single tweets. Note follower counts and engagement metrics as quality signals."
    },
    {
      "role": "user",
      "content": "$QUERY"
    }
  ],
  "temperature": 0.7
}
EOF
)"
