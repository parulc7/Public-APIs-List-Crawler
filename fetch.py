import logging
import asyncio
import aiohttp
import time
import json
import urllib3
import attr
import requests_async as requests
from urllib.parse import quote

# Global Variables
BASE_URL = "https://public-apis-api.herokuapp.com/api/v1/"
# 10 Requests allowed per minute
LIMIT = 9
# Calculate rate of sending requests - approximate delay after which next request must be sent
RATE = round(60/(LIMIT+1))

TOKEN = {}


# Configuration for the Logger
LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)

# Fetch Class

@attr.s
class Fetch:
    # Attributes as defined under attr package
    limit = attr.ib()
    rate = attr.ib(default=5, converter=int)
    async def getToken(self):
        "Function to get the Authentication Token"
        "Since getting a token is an individual request, including it in the session is not a smart decision"
        url = BASE_URL+'auth/token/'
        try:
            # Create a request for Authentication Token using urllib3
            http = urllib3.PoolManager()
            response = http.request('GET', url)
            # Log the Actions
            status = response.status
            log.info(f"Made Request : {url}, Status : {status}")
            # Decode the obtained JSON token
            json_data = json.loads(response.data.decode('utf-8'))
            # Extract the token value and return it
            token_data = json_data["token"]
            print("Connection to the API established!!\n")
            return token_data

        except json.decoder.JSONDecodeError:
            print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
            exit()


    async def getList(self, session, num, categories):
        "Recursive Function to get all pages of the list of all Categories of APIs"
        url = BASE_URL+'apis/categories?page='+str(num)
        response = await session.get(url)
        status = int(response.status_code)
        if(status!=200):
            if(status==429):
                print(response.headers)
                await asyncio.sleep(60)
            TOKEN = await self.getToken()
            session.headers.update({"Authorization":"Bearer= "+str(TOKEN)})
            await self.getList(session, num, categories)
        else:
            try:
                # Log the Request
                log.info(f"Made Request : {url}, Status : {status}")
                # Get the JSON data and extract the Categories Array
                json = response.json()
                val = json['categories']
                # Base Case for the Recursive Calls to end
                if(len(val)==0):
                    return
                # Append the newly obtained data to the list of already obtained data
                categories+=val
                # Throttle the next request
                await asyncio.sleep(self.rate)
                # Recursive call to get the next page
                await self.getList(session, num+1, categories)
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Error Locating the API Enpoint...\nPlease Check the URLs Again!!")
                exit()
    
    async def getCategoryContents(self, session, num, category, current):
        "Recursive Function to fetch all pages of the API Endpoints within each Category"
        url=BASE_URL+'apis/entry?page='+str(num)+'&category='+quote(str(category))
        response = await session.get(url)
        status = int(response.status_code)
        print(response, type(response))
        if(status!=200):
            if(status==429):
                print(response.headers)
                await asyncio.sleep(60)
            TOKEN = await self.getToken()
            session.headers.update({"Authorization":"Bearer= "+str(TOKEN)})
            await self.getCategoryContents(session, num, category, current)
        else:
            try:
                #Log the request
                log.info(f"Made Request : {url} , Status : {status}")
                # Extract the category list and return the obtained JSON data
                json_data = response.json()
                category_contents = json_data['categories']
                # Base Case for Recursive Call to end
                if(len(category_contents)==0):
                    return
                # Append the newly obtained data to the already existing data
                current+=category_contents
                # Throttle the next request
                await asyncio.sleep(self.rate)
                # Recursive call to get the next page
                await self.getCategoryContents(session, num+1, category, current)
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
                exit()

    async def request(self):
        # Only make "Limit" number of Requests per minute (here 10 allowed) - 0 based index
        async with self.limit:
            # Get Authentication Token
            TOKEN = await self.getToken()
            # Start the Client Session and pass the Authentication Token Data in the Header
            session = requests.Session()
            session.headers.update({"Authorization":"Bearer= "+str(TOKEN)})
            async with session:
                # Output Object
                result = {}
                categories = []
                # Get the Category list on Each Page
                await self.getList(session, 1, categories)
                # Throttle next request to maintain the rate limit
                await asyncio.sleep(self.rate)
                # For every category in the categories list, get the category api contents 
                for category in categories:
                    current = []
                    # Fills the current api category list
                    await self.getCategoryContents(session, 1, category, current)
                    # Throttle the next request to maintain the rate limit
                    await asyncio.sleep(self.rate)
                    # Insert (category, apiList) pair into the result object
                    result[category] = current
                return result