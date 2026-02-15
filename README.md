# The Builder v1.5 - Autonomous AI Telegram Bot

A fully autonomous Telegram bot that finds Western No-code/SaaS case studies, analyzes them with Google Gemini 1.5 Pro, and publishes minimalist posts with unique AI-generated covers.

## Features
- **Smart Scraper**: Monitors Reddit (r/nocode, r/saas) and Indie Hackers.
- **AI Writer & Critic**: Gemini 1.5 Pro writes posts and self-critiques them (publishing only if score >= 8/10).
- **Auto-Design**: Generates unique cover images using `Pillow` and a template.
- **Git-based DB**: Uses `history.json` to track published posts, no external database required.
- **CI/CD**: Runs automatically via GitHub Actions every 6 hours.

## Setup

1. **Secrets**: Add these to GitHub Repository Secrets:
   - `GEMINI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHANNEL_ID`

2. **Template**: ensure `template.png` is in the root directory.

3. **Deploy**:
   The bot runs on schedule. You can also trigger it manually from the "Actions" tab.

## Local Development
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set `.env` file with keys.
3. Run:
   ```bash
   python main.py
   ```