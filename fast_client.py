import asyncio, aiohttp, os
from itertools import cycle

conns = 15000
chunk_size = 100
url = "http://localhost:9005/test_endpoint"


async def query_url(session, url, headers=None, method='get', data=None):
    response = await session.get(
        url=url, headers=headers, timeout=600, data=data
    )
    
    return response


async def bound_query_url(sem, session, url):
    # will block in case there are more attempts
    # to use it than was during semaphore creation
    async with sem:
        return await query_url(session, url)

    
async def read_responses(responses):
    c_responses = cycle(enumerate(responses))
    
    while True:
        file_ind, response = c_responses.__next__()
    
        with open(f'./files/temp_file_{file_ind}.txt', 'ab') as file:
            chunk = await response.content.read(chunk_size)
            if not chunk:
                break
            file.write(chunk)


def _create_working_folder():
    if not os.path.isdir('./files'):
        os.mkdir('./files')
    
    
async def run(conns):
    tasks = []
    # Semaphore will limit the number of concurrently running coroutines
    # in case you want to balance load on the CPU or network
    sem = asyncio.Semaphore(conns) 
    conn = aiohttp.TCPConnector(limit=conns)
    
    async with aiohttp.ClientSession(connector=conn) as session:
        for conn in range(conns):
            task = asyncio.create_task(bound_query_url(sem, session, url))
            tasks.append(task)
    
        responses = await asyncio.gather(*tasks)    
        await read_responses(responses)
    

if __name__ == '__main__':
    _create_working_folder()
    asyncio.run(run(conns))
    