# 🪐 Exoplanet Papers - Daily arXiv Digest

Automated daily digest of exoplanet research from arXiv with AI summaries, social media posting, and Turkish translations.

🌐 **Live:** [arifsolmaz.github.io/arxiv](https://arifsolmaz.github.io/arxiv)

## Features

- **Daily arXiv fetch** from astro-ph.EP (exoplanet papers only)
- **AI summaries** for general audiences (Claude), with **Turkish translations** and an EN/TR toggle on the page
- **Auto-posting** to Twitter/X and Bluesky
- **RSS feed** at `/arxiv/feed.xml`
- **Paper archive** with date navigation

## Schedule (Istanbul Time)

| Time | Action |
|------|--------|
| 05:00 | Fetch & summarize papers |
| 07:00-23:00 | Post to Twitter/Bluesky |

## Quick Setup

Add these secrets in GitHub repo settings:

```
ANTHROPIC_API_KEY     # AI summaries
TWITTER_API_KEY       # Twitter posting
TWITTER_API_SECRET
TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_SECRET
BLUESKY_HANDLE        # e.g., name.bsky.social
BLUESKY_PASSWORD      # App password
TELEGRAM_BOT_TOKEN    # Notifications (optional)
TELEGRAM_CHAT_ID
```

Then run **Actions → Update Exoplanet Papers**.

## File Structure

```
arxiv/
├── index.html              # Main page
├── feed.xml                # RSS feed
├── data/
│   ├── papers.json         # Current papers
│   └── archive/            # Past days
└── scripts/
    ├── fetch_papers.py     # Fetch & summarize
    ├── ai_content.py       # Claude: EN summary + hook + TR translation
    ├── backfill_ai.py      # Fill missing content in old days
    ├── (workflow) Backfill Summaries (EN + TR)  # Actions -> run manually
    ├── post_twitter.py     # Twitter posting
    ├── post_bluesky.py     # Bluesky posting
```

## License

MIT

---

📄 Data from [arXiv.org](https://arxiv.org) · 🤖 Summaries by [Claude](https://anthropic.com)
