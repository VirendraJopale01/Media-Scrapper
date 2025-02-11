
import logging
import re
import asyncio
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
 
# Import necessary modules
from Utils.utils import save_article_to_markdown
from api.data_fetch import fetchData
from channels.media_channel import scrape_bbc_article, scrape_cnn_article
 

def parse_article(url, html_content):
    """Parses article data synchronously using threading."""
    soup = BeautifulSoup(html_content, 'html.parser')
 
    if 'bbc' in url:
        return scrape_bbc_article(soup)
    elif 'cnn' in url:
        return scrape_cnn_article(soup)
    return None, None
 
async def CollectAll(url):
    """Fetches and processes an article asynchronously using threading.
    
    1. Fetches the HTML content of the article asynchronously using aiohttp.
    2. Parses the HTML content synchronously using threading to improve performance.
    3. Saves the article data to a markdown file using the title and body.
    """
    data = await fetchData(url)
 
    # Using ThreadPoolExecutor for concurrent HTML parsing
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Parse the HTML content synchronously using threading
        title, body = await loop.run_in_executor(executor, parse_article, url, data)

    if title and body:
        # Save the article data to a markdown file
        filename = f"{title[:10].replace(' ', '_')}.md"
        await save_article_to_markdown(title, body, filename)
        logging.info(f"Article saved successfully: {filename}")
 
def ForMultipleChannels():
    """Collects multiple URLs from the user.
    
    This function serves as the main entry point of the program for fetching
    multiple articles. It provides a loop for the user to input multiple URLs
    until the user chooses to exit.
    """
    scraped_urls = []  # List to store all the scraped URLs
    while True:  # Loop until the user chooses to exit
        url = input('Enter Link (Enter "exit" to stop): ').strip()
        if url.lower() == "exit":  # Check if the user wants to exit
            break
        if re.search(r'www.bbc.com|cnn.com', url):
            if url in scraped_urls:
                print('Link is reused, please enter another link.')
            else:
                scraped_urls.append(url)
        else:
            print('Wrong Media Link. Use only CNN or BBC news articles.')
    return scraped_urls
 
async def main():
    """Main entry point with threading for concurrent article fetching.
    
    This function serves as the main entry point of the program. It provides
    a menu for the user to choose from. The user can choose to fetch a single
    article, fetch multiple articles, or exit the program.
    """
    while True:
        print('-- Enter Your Choice --\n')
        print('1. Fetch a Single Article')
        print('2. Fetch Multiple Articles')
        print('3. Exit')
 
        choice = input('Enter Choice: ').strip()
 
        if choice == '1':
            # Fetch a single article
            url = input('Enter the correct URL: ').strip()
            if re.search(r'www.bbc.com|cnn.com', url):
                await CollectAll(url)
            else:
                print('Invalid URL')
        elif choice == '2':
            # Fetch multiple articles
            urls = ForMultipleChannels()
            if urls:
                # Use asyncio.gather to run all the tasks concurrently
                await asyncio.gather(*(CollectAll(url) for url in urls))
        elif choice == '3':
            # Exit the program
            print("Closing the program...")
            break
        else:
            # Handle invalid choices
            print("Invalid choice, try again.")
 
if __name__ == "__main__":
    asyncio.run(main())