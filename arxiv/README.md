# 🪐 Exoplanet Papers - Daily arXiv Digest with AI Summaries

A beautiful, automated daily digest of exoplanet research papers from arXiv with **AI-generated summaries** written for general audiences.

![Preview](preview.png)

## ✨ Features

- **Daily Updates**: Automatically fetches the latest papers from arXiv astro-ph.EP
- **AI Summaries**: Each paper gets a ~300 word summary explaining:
  - Why It Matters (big picture significance)
  - What They Did (methods in plain language)
  - Key Findings (main discoveries)
  - Looking Forward (implications)
- **Hourly Tweets**: Each paper gets its own tweet, spread throughout the day
- **Dynamic Hashtags**: Auto-extracts relevant hashtags from paper content (telescopes, planet types, methods, etc.)
- **Premium Support**: Longer tweets with full summaries for Twitter Premium users
- **Beautiful UI**: Cosmic dark theme with animated starfield
- **Mobile Friendly**: Fully responsive design
- **Zero Maintenance**: GitHub Actions handles everything automatically

## 🏷️ Dynamic Hashtags

Hashtags are automatically extracted based on paper content:

| Category | Example Hashtags |
|----------|------------------|
| Telescopes | #JWST #TESS #Kepler #Hubble #VLT |
| Planet Types | #HotJupiter #SuperEarth #SubNeptune #OceanWorld |
| Methods | #TransitMethod #RadialVelocity #Spectroscopy |
| Atmospheres | #WaterVapor #CO2 #Methane #ExoplanetAtmosphere |
| Habitability | #HabitableZone #Biosignatures #Astrobiology |
| Systems | #TRAPPIST1 #ProximaCentauri #WASP39 |
| Processes | #PlanetFormation #TidalHeating #AtmosphericEscape |

Base hashtags always included: `#Exoplanets #Astronomy #arXiv`

## 📁 File Structure

```
your-repo/
├── .github/
│   └── workflows/
│       ├── update-papers.yml    # Fetches papers daily at 08:00 UTC
│       └── tweet-paper.yml      # Tweets one paper hourly (09:00-23:00 UTC)
├── arxiv/
│   ├── index.html               # Main webpage
│   ├── data/
│   │   ├── papers.json          # Cached paper data
│   │   └── tweeted.json         # Tracks tweeted papers
│   └── scripts/
│       ├── fetch_papers.py      # Fetches & generates summaries
│       └── post_twitter.py      # Posts one paper to Twitter
```

## 🚀 Setup Instructions

### Step 1: Add Files to Your Repository

1. Copy the entire `arxiv/` folder to your `arifsolmaz.github.io` repository
2. Copy the `.github/` folder to your repository root

Your repo structure should look like:
```
arifsolmaz.github.io/
├── .github/
│   └── workflows/
│       ├── update-papers.yml
│       └── tweet-paper.yml
├── arxiv/
│   ├── index.html
│   ├── data/
│   │   ├── papers.json
│   │   └── tweeted.json
│   └── scripts/
│       ├── fetch_papers.py
│       └── post_twitter.py
├── index.html (your main site)
└── ... (other files)
```

### Step 2: Add Your Anthropic API Key

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `ANTHROPIC_API_KEY`
5. Value: Your Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))
6. Click **Add secret**

### Step 3: Set Up Twitter/X Posting (Optional)

To automatically post paper summaries to Twitter:

#### 3a. Create a Twitter Developer Account
1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Sign up for a developer account (Free tier works!)
3. Create a new Project and App

#### 3b. Get Your API Keys
In your Twitter Developer Portal App settings:
1. Go to **Keys and Tokens**
2. Generate/copy these 4 values:
   - API Key (Consumer Key)
   - API Secret (Consumer Secret)
   - Access Token
   - Access Token Secret

⚠️ **Important**: Make sure your app has **Read and Write** permissions!

