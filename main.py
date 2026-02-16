import time
import re
import os
from src.config import RSS_FEEDS
from src.scraper import scrape_feeds
from src.utils import is_url_processed, add_url_to_history
from src.ai_engine import generate_post, critique_post
from src.image_generator import create_cover
from src.publisher import send_post

def main():
    print("Starting The Builder v1.5...")
    
    # 1. Scrape
    print("Step 1: Scraping RSS feeds...")
    articles = scrape_feeds(RSS_FEEDS)
    print(f"Step 1 Complete: Found {len(articles)} total articles")
    
    # 2. Filter & Process
    processed_count = 0
    
    # Limit the number of articles to process per run to avoid hitting API limits
    # Gemini Free Tier has stricter limits than expected.
    # Processing 5 articles = 10 calls (Generation + Critique). Optimal for quality.
    MAX_ARTICLES_TO_PROCESS = 5
    articles_checked = 0
    
    for article in articles:
        if articles_checked >= MAX_ARTICLES_TO_PROCESS:
            print(f"Reached limit of {MAX_ARTICLES_TO_PROCESS} processed articles. Stopping for this run.")
            break
            
        if is_url_processed(article['link']):
            # Skipping doesn't count towards API usage
            continue
            
        print(f"Processing: {article['title']}")
        articles_checked += 1
        
        # 3. Generate Draft
        # Combine title and summary for better context
        content = f"Title: {article['title']}\nLink: {article['link']}\nSource: {article['source']}\nSummary: {article['summary']}"
        
        # Add delay to respect rate limits (approx 4 seconds between calls to stay under 15 RPM)
        time.sleep(5) 
        print("Calling AI to generate post...")
        draft_post = generate_post(content)
        
        if not draft_post:
            print("Failed to generate draft. Skipping.")
            continue
            
        print("Draft generated.")
        
        # 4. Critique
        time.sleep(5) # Delay before critique
        score = critique_post(draft_post)
        print(f"Critique Score: {score}/10")
        
        if score < 8:
            print("Score too low. Skipping.")
            add_url_to_history(article['link']) 
            continue
            
        # 5. Generate Image
        tools = "No-code / AI" 
        revenue = ""
        
        # Extract stack
        stack_match = re.search(r'\*\*Стек\*\*:\s*(.*)', draft_post) or re.search(r'\*\*Решение.*?\*\*:\s*(.*)', draft_post)
        if stack_match:
            tools = stack_match.group(1).strip()[:30] + "..." if len(stack_match.group(1)) > 30 else stack_match.group(1).strip()
        
        # Extract revenue/metrics for image overlay
        revenue_match = re.search(r'\$\s*(\d[\d,k]+)\s*(MRR|/мес|в месяц)', draft_post, re.IGNORECASE)
        if revenue_match:
            revenue = f"${revenue_match.group(1)} MRR"

        image_path = create_cover(article['title'], tools, revenue)
        
        # 6. Publish
        if send_post(draft_post, image_path):
            add_url_to_history(article['link'])
            print(f"Successfully published: {article['title']}")
            processed_count += 1
            # Stop after one successful post to spread out content
            break 
        else:
            print("Failed to publish. Check BOT_TOKEN and CHANNEL_ID.")
            
    if processed_count == 0:
        print("No new qualified articles found/published this run.")

if __name__ == "__main__":
    main()
