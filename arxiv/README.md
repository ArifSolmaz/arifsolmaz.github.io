# 🪐 Exoplanet Papers - Daily arXiv Digest

Automated daily digest of exoplanet research from arXiv with AI summaries, social media posting, and Turkish translations.

🌐 **Live:** [arifsolmaz.github.io/arxiv](https://arifsolmaz.github.io/arxiv)

## Features

- **Daily arXiv fetch** from astro-ph.EP (exoplanet papers only)
- **AI summaries** for general audiences (Claude)
- **Auto-posting** to Twitter/X and Bluesky
- **Turkish news** generation
- **RSS feed** at `/arxiv/feed.xml`
- **Paper archive** with date navigation

## Schedule (Istanbul Time)

| Time | Action |
|------|--------|
| 05:00 | Fetch & summarize papers |
| 06:00 | Generate Turkish news |
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
├── news.html               # Turkish news
├── feed.xml                # RSS feed
├── data/
│   ├── papers.json         # Current papers
│   ├── arxiv_news.json     # Turkish articles
│   └── archive/            # Past days
└── scripts/
    ├── fetch_papers.py     # Fetch & summarize
    ├── post_twitter.py     # Twitter posting
    ├── post_bluesky.py     # Bluesky posting
    └── generate_turkish_news.py
```

## License

MIT

---

📄 Data from [arXiv.org](https://arxiv.org) · 🤖 Summaries by [Claude](https://anthropic.com)
