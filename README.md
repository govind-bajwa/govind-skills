# Govind's Claude Code Skills

Four production-grade skills for Claude Code. Built and used internally at BraindAI.

## Skills

| Skill | What it does | When to use it |
|-------|-------------|----------------|
| `/uncover` | Deep multi-platform research (Twitter/X, YouTube, Reddit, web) | "research this", "what are builders saying about X", "deep dive into Y" |
| `/crystallize` | Turns vague ideas into structured, actionable briefs | "crystallize this", "help me think through", "I have this idea" |
| `/eli12` | Explains any technical concept in plain English with ASCII diagrams | "eli12", "explain this", "explain like I'm 12" |
| `/ai-radar` | Fast AI ecosystem scan — model launches, tools, framework updates | "ai radar", "what's new in AI", "catch me up on AI" |

## Install

```bash
git clone https://github.com/govind-bajwa/govind-skills.git
cd govind-skills
bash install.sh
```

Install specific skills only:

```bash
bash install.sh uncover crystallize
```

## Prerequisites

**All skills:** Claude Code CLI installed and configured.

**uncover + ai-radar:** Grok API key for Twitter/X search (optional — skills work without it but Twitter results are skipped).

```bash
export GROK_API_KEY=your_key_here
# or add to your project .env file
```

**ai-radar PDF output:** Chrome or Chromium installed (used by the PDF generator script). If missing, the report is shown in chat only.

## How skills work in Claude Code

Once installed, skills are invoked by typing their name in any Claude Code conversation:

```
/uncover  →  starts a deep research session
/crystallize  →  starts a strategic consultation
/eli12  →  explains the last thing discussed
/ai-radar  →  runs a fast AI ecosystem scan
```

Skills live at `~/.claude/skills/<name>/SKILL.md`. You can edit them to customize behavior for your context.

## What's inside each skill

```
skills/
├── uncover/
│   ├── SKILL.md              ← the skill definition Claude reads
│   ├── references/           ← per-platform research guides (Grok, YouTube, Reddit, web)
│   └── scripts/
│       ├── grok-search.sh    ← Twitter/X via Grok API
│       └── yt-transcript.sh  ← YouTube transcript extraction
├── crystallize/
│   ├── SKILL.md
│   └── references/
│       └── frameworks.md     ← SCQA, MECE, DSRP, Cynefin engine
├── eli12/
│   └── SKILL.md
└── ai-radar/
    ├── SKILL.md
    ├── references/           ← scan-sources, report-structure, report-schema
    └── scripts/
        └── generate_pdf.py   ← Chrome-based PDF generator
```
