import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import argparse
from datetime import datetime

def get_substack_articles(substack_archive_url, debug=False, show_dates=False, sort_by_date=False, descending=True):
    # Set up Selenium with real browser behavior
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Disable for debugging
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Use a real User-Agent string
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Start the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Open the Substack archive page
        driver.get(substack_archive_url)
        time.sleep(random.uniform(3, 6))  # Random delay to simulate human interaction
        
        # Scroll down slowly to mimic a user
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(2, 5))  # Randomized wait
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Stop if no new content loads
            last_height = new_height
        
        # Get the fully loaded page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        if debug:
            with open("substack_debug.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Saved page source to substack_debug.html. Open it to inspect article structure.")
        
    finally:
        driver.quit()  # Ensure WebDriver is always closed
    
    articles = []  # Use a list to maintain order
    seen_urls = set()  # Track seen URLs to remove duplicates
    
    # Find article links and their publication dates in the archive page
    for link in soup.find_all("a", href=True):
        href = link['href']
        if '/p/' in href and not href.endswith('/comments'):
            full_url = href if href.startswith("http") else substack_archive_url.rstrip('/') + href
            if full_url in seen_urls:
                continue  # Skip duplicate URLs
            seen_urls.add(full_url)
            pub_date = "Unknown date"
            
            if show_dates or sort_by_date:
                date_tag = link.find_previous("time")
                if date_tag:
                    try:
                        parsed_date = datetime.strptime(date_tag.text.strip(), "%B %d, %Y")
                        pub_date = parsed_date.strftime("%d.%m.%Y")
                    except ValueError:
                        pub_date = date_tag.text.strip()
                articles.append((pub_date, full_url))
            else:
                articles.append((None, full_url))
    
    # Sort articles by date if required
    if sort_by_date:
        def sort_key(item):
            date_str, _ = item
            try:
                return datetime.strptime(date_str, "%d.%m.%Y") if date_str != "Unknown date" else datetime.min
            except ValueError:
                return datetime.min  # Handle unexpected formats
        
        articles = sorted(articles, key=sort_key, reverse=descending)
    
    return articles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Substack archive for article links.")
    parser.add_argument("url", help="Substack archive page URL (e.g., https://substack.com/archive)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode and save HTML for inspection")
    parser.add_argument("--show-dates", action="store_true", help="Show publication dates of articles")
    parser.add_argument("--sort-by-date", action="store_true", help="Sort articles by date")
    parser.add_argument("--ascending", action="store_true", help="Sort articles in ascending order instead of descending")
    args = parser.parse_args()
    
    articles = get_substack_articles(
        args.url, debug=args.debug, show_dates=args.show_dates, sort_by_date=args.sort_by_date, descending=not args.ascending
    )
    
    print("\nFound articles:")
    for pub_date, article_url in articles:
        if args.show_dates:
            print(f"{pub_date} - {article_url}")
        else:
            print(article_url)
