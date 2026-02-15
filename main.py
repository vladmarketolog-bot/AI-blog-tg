from src.config import RSS_FEEDS
from src.scraper import scrape_feeds
from src.utils import is_url_processed, add_url_to_history
from src.ai_engine import generate_post, critique_post
from src.image_generator import create_cover
from src.publisher import send_post
import os

def main():
    print("Starting The Builder v1.5...")
    
    # 1. Scrape
    articles = scrape_feeds(RSS_FEEDS)
    
    # 2. Filter & Process
    processed_count = 0
    
    # Limit the number of articles to process per run to avoid hitting API limits
    # Gemini Free Tier has limits (e.g. 15 RPM). 
    # Processing 5 articles = 5 * 2 (Generation + Critique) = 10 calls.
    MAX_ARTICLES_TO_PROCESS = 5
    articles_checked = 0
    
    import time
    
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
        content = f"Title: {article['title']}\nSource: {article['source']}\nSummary: {article['summary']}"
        
        # Add delay to respect rate limits (approx 4 seconds between calls to stay under 15 RPM)
        time.sleep(5) 
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
        import re
        stack_match = re.search(r'\*\*Стек\*\*:\s*(.*)', draft_post)
        if stack_match:
            tools = stack_match.group(1).strip()[:30] + "..." if len(stack_match.group(1)) > 30 else stack_match.group(1).strip()

        image_path = create_cover(article['title'], tools)
        
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