#### 3c. Add Twitter Secrets to GitHub
Add these 4 secrets to your repository (Settings → Secrets → Actions):

| Secret Name | Value |
|-------------|-------|
| `TWITTER_API_KEY` | Your API Key |
| `TWITTER_API_SECRET` | Your API Secret |
| `TWITTER_ACCESS_TOKEN` | Your Access Token |
| `TWITTER_ACCESS_SECRET` | Your Access Token Secret |

#### 3d. Update Your Page URL
Edit `.github/workflows/tweet-paper.yml` and change:
```yaml
PAGE_URL: "https://arifsolmaz.github.io/arxiv"
```
to your actual GitHub Pages URL.

#### 3e. Enable Twitter Premium (Optional)
If you have Twitter Premium, enable longer tweets with full summaries:

1. Go to Settings → Variables → Actions
2. Click "New repository variable"
3. Add variable:
   - Name: `TWITTER_PREMIUM`
   - Value: `true` (for Premium, 4000 chars) or `plus` (for Premium+, 25000 chars)

**Tweet lengths by account:**
| Account | Limit | Content |
|---------|-------|---------|
| Free | 280 chars | Title + brief highlight + link |
| Premium | 4,000 chars | Full title + all summary sections + link |
| Premium+ | 25,000 chars | Complete summary with formatting |

### Step 4: Enable GitHub Actions

1. Go to your repository's **Actions** tab
2. If prompted, enable workflows
3. You should see two workflows:
   - "Update Exoplanet Papers" (fetches papers daily)
   - "Tweet Paper" (tweets hourly)

### Step 5: Run the First Update

1. Go to **Actions** → **Update Exoplanet Papers**
2. Click **Run workflow** → **Run workflow**
3. Wait ~2-3 minutes for it to complete
4. Check that `arxiv/data/papers.json` has been updated

### Step 6: View Your Page

Visit: `https://arifsolmaz.github.io/arxiv`

🎉 That's it! 
- Papers fetch daily at 08:00 UTC
- Tweets post hourly from 09:00-23:00 UTC (one paper per hour)

## 🧪 Testing Locally

Before deploying, test everything locally to make sure it works.

### Step 1: Install dependencies

```bash
pip install requests anthropic tweepy
```

### Step 2: Set environment variables

```bash
# Required for summaries
export ANTHROPIC_API_KEY='your-anthropic-key'

# Required for Twitter (optional for testing)
export TWITTER_API_KEY='your-api-key'
export TWITTER_API_SECRET='your-api-secret'
export TWITTER_ACCESS_TOKEN='your-access-token'
export TWITTER_ACCESS_SECRET='your-access-secret'

# Optional: Test Premium tweet formatting
export TWITTER_PREMIUM='true'  # or 'plus'
```

### Step 3: Run the test script

```bash
cd arxiv

# Basic test (fetches 3 papers, generates 1 summary, tests formatting)
python test_local.py

# Test with more papers
python test_local.py --papers 5 --summaries 2

# Test and actually post ONE tweet (will ask for confirmation)
python test_local.py --post

# Skip fetching, use existing data
python test_local.py --skip-fetch
```

### Step 4: Test the website

```bash
cd arxiv
python -m http.server 8000
# Open http://localhost:8000 in your browser
```

### What the test checks:

| Test | What it verifies |
|------|------------------|
| 📡 Fetch papers | arXiv API connection works |
| 🤖 Generate summaries | Anthropic API key is valid |
| 🏷️ Hashtag extraction | Keywords are detected correctly |
| 📝 Tweet formatting | Tweets fit within character limits |
| 🐦 Twitter connection | API credentials work |
| 💾 Save data | JSON file is created properly |

### Example test output:

