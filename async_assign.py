
# 1) Create a decorator named log_execution_time that: 
# • Logs the start time before making an API request. 
# • Logs the end time and total execution time after the request completes. 
# 2) Use asyncio and aiohttp to: 
# • Install aiohttp library 
# • Check aiohttp documentation: https://docs.aiohttp.org/en/stable/ 
# • Fetch data from multiple APIs concurrently. 
# • Use async def and await to handle API requests asynchronously. 
# 3)  Fetch data from at least 3 sample APIs 
# • Check dummy API from https://jsonplaceholder.typicode.com 
# • Use following API links to fetch data: 
# o https://jsonplaceholder.typicode.com/users/6 
# o https://jsonplaceholder.typicode.com/users/4 
# o https://jsonplaceholder.typicode.com/todos/19
import asyncio
import aiohttp
import time
async def getData(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as respose:
            # data=await respose.status
            print(f'{url} data is := {await respose.text()}')
            # print(data)



def log_execution_time(func_API):
    async def wrapper(*args,**kwargs):
        st=time.time()
        result=await func_API(*args,**kwargs)
        # func_API()
        et=time.time()
        print(f'Time Taken {et-st}')
        return result
    return wrapper

@log_execution_time
async def main():
    urls=['https://jsonplaceholder.typicode.com/users/6' ,'https://jsonplaceholder.typicode.com/users/4' ,'https://jsonplaceholder.typicode.com/todos/19']
    task=[getData(url) for url in urls]
    await asyncio.gather(*task)


asyncio.run(main())
