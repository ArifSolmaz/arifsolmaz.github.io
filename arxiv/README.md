# 🪐 Exoplanet Papers - Daily arXiv Digest with AI Summaries

A beautiful, automated daily digest of exoplanet research papers from arXiv with **AI-generated summaries** written for general audiences, **cross-platform social posting**, and **RSS feed**.

🌐 **Live site:** [arifsolmaz.github.io/arxiv](https://arifsolmaz.github.io/arxiv)

## ✨ Features

- **Daily Updates**: Automatically fetches the latest papers from arXiv astro-ph.EP
- **AI Summaries**: Each paper gets a ~300 word summary explaining:
  - Why It Matters (big picture significance)
  - What They Did (methods in plain language)
  - Key Findings (main discoveries)
  - Looking Forward (implications)
- **RSS Feed**: Subscribe at `/arxiv/feed.xml`
- **Paper Archive**: Browse past days' papers with date navigation
- **Cross-Platform Posting**: Automated posts to Twitter/X and Bluesky
- **Telegram Notifications**: Get notified when tweets are posted
- **Smart Figure Fetching**: Extracts actual paper figures, with branded fallback cards
- **Turkish News**: Auto-generated Turkish news articles for outreach
- **Beautiful UI**: Clean design with responsive layout
- **Zero Maintenance**: GitHub Actions handles everything automatically

## 📅 Schedule (Istanbul Time, UTC+3)

| Time | Event |
|------|-------|
| 05:00 | Fetch new papers from arXiv |
| 06:00 | Generate Turkish news articles |
| 07:00-23:00 | Tweet papers (evenly distributed) |

Papers are distributed evenly throughout the day. With 15 papers, expect one tweet roughly every 64 minutes.

## 📁 File Structure

```
your-repo/
├── .github/
│   └── workflows/
│       ├── update-papers.yml      # Fetches papers (05:00 Istanbul)
│       ├── generate-turkish-news.yml  # Turkish news (06:00 Istanbul)
│       ├── tweet-paper.yml        # Twitter posting (07:00-23:00 Istanbul)
│       └── post-bluesky.yml       # Bluesky posting
├── arxiv/
│   ├── index.html                 # Main webpage
│   ├── feed.xml                   # RSS feed (auto-generated)
│   ├── news.html                  # Turkish news page
│   ├── admin.html                 # Admin panel for corrections
│   ├── data/
│   │   ├── papers.json            # Today's papers
│   │   ├── tweeted.json           # Tweet tracking
│   │   ├── bluesky_posted.json    # Bluesky tracking
│   │   ├── arxiv_news.json        # Turkish news data
│   │   └── archive/
│   │       ├── index.json         # Archive date list
│   │       └── YYYY-MM-DD.json    # Daily archives
│   └── scripts/
│       ├── fetch_papers.py        # Fetch + summarize papers
│       ├── generate_turkish_news.py
│       ├── generate_rss.py        # RSS feed generator
│       ├── archive_papers.py      # Daily archiver
│       ├── post_twitter.py        # Twitter posting
│       └── post_bluesky.py        # Bluesky posting
```

## 🚀 Setup Instructions

### Step 1: Add Required Secrets

Go to **Settings** → **Secrets and variables** → **Actions** and add:

| Secret | Description |
|--------|-------------|
| `ANTHROPIC_API_KEY` | For AI summaries |
| `TWITTER_API_KEY` | Twitter API |
| `TWITTER_API_SECRET` | Twitter API |
| `TWITTER_ACCESS_TOKEN` | Twitter API |
| `TWITTER_ACCESS_SECRET` | Twitter API |
| `TELEGRAM_BOT_TOKEN` | From @BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID |
| `BLUESKY_HANDLE` | e.g., `yourname.bsky.social` |
| `BLUESKY_PASSWORD` | App password (not main password!) |

### Step 2: Optional Variables

Go to **Settings** → **Variables** → **Actions**:

| Variable | Value | Description |
|----------|-------|-------------|
| `TWITTER_PREMIUM` | `true` or `plus` | Enable longer tweets |

### Step 3: Run Initial Update

1. Go to **Actions** → **Update Exoplanet Papers**
2. Click **Run workflow**

## 📡 RSS Feed

Subscribe to updates at:
```
https://arifsolmaz.github.io/arxiv/feed.xml
```

Works with any RSS reader (Feedly, Inoreader, NetNewsWire, etc.)

## 🦋 Bluesky Setup

1. Go to Bluesky → **Settings** → **App Passwords**
2. Create new app password named "GitHub Bot"
3. Add to GitHub Secrets as `BLUESKY_PASSWORD`
4. Add your handle as `BLUESKY_HANDLE` (e.g., `yourname.bsky.social`)

## 📱 Telegram Notifications

Get notified when tweets are posted:

1. Message [@BotFather](https://t.me/botfather) → `/newbot`
2. Get your chat ID from [@userinfobot](https://t.me/userinfobot)
3. Add `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` to GitHub Secrets

## 🧪 Testing Locally

```bash
# Install dependencies
pip install requests anthropic tweepy pillow atproto

# Check tweet timing (won't actually tweet without credentials)
python arxiv/scripts/post_twitter.py

# Test paper fetching
python arxiv/scripts/fetch_papers.py
```

## 🏷️ Dynamic Hashtags

Hashtags are automatically extracted (2-4 max):

| Category | Example Hashtags |
|----------|------------------|
| Telescopes | #JWST #TESS #Kepler #Hubble |
| Planet Types | #HotJupiter #SuperEarth #SubNeptune |
| Habitability | #HabitableZone #Biosignatures |
| Systems | #TRAPPIST1 #ProximaCentauri |

## 📝 Tweet Format

**Tweet 1** (with figure/card image):
```
[Paper Title]

[Author et al.]

[Hook: attention-grabbing finding]
[Claim: what's new]
[Evidence: specific detail]

[Question: invite discussion]
```

**Tweet 2** (reply):
```
📄 arXiv: [link]
📖 Full summary: [page link]

#Exoplanets #JWST
```

## 💰 Cost Estimate

- ~$0.003-0.005 per paper summary
- ~$0.001-0.002 per tweet hook
- ~$0.002-0.004 per Turkish news article
- **~$2-4 per month** total

## 🔧 Troubleshooting

### No tweets posting
- Check if within tweet window (07:00-23:00 Istanbul)
- Run `python arxiv/scripts/post_twitter.py` locally to see timing

### Twitter 403 Forbidden
- App needs Read and Write permissions
- Regenerate tokens after changing permissions

### Telegram not working
- Verify chat ID with test: `curl "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<ID>&text=test"`
- Make sure you started a conversation with the bot first

### Bluesky not posting
- Use app password, not main password
- Check handle format (include `.bsky.social`)

### Figures not loading
- Script tries: stored URL → arXiv HTML → ar5iv → fallback card
- Some papers only have PDFs (no extractable figures)

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- Paper data from [arXiv.org](https://arxiv.org)
- AI summaries by [Claude](https://anthropic.com) (Anthropic)
- Built for the exoplanet research community 🪐

---

**Follow for updates:**
- 🐦 Twitter/X: [@arifsolmaz](https://x.com/arifsolmaz)
- 🦋 Bluesky: [@arifsolmaz.bsky.social](https://bsky.app/profile/arifsolmaz.bsky.social)
