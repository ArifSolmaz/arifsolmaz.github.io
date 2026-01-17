# 🪐 Exoplanet Papers - Daily arXiv Digest with AI Summaries

A beautiful, automated daily digest of exoplanet research papers from arXiv with **AI-generated summaries** written for general audiences, and **optimized Twitter engagement**.

## ✨ Features

- **Daily Updates**: Automatically fetches the latest papers from arXiv astro-ph.EP
- **AI Summaries**: Each paper gets a ~300 word summary explaining:
  - Why It Matters (big picture significance)
  - What They Did (methods in plain language)
  - Key Findings (main discoveries)
  - Looking Forward (implications)
- **Optimized Tweets**: 2-tweet threads with:
  - Tweet 1: Hook + claim + evidence + question (with image, no links)
  - Tweet 2: arXiv link + summary link + hashtags
- **Smart Paper Selection**: Papers ranked by "tweetability" score (JWST, habitability, biosignatures get priority)
- **Dynamic Hashtags**: Auto-extracts relevant hashtags (2-4 max, fixed lowercase matching)
- **Fallback Images**: Generates branded "paper card" when no figure available
- **Share Button**: Website visitors can easily share papers on Twitter
- **Beautiful UI**: Clean design with responsive 3-column grid
- **Mobile Friendly**: Fully responsive design
- **Zero Maintenance**: GitHub Actions handles everything automatically

## 🆕 Recent Improvements

### Twitter Engagement Optimization

| Before | After |
|--------|-------|
| Generic analogies in tweets | Hook → Claim → Evidence → Question format |
| 8+ hashtags (looked like spam) | 2-4 relevant hashtags max |
| Single tweet with links | 2-tweet thread (content then links) |
| Random paper selection | Tweetability-scored selection |
| No image if figure missing | Fallback paper card image |
| Hashtag matching bug | Fixed lowercase key matching |

### Website Features

- **"Tweet This" button** in paper modal
- **"Copy Link" button** for easy sharing
- Pre-filled tweet text with hook + question

## 🏷️ Dynamic Hashtags

Hashtags are automatically extracted based on paper content (limited to 2-4):

| Category | Example Hashtags |
|----------|------------------|
| Telescopes | #JWST #TESS #Kepler #Hubble |
| Planet Types | #HotJupiter #SuperEarth #SubNeptune |
| Habitability | #HabitableZone #Biosignatures |
| Systems | #TRAPPIST1 #ProximaCentauri |

Base hashtag always included: `#Exoplanets`

## 📁 File Structure

```
your-repo/
├── .github/
│   └── workflows/
│       ├── update-papers.yml    # Fetches papers daily at 08:00 UTC
│       └── tweet-paper.yml      # Tweets one paper hourly (09:00-23:00 UTC)
├── arxiv/
│   ├── index.html               # Main webpage (with share buttons)
│   ├── test_local.py            # Local testing script
│   ├── data/
│   │   ├── papers.json          # Cached paper data + tweet hooks
│   │   └── tweeted.json         # Tracks tweeted papers
│   └── scripts/
│       ├── fetch_papers.py      # Fetches papers, generates summaries + tweet hooks
│       └── post_twitter.py      # Posts paper as 2-tweet thread
```

## 🚀 Setup Instructions

### Step 1: Add Files to Your Repository

1. Copy the entire `arxiv/` folder to your `arifsolmaz.github.io` repository
2. Copy the `.github/` folder to your repository root

### Step 2: Add Your Anthropic API Key

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your Anthropic API key

### Step 3: Set Up Twitter/X Posting

Add these 4 secrets to your repository:

| Secret Name | Value |
|-------------|-------|
| `TWITTER_API_KEY` | Your API Key |
| `TWITTER_API_SECRET` | Your API Secret |
| `TWITTER_ACCESS_TOKEN` | Your Access Token |
| `TWITTER_ACCESS_SECRET` | Your Access Token Secret |

⚠️ **Important**: Make sure your app has **Read and Write** permissions!

### Step 4: Enable Twitter Premium (Optional)

If you have Twitter Premium, enable longer tweets:

1. Go to Settings → Variables → Actions
2. Add variable: `TWITTER_PREMIUM` = `true` (or `plus` for Premium+)

### Step 5: Run the First Update

1. Go to **Actions** → **Update Exoplanet Papers**
2. Click **Run workflow**

## 🧪 Testing Locally

```bash
# Install dependencies
pip install requests anthropic tweepy pillow

# Set environment variables
export ANTHROPIC_API_KEY='your-key'
export TWITTER_API_KEY='...'  # Optional for testing

# Run tests
cd arxiv
python test_local.py

# Test with more papers
python test_local.py --papers 5 --summaries 2 --hooks 2

# Actually post (requires confirmation)
python test_local.py --post
```

### What the test checks:

| Test | What it verifies |
|------|------------------|
| 📡 Fetch papers | arXiv API connection |
| 🤖 Generate summaries | Anthropic API key |
| 🎣 Generate tweet hooks | Hook/claim/evidence/question format |
| 📊 Tweetability scoring | Paper ranking for engagement |
| 🏷️ Hashtag extraction | Lowercase matching fix |
| 📝 Thread formatting | 2-tweet structure |
| 🖼️ Paper card generation | Fallback image creation |
| 🐦 Twitter connection | API credentials |

## 📝 Tweet Format

### Tweet 1 (with image, no links)
```
[Hook: attention-grabbing finding]

[Claim: what's new]

[Evidence: specific detail]

[Question: invite discussion]
```

### Tweet 2 (reply with links)
```
📄 [arXiv link]
📖 Full summary: [page link]

#Exoplanets #JWST
```

## 💰 Cost Estimate

- ~$0.003-0.005 per paper summary
- ~$0.001-0.002 per tweet hook
- **~$1.50-2.50 per month** total

## 🔧 Troubleshooting

### Hashtags not matching
- Fixed in this version: all keyword keys are now lowercase

### Twitter showing "403 Forbidden"
- Your app needs Read and Write permissions
- Regenerate tokens after changing permissions

### Paper cards not generating
- Install PIL: `pip install pillow`
- Check font availability in your environment

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- Paper data from [arXiv.org](https://arxiv.org)
- AI summaries by [Claude](https://anthropic.com) (Anthropic)
- Built for the exoplanet research community
