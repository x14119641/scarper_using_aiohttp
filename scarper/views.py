from aiohttp import web, ClientSession
from asyncio import run,gather, create_task, Semaphore
from lxml import html



ENDPOINTS = ['Insider_Analysis','SPY','BTC.X', 'ND_F','SPX',]


async def fetch(url, session, endpoint=None):
    async with session.get(url) as response:
        html_body = await response.read()
        return {"body":html_body, "endpoint": endpoint}


async def fetch_with_sem(url, session, sem, endpoint=None):
    async with sem:
        return await fetch(url, session, endpoint)


async def main(start_year=2020, years_ago=5):
    tasks = []
    # semaphore
    sem = Semaphore(10) # 10 tasks in a time
    async with ClientSession() as session:
        for endpoint in ENDPOINTS:
            url = f'https://stocktwits.com/symbol/{endpoint}'
            if endpoint.isalpha():
                url = f'https://stocktwits.com/{endpoint}'
            tasks.append(
                create_task(
                    fetch_with_sem(url, session, sem, endpoint)
                )
            )
        pages_content = await gather(*tasks)
        return pages_content


if __name__ == "__main__":
    pages_content = run(main())
    print(pages_content[1])
