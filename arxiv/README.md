# 🪐 Exoplanet Papers - Daily arXiv Digest with AI Summaries

A beautiful, automated daily digest of exoplanet research papers from arXiv with **AI-generated summaries** written for general audiences, **Turkish news translations**, and **optimized Twitter engagement**.

🌐 **Live Site**: [arifsolmaz.github.io/arxiv](https://arifsolmaz.github.io/arxiv)  
🇹🇷 **Turkish News**: [arifsolmaz.github.io/news.html](https://arifsolmaz.github.io/news.html)

## ✨ Features

### 📰 Daily Paper Digest
- **Daily Updates**: Automatically fetches papers from arXiv astro-ph.EP RSS feed
- **Archive System**: Browse papers by date with Prev/Next navigation
- **Smart Classification**: Improved detection of exoplanet-focused papers
- **AI Summaries**: Each paper gets a ~300 word summary explaining:
  - Why It Matters (big picture significance)
  - What They Did (methods in plain language)
  - Key Findings (main discoveries)
  - Looking Forward (implications)

### 🇹🇷 Turkish News Page
- **Auto-Translation**: Generates Turkish press-release style news articles
- **Terminology**: Proper Turkish terms (ötegezegen, atmosfer, etc.)
- **Tag-based Filtering**: Filter news by topic tags
- **Admin Panel**: Direct editing via GitHub API

### 🐦 Twitter Integration
- **2-Tweet Threads**: Hook + content (with image), then links + hashtags
- **Smart Selection**: Papers ranked by "tweetability" score
- **Time-Based Posting**: Exoplanet papers during PST prime time
- **Real Figures**: Fetches actual paper figures from arXiv HTML
- **Fallback Cards**: Generates branded cards when no figure available

### 🖼️ Figure Detection
- Fetches Figure 1 from arXiv HTML beta pages
- Falls back to ar5iv.org rendering
- Topic-based fallback images (JWST, habitable zones, etc.)
- Correct URL construction for relative paths

## 📁 File Structure

```
arifsolmaz.github.io/
├── .github/
│   └── workflows/
│       ├── update-papers.yml        # Fetches papers daily at 02:00 UTC
│       ├── tweet-paper.yml          # Tweets hourly during prime time
│       └── generate-turkish-news.yml # Turkish news at 03:00 UTC
├── arxiv/
│   ├── index.html                   # Main webpage with date picker
│   ├── data/
│   │   ├── papers.json              # Current day's papers
│   │   ├── tweeted.json             # Tracks tweeted papers
│   │   └── archive/
│   │       ├── index.json           # List of available dates
│   │       ├── 2026-01-19.json      # Papers for specific date
│   │       └── ...                  # Up to 90 days history
│   └── scripts/
│       ├── fetch_papers.py          # Fetches papers, generates summaries
│       ├── post_twitter.py          # Posts as 2-tweet thread
│       ├── generate_turkish_news.py # Creates Turkish news articles
│       └── split_archive.py         # Utility: split papers by date
├── news.html                        # Turkish news page
└── admin.html                       # Admin panel for editing
```

## 🚀 Setup Instructions

### Step 1: Add Repository Secrets

Go to **Settings** → **Secrets and variables** → **Actions** and add:

| Secret Name | Required | Description |
|-------------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ | For AI summaries |
| `TWITTER_API_KEY` | Optional | For Twitter posting |
| `TWITTER_API_SECRET` | Optional | For Twitter posting |
| `TWITTER_ACCESS_TOKEN` | Optional | For Twitter posting |
| `TWITTER_ACCESS_SECRET` | Optional | For Twitter posting |

### Step 2: Enable Workflows

1. Go to **Actions** tab
2. Enable workflows if prompted
3. Run **Update Exoplanet Papers** manually for first run

### Step 3: (Optional) Twitter Premium

Add repository variable `TWITTER_PREMIUM` = `true` for longer tweets.

## 🔄 Workflow Schedule

| Workflow | Schedule (UTC) | Description |
|----------|----------------|-------------|
| Update Papers | 02:00 Mon-Fri | Fetch new papers after arXiv announces |
| Tweet Paper | Hourly 9-23 | Tweet one paper per hour |
| Turkish News | 03:00 Mon-Fri | Generate Turkish translations |

*Note: arXiv announces papers at 20:00 ET (01:00 UTC), Mon-Fri only.*

## 🏷️ Exoplanet Classification

Papers are classified as "exoplanet-focused" based on keywords:

| Category | Keywords |
|----------|----------|
| Core Terms | exoplanet, extrasolar planet |
| Planet Types | hot jupiter, super-earth, sub-neptune |
| Habitability | habitable zone, biosignature |
| Methods | microlensing planet, transiting planet, radial velocity |
| Systems | TRAPPIST-1, WASP-, TOI-, Kepler- |
| Atmospheres | transmission spectrum, planetary atmosphere |

## 🐦 Tweet Format

### Tweet 1 (with figure image)
```
[Paper Title]

[Author et al.]

[Hook: attention-grabbing finding]

[Claim: what's new]

[Evidence: specific detail]

[Question: invite discussion]
```

### Tweet 2 (reply)
```
📄 arXiv: [link]
📖 Full summary: [page link]

#Exoplanets #Astronomy #JWST
```

## 🧪 Local Testing

```bash
# Install dependencies
pip install requests anthropic tweepy pillow

# Set API key
export ANTHROPIC_API_KEY='your-key'

# Fetch papers
cd arxiv/scripts
python fetch_papers.py

# Test figure detection
python test_figure_fetch.py

# Split existing papers into daily archives
python split_archive.py
```

## 💰 Cost Estimate

- ~$0.003-0.005 per paper summary
- ~$0.001-0.002 per tweet hook
- ~$0.002-0.004 per Turkish news article
- **~$2-4 per month** total (typical usage)

## 🔧 Troubleshooting

### Papers from wrong date showing
- The fetch script now uses RSS feed only (today's papers)
- API fallback only if RSS fails completely

### Figures not loading
- Check if arXiv has HTML version: `arxiv.org/html/[paper_id]`
- Script tries arxiv.org/html first, then ar5iv.org

### Twitter 403 error
- App needs Read and Write permissions
- Regenerate tokens after changing permissions

### Turkish translation issues
- Check admin panel to fix terminology
- "ötegezegen" should be one word

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- Paper data from [arXiv.org](https://arxiv.org)
- AI summaries by [Claude](https://anthropic.com) (Anthropic)
- Built for the exoplanet research community 🪐
