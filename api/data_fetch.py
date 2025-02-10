import aiohttp

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
