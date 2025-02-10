
import logging
def scrape_bbc_article(data):
    """
    Scrapes a BBC article.

    Args:
        data (BeautifulSoup): The parsed HTML of the article.

    Returns:
        tuple: A tuple containing the title and body of the article as strings.
               If the article could not be scraped, returns (None, None).

    Raises:
        Exception: If there is an error while scraping the article.
    """
    # Try to scrape the article
    try:
        # Get the title of the article
        title = data.find('h1').get_text(strip=True)
        
        article_body = ""
        paragraphs = data.find_all('p')
        for para in paragraphs:
            article_body += para.get_text(strip=True) + '\n'
        # Return the title and body of the article
        return title, article_body
    # Handle any errors that occur while scraping the article
    except Exception as e:
        logging.error(f"Error while scraping BBC article: {e}")
        return None, None


def scrape_cnn_article(data):
    """
    Scrapes a CNN article.

    Args:
        data (BeautifulSoup): The parsed HTML of the article.

    Returns:
        tuple: A tuple containing the title and body of the article as strings.
               If the article could not be scraped, returns (None, None).

    Raises:
        Exception: If there is an error while scraping the article.
    """
    # Attempt to scrape the article
    try:
        # Extract the title of the article
        title = data.find('h1').get_text(strip=True)

        article_body = ""
        
        # Find all paragraphs within the article content
        paragraphs = data.find_all('div', {'class': 'article__content'})
        
        # Concatenate text from each paragraph into the article body
        for para in paragraphs:
            article_body += para.get_text(strip=True) + '\n'

        # Return the extracted title and body
        return title, article_body

    # Log any exceptions that occur during scraping
    except Exception as e:
        logging.error(f"Error while scraping CNN article: {e}")
        return None, None