```
🪐 Exoplanet Papers - Local Test Suite

============================================================
📡 TESTING: Fetch papers from arXiv
============================================================
✅ Successfully fetched 3 papers

Paper 1:
  ID: 2501.12345
  Title: Detection of Water Vapor in the Atmosphere of...
  Authors: Sarah Chen, Michael Rodriguez, Elena Petrova
  Categories: astro-ph.EP

============================================================
🏷️  TESTING: Hashtag extraction
============================================================
Paper 1: Detection of Water Vapor in the Atmosphere of...
  Extracted hashtags: #Exoplanets #Astronomy #arXiv #JWST #WaterVapor #SubNeptune

============================================================
📝 TESTING: Tweet formatting
============================================================
Account: FREE (280 chars)
Length: 267 / 280 chars
✅ Tweet fits within limit (13 chars remaining)
```

## ⚙️ Configuration

### Change Paper Fetch Schedule

Edit `.github/workflows/update-papers.yml`:

```yaml
on:
  schedule:
    - cron: '0 8 * * 1-5'  # 08:00 UTC weekdays
```

### Change Tweet Schedule

Edit `.github/workflows/tweet-paper.yml`:

```yaml
on:
  schedule:
    # Tweets hourly from 09:00-23:00 UTC on weekdays
    - cron: '0 9-23 * * 1-5'
```

To adjust for your timezone or audience:
- `'0 9-23 * * 1-5'` - 09:00-23:00 UTC (default, covers EU/US hours)
- `'0 13-22 * * 1-5'` - 13:00-22:00 UTC (better for US East Coast)
- `'0 6-20 * * 1-5'` - 06:00-20:00 UTC (better for Europe)

### Change Number of Papers

Edit `arxiv/scripts/fetch_papers.py`:

```python
MAX_PAPERS = 15  # Change to desired number
```

### Change arXiv Category

Edit `arxiv/scripts/fetch_papers.py`:

```python
ARXIV_CATEGORY = "astro-ph.EP"  # Earth and Planetary Astrophysics
```

Other relevant categories:
- `astro-ph.EP` - Exoplanets, planetary systems
- `astro-ph.SR` - Solar and stellar astrophysics
- `astro-ph.GA` - Galaxies
- `astro-ph.IM` - Instrumentation and methods

## 💰 Cost Estimate

The Anthropic API costs approximately:
- ~$0.003-0.005 per paper summary (using Claude Sonnet)
- ~$0.05-0.08 per day for 15 papers
- **~$1.00-1.75 per month** (weekdays only, ~22 days)

The script also reuses existing summaries when papers haven't changed, further reducing costs.

## 🔧 Troubleshooting

### Action fails with "ANTHROPIC_API_KEY not set"
- Make sure you added the secret correctly in repository settings
- The secret name must be exactly `ANTHROPIC_API_KEY`

### Papers not updating
- Check the Actions tab for error logs
- Ensure GitHub Actions is enabled for your repository
- Try running the workflow manually

### Page shows "Error loading papers"
- Make sure `arxiv/data/papers.json` exists and is valid JSON
- Check that the file path is correct (`data/papers.json` relative to `index.html`)

### Twitter not posting
- Verify all 4 Twitter secrets are set correctly
- Check that your Twitter app has **Read and Write** permissions
- Go to Twitter Developer Portal → Your App → Settings → App permissions
- If you just changed permissions, regenerate your Access Token & Secret

### Twitter error: "403 Forbidden"
- Your app likely has Read-only permissions
- In Twitter Developer Portal: Settings → User authentication settings → Edit
- Set App permissions to "Read and write"
- Regenerate tokens after changing permissions

### CORS errors when testing locally
- Use a local server: `python -m http.server 8000`
- Or deploy to GitHub Pages first

### Disable Twitter temporarily
To disable tweeting without removing secrets:
1. Go to Settings → Variables → Actions
2. Add variable: `TWITTER_ENABLED` = `false`
3. Remove the variable to re-enable

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- Paper data from [arXiv.org](https://arxiv.org)
- AI summaries by [Claude](https://anthropic.com) (Anthropic)
- Built for the exoplanet research community
