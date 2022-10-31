from aiohttp import ClientSession
from asyncio import to_thread

from random import randint, choice
from time import time

from typing import Tuple, Optional


# Случайная шутка с сайта http://castlots.org/generator-anekdotov-online


headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Content-Length": "0",
        "Host": "castlots.org",
        "Origin": "http://castlots.org",
        "Referer": "http://castlots.org/generator-anekdotov-online/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "X-Requested-With": "XMLHttpRequest"
        }


def return_timestamp() -> Tuple[str, ...]:
    return '{:.9f}'.format(time()).split('.')


def randigits(n) -> int:
    start = 10**(n-1)
    end = (10**n)-1
    return randint(start, end)


async def gen_cookie_str(n: int, timestamp: str) -> str:
    return f'GA1.2.{await to_thread(randigits, n)}.{timestamp}'


async def gen_cookies() -> dict:
    ts1, ts2 = await to_thread(return_timestamp)
    return {
            '_ga': await gen_cookie_str(choice((8,9)), ts1),
            '_gid': await gen_cookie_str(10, ts1),
            '_ym_d': ts1,
            '_ym_isad': '2',
            '_ym_uid': f'{ts1}{ts2}'
            }


async def main() -> Optional[str]:
    async with ClientSession() as session:
        resp = await session.post('http://castlots.org/generator-anekdotov-online/generate.php',
                                                    headers=headers, cookies=await gen_cookies())
        data = await resp.json(content_type='text/html')
    del resp
    if data['success']:
        return data['va']



if __name__ == "__main__":
    from asyncio import run
    print(run(main()))