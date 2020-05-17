import aiohttp
import attr
import logging
import asyncio
import urllib
import time
import json
import urllib3
from urllib.parse import quote
from attr.validators import instance_of

BASE_URL = "https://public-apis-api.herokuapp.com/api/v1/"
RATE = 6
LIMIT = 9

LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)

@attr.s
class Fetch:
    limit = attr.ib()
    rate = attr.ib(default=5, converter=int)

    async def getToken(self, url):
        try:
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            json_data = json.loads(response.data.decode('utf-8'))
            status = response.status
            log.info(f"Made Request : {url}, Status : {status}")
            token = json_data["token"]
            print("Connection to the API established!!\n")
            return token
        except json.decoder.JSONDecodeError:
            print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
            exit()

    async def getList(self, session, url):
        async with session.get(url) as response:
            try:
                status = response.status
                log.info(f"Made Request : {url}, Status : {status}")
                json = await response.json()
                categories = json['categories']
                print("Categories List Retrieved!!\n")
                return categories
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Error Locating the API Enpoint...\nPlease Check the URLs Again!!")
                exit()

    async def getCategoryDetails(self, session, url):
        async with session.get(url) as response:
            try:
                status = response.status
                log.info(f"Made Request : {url}, Status : {status}")
                json_data = await response.json()
                return json_data
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
                exit()

    async def request(self, url):
        async with self.limit:
            authToken = await self.getToken(BASE_URL+'auth/token/')
            async with aiohttp.ClientSession(headers={"Authorization":"bearer "+authToken}) as session:
                result = {}

                for page_number in range(1,6):
                    categories = await (self.getList(session, BASE_URL+'apis/categories?page='+str(page_number)))
                    await asyncio.sleep(self.rate)
                    for category in categories:
                        if category is not None:
                            url = BASE_URL+'apis/entry?page='+str(page_number)+'&category='+quote(category)
                            current = await self.getCategoryDetails(session, url)
                            result[category] = current['categories']
                            await asyncio.sleep(self.rate)
                        else:
                            break
                return result

async def main(url, rate, limit):
    limit = asyncio.Semaphore(limit)
    f = Fetch(rate=rate, limit=limit)
    results = json.dumps(await f.request(url=url), indent=4)
    print(results)


time_before = time.perf_counter()
asyncio.run(main(BASE_URL, RATE, LIMIT))
time_taken = time.perf_counter()-time_before
print(f'Time Take to complete:{time_taken:0.2f} seconds.')
