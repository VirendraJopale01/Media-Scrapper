import logging
import os
import aiofiles

#  log congif file with time and message
logging.basicConfig(
    filename='scraping_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def save_article_to_markdown(title, body, filename):
    """
    Saves article content to a markdown file.

    Args:
        title (str): Article title.
        body (str): Article body.
        filename (str): Filename to save the article to.

    Returns:
        bool: True if the article was saved successfully, False otherwise.
    """
    #  Complete path of markdown file
    folder_path = os.path.join(os.getcwd(), 'markdown')

    # Ensure the 'markdown' folder exists, create if it doesn't
    os.makedirs(folder_path, exist_ok=True)

    # Complete path of markdown file
    completePath = os.path.join(folder_path, filename)
    try:
        #  Open file in write mode
        async with aiofiles.open(completePath, 'w', encoding='utf-8') as file:
            #  Content to write in markdown file
            md_content = f"# {title}\n\n{body}"
            await file.write(md_content)
            #  Return True if article is saved successfully
            return True
    except Exception as e:
        #  Log the error in log file
        logging.error(f"Error while saving article to file: {e}")
        return False

