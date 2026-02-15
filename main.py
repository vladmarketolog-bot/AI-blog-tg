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
    
    for article in articles:
        if is_url_processed(article['link']):
            print(f"Skipping duplicate: {article['title']}")
            continue
            
        print(f"Processing: {article['title']}")
        
        # 3. Generate Draft
        # Combine title and summary for better context
        content = f"Title: {article['title']}\nSource: {article['source']}\nSummary: {article['summary']}"
        draft_post = generate_post(content)
        
        if not draft_post:
            print("Failed to generate draft. Skipping.")
            continue
            
        print("Draft generated.")
        
        # 4. Critique
        score = critique_post(draft_post)
        print(f"Critique Score: {score}/10")
        
        if score < 8:
            print("Score too low. Skipping.")
            # Optional: Log this? For now just skip.
            # We mark as processed to avoid re-evaluating the same bad article forever?
            # actually, if we mark it processed, we never retry. 
            # If the score is low because of the article quality, that's good.
            # If it's low because of Gemini mood, maybe bad.
            # Let's mark it processed to avoid loops.
            add_url_to_history(article['link']) 
            continue
            
        # 5. Generate Image
        # Extract tools/keywords for the image from the post? 
        # The prompt asks for "Stack" in the text. We might need to extract it or just use the title.
        # Let's use the Title and a generic "No-code" or extract from text if possible.
        # For simplicity, let's use the article title and "AI & No-code" as subtitle/tools.
        # Or better, ask Gemini to extract keywords? 
        # The prompt says: "Developer must implement... function that takes template... adds Title... List of tools".
        # I'll stick to Title and "No-code Tools" for now to keep it simple, or try to parse the draft.
        
        tools = "No-code / AI" # Placeholder, or could parse the "Стек:" line from draft
        
        # Try to parse stack from draft
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
            # 7. Stop after one successful post?
            # The prompt says "Auto-schedule every 4-6 hours". 
            # Posting one per run is a safe strategy to maintain quality and not flood.
            break 
        else:
            print("Failed to publish.")
            
    if processed_count == 0:
        print("No new qualified articles found/published this run.")

if __name__ == "__main__":
    main()
