import logging,re
import aiohttp,asyncio
from bs4 import BeautifulSoup # import libreries 

from Utils.utils import save_article_to_markdown
# from api.data_fetch import fetchData
from channels.media_channel import scrape_bbc_article, scrape_cnn_article # import modules from th folders structure


async def fetchData(url): 
    """
    Asynchronously fetches data from a given URL.
    Args:
        url (str): The URL from which to fetch the data.

    Returns:
        str: The response data as a string.

    This function uses the aiohttp library to perform an asynchronous HTTP GET request.
    """
    # Cnew aiohttp session to handle the request
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:  # Send a GET request to the URL
            data = await response.text() # Await the text content of the response 
            return data
       
async def CollectAll(url):
    """
    Asynchronously processes a list of URLs to fetch and scrape article data.

    Args:
        urls (list): List of URLs pointing to BBC or CNN articles.

    For each URL, fetches the content, parses the HTML, and extracts the article
    title and body using the appropriate scraper function. If the article is successfully
    extracted, it saves the content to a markdown file and logs the success.
    """
    
        # Fetch the HTML content of the article
    data = await fetchData(url)
        # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(data, 'html.parser')
        # Check if the URL is a BBC article
    if 'bbc' in url:
            # Extract the title and body of the article using the BBC scraper
        title, body = scrape_bbc_article(soup)
       
    elif 'cnn' in url:
            
         title, body = scrape_cnn_article(soup)
        # If the title and body are not None, save the article to a markdown file
    if title and body:
            # Create a filename for the markdown file using the title
        filename = f"{title[:10].replace(' ', '_')}.md"  
            
        await save_article_to_markdown(title, body, filename)
      
        logging.info(f"Article saved successfully: {filename}")
        


#    urls = [
#         "https://www.bbc.com/news/articles/cpqlxrdlg3yo", 
#         "https://edition.cnn.com/2025/02/05/europe/belgium-brussels-shooting-metro-station-intl/index.html" 
#     ]
    # https://www.bbc.com/news/articles/cg7ze00ly1zo
    # https://www.bbc.com/news/articles/c1dg95dyxygo
    # https://www.bbc.com/news/articles/cpqlxrdlg3yo    
    # 


async def ForSingelChannels():    
    """
    Asks user for a URL of a news article and scrapes it using appropriate
    scraper function. If article is scraped successfully, it saves the article
    to a markdown file and logs the success.

    If the URL is not a valid article URL, it prints an error message and exits.
    """

    url=str(input('Enter the correct URL : '))
    if re.search(r'www.bbc.com|cnn.com',url): # regex fo check url
        data=await fetchData(url)
        soup = BeautifulSoup(data, 'html.parser')

        # scrape article data
        if 'bbc' in url:
            title, body = scrape_bbc_article(soup) # function for scrap bbc data

        elif 'cnn' in url:
            title, body=scrape_cnn_article(soup) # function for scrap cnn data
           
        if title and body:
            # save article to markdown file
            filename = f"{title[:10].replace(' ', '_')}.md"  
            await save_article_to_markdown(title, body, filename) 
            logging.info(f"Article saved successfully: {filename}")

    else:
        print('Wrong URL')  
        return 

def ForMultipleChannels():
    """
    Asks user for multiple URLs of news articles and scrapes them using appropriate
    scraper functions. If articles are scraped successfully, it saves the articles
    to markdown files and logs the successes.

    If the URL is not a valid article URL, it prints an error message.

    Returns a list of URLs of the articles scraped.
    """
    # List to store the URLs of the articles scraped
    scraped_urls = []

    while True:
        # Ask user for a URL
        url = str(input('-- Enter Link -- (For End enter " exit "): '))

        # If user enters "0", break the loop
        if url == "exit":
            break  

        # Check if the URL is valid
        if re.search(r'www.bbc.com|cnn.com', url): #regex
            # Check if the URL is already in the list
            if url in scraped_urls:
                print('Link is reused , Please Enter Another link')
            else:
                # Add the URL to the list and strip any leading/trailing spaces
                scraped_urls.append(url.strip())   
        else:
            print('Wrong Media Link Use only CNN or BBC news channels links')    

    return scraped_urls

 

async def main():
    """
    The main entry point of the program.

    Provides a menu for the user to choose from:

    1. For Single Channel: Scrapes a single article from a single channel (BBC or CNN)
    2. From Muliple Channels: Scrapes multiple articles from multiple channels (BBC or CNN)

    If the user chooses 1, it calls ForSingelChannels().
    If the user chooses 2, it calls ForMultipleChannels() and then CollectAll() to process the list of URLs.

    If the user chooses anything else, it prints a message and exits the program.
    """
    while True:
        # Show the menu to the user
        print('-- Enter Your Choice -- \n\n')
        print('1. For Single Channel \n')
        print('2. From Muliple Channels \n')
        print('3. Exit  \n')
        # Get the user's choice
        choice = int(input('Enter Choice : '))
        if choice not in (1,2,3):  
            print('Wrong Choice')
        else:    
            if choice == 1:
                # If the user chooses 1, call ForSingelChannels()
                await ForSingelChannels()
            elif choice == 2:
                # If the user chooses 2, call ForMultipleChannels() and CollectAll()
                urls =  ForMultipleChannels()
                # Process the list of URLs in parallel using asyncio.gather()
                print(urls)
                if urls.__len__() > 0:
                    tasks = [CollectAll(url) for url in urls]
                    await asyncio.gather(*tasks)
            else:
                # If the user enters anything else, print a message and exit the program
                print("Closing The Windoow.....")
                break
        
            
if __name__ == "__main__":

    asyncio.run(main())
    
