# The Builder v1.5 - Autonomous AI Telegram Bot

A fully autonomous Telegram bot that finds Western No-code/SaaS case studies, analyzes them with Google Gemini AI, and publishes minimalist posts with unique AI-generated covers.

## Features

- **Smart Scraper**: Monitors Reddit (r/nocode, r/saas, r/Entrepreneur, r/SideProject), Indie Hackers, Product Hunt, and Dev.to
- **AI Writer & Critic**: Gemini 2.0 Flash writes posts and self-critiques them (publishing only if score >= 8/10)
- **Auto-Design**: Generates unique cover images using `Pillow` and a template
- **Git-based DB**: Uses `history.json` to track published posts, no external database required
- **CI/CD**: Runs automatically via GitHub Actions every 6 hours

## Architecture

```
┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│ RSS Feeds   │──▶│  Scraper     │──▶│ History     │
│ (7 sources) │   │ (feedparser) │   │ Filter      │
└─────────────┘   └──────────────┘   └──────┬──────┘
                                           │
                  ┌────────────────────────┘
                  ▼
         ┌────────────────┐
         │ AI Engine      │
         │ (Gemini API)   │
         │ • Writer       │
         │ • Critic       │
         └────────┬───────┘
                  │ (Score >= 8)
                  ▼
         ┌────────────────┐
         │ Image Generator│──┐
         │ (Pillow)       │  │
         └────────────────┘  │
                             ▼
                  ┌──────────────────┐
                  │ Telegram Publisher│
                  └──────────────────┘
```

## Setup

### Prerequisites

- Python 3.10+
- Google Gemini API Key ([Get it here](https://makersuite.google.com/app/apikey))
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- Telegram Channel (where posts will be published)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/AI-blog-tg.git
   cd AI-blog-tg
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```
   GEMINI_API_KEY=your_actual_api_key
   TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHANNEL_ID=@your_channel
   ```

4. **Generate template image** (optional, if not present)
   ```bash
   python generate_template.py
   ```

5. **Run the bot**
   ```bash
   python main.py
   ```

### GitHub Actions Deployment

1. **Add secrets** to your GitHub repository:
   - Go to `Settings` → `Secrets and variables` → `Actions`
   - Add the following secrets:
     - `GEMINI_API_KEY`
     - `TELEGRAM_BOT_TOKEN`
     - `TELEGRAM_CHANNEL_ID`

2. **Enable GitHub Actions**
   - The bot will automatically run every 6 hours via the schedule in `.github/workflows/schedule.yml`
   - You can also manually trigger it from the "Actions" tab

3. **Configure bot user for commits**
   - Update lines 38-39 in `.github/workflows/schedule.yml` with your bot username/email

## Configuration

### Article Processing Limit

The bot processes up to **5 articles per run** to stay within Gemini API's free tier limits (5 articles × 2 API calls = 10 API requests).

Adjust in `main.py`:
```python
MAX_ARTICLES_TO_PROCESS = 5  # Change this value
```

### RSS Feeds

Customize feeds in `src/config.py`:
```python
RSS_FEEDS = [
    "https://www.reddit.com/r/nocode/.rss",
    # Add more feeds...
]
```

### AI Prompts

Modify writer and critic prompts in `src/config.py` to customize post style and quality criteria.

## Utilities

### Check Available Gemini Models

```bash
python check_models.py
```

Or use GitHub Actions workflow: `Check Available Models`

## Troubleshooting

### Bot not posting

1. **Check Telegram credentials**: Verify bot token and channel ID in `.env`
2. **Bot permissions**: Ensure bot is an admin in your channel
3. **Channel ID format**: Use `@channel_name` (public) or `-100XXXXXXXXXX` (private)

### API Rate Limits

- **429 Error**: The bot includes automatic retry with 60-second delay
- **Reduce processing limit**: Lower `MAX_ARTICLES_TO_PROCESS` in `main.py`
- **Increase delays**: Adjust `time.sleep()` values in `main.py` (lines 43, 53)

### No articles found

- Check if RSS feeds are accessible
- Review `history.json` - bot skips already processed articles
- Try running `python main.py` locally to see detailed logs

### Image generation fails

- Verify `template.png` exists in root directory
- Run `python generate_template.py` to create it
- Check for font errors in logs (bot falls back to default font)

## Project Structure

```
AI-blog-tg/
├── .github/workflows/      # GitHub Actions automation
│   ├── schedule.yml        # Main bot schedule (every 6 hours)
│   └── check_models.yml    # Utility to check available models
├── src/
│   ├── ai_engine.py        # Gemini API integration
│   ├── config.py           # Configuration and prompts
│   ├── image_generator.py  # Cover image creation
│   ├── publisher.py        # Telegram publishing
│   ├── scraper.py          # RSS feed scraping
│   └── utils.py            # History management
├── main.py                 # Entry point
├── check_models.py         # Utility: list available models
├── generate_template.py    # Utility: create template image
├── history.json            # Processed articles database
├── template.png            # Cover image template
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## License

MIT License - Feel free to use and modify for your projects.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.