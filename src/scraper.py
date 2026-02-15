import feedparser
import time

def scrape_feeds(feed_urls):
    """
    Scrapes RSS feeds and returns a list of dictionaries with title, link, and summary.
    """
    articles = []
    print("Scraping feeds...")
    for url in feed_urls:
        try:
            print(f"Parsing {url}...")
            feed = feedparser.parse(url)
            for entry in feed.entries:
                # Basic filtering to ensure we have content
                if hasattr(entry, 'link') and hasattr(entry, 'title'):
                    summary = getattr(entry, 'summary', '')
                    # If summary is empty, sometimes content is in 'content' field
                    if not summary and hasattr(entry, 'content'):
                        summary = entry.content[0].value if entry.content else ''
                    
                    articles.append({
                        'title': entry.title,
                        'link': entry.link,
                        'summary': summary,
                        'source': url
                    })
        except Exception as e:
            print(f"Error parsing feed {url}: {e}")
            
    print(f"Found {len(articles)} articles.")
    return articles
