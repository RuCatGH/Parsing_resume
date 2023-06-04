import requests 
import jmespath
import asyncio
import aiohttp
from headers import headers

async def get_file(session, cvid, id_worker) -> None:
    params = {
        'candidateId': f'{id_worker}',
        'cvId': f'{cvid}',
        'portalCode': 'redesign.trudvsem.ru',
    }
    cookies = {
    '...'
    }

    async with session.get('https://trudvsem.ru/iblocks/cv_download/download_docx',cookies=cookies, params=params) as response:
        with open(f'{cvid}.docx', 'wb') as f:
            f.write(await response.read())

async def get_data() -> None:
    async with aiohttp.ClientSession() as session:
        for page in range(201, 202):
            params = {
                'filter': '{"regionCode":["7700000000000"],"salary":["0","999999"],"experience":["EXP_STAFF"],"cvType":["LONG"]}',
                'page': f'{page}',
                'pageSize': '10',
            }

            async with session.get('https://trudvsem.ru/iblocks/_catalog/flat_filter_prr_search_cv/data', params=params) as response:
                data = await response.json()
                cvid = jmespath.search('result.data[*][0]', data)
                id_worker = jmespath.search('result.data[*][1]', data)

                tasks = []
                for i in range(len(id_worker)):
                    tasks.append(get_file(session, cvid[i], id_worker[i]))

                await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_data())
