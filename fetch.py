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

# Global Token object
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
            response = await requests.get(url=url)
        except requests.exceptions.ConnectionError as e:
            print("Unable to connect to the API!!\n Please make sure your are connected to the internet or check the URLs again..\n")
            print(e)
            exit()
        else:
            try:
                # Log the Actions
                status = response.status_code
                log.info(f"Made Request : {url}, Status : {status}")
                # Decode the obtained JSON token
                json_data = response.json()
                # Extract the token value and return it
                token_data = json_data["token"]
                print("Token Received!\n\nConnection to the API established!!\n")
                return token_data

            except json.decoder.JSONDecodeError:
                print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
                exit()


    async def getList(self, session, num, categories):
        "Recursive Function to get all pages of the list of all Categories of APIs"

        # URL for the category list
        url = BASE_URL+'apis/categories?page='+str(num)
        # Get response and if error occurs
        try:
            response = await session.get(url)
        except requests.exceptions.ConnectionError as e:
            print("Unable to connect to the API!!\n Please make sure your are connected to the internet or check the URLs again..\n")
            print(e)
        else:
            # Check if status is not 200
            status = int(response.status_code)
            if(status!=200):
                # If too many requests, sleep
                if(status==429):
                    await asyncio.sleep(20)
                if(status==403 | status==429):
                    # Get a new token
                    TOKEN = await self.getToken()
                    # Update the token in the session header
                    session.headers.update({"Authorization":"Bearer= "+str(TOKEN)})
                    await self.getList(session, num, categories)
            else:
                # If we get status-code == 200
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

        # URL for the function call
        url=BASE_URL+'apis/entry?page='+str(num)+'&category='+quote(str(category))
        # Make a request and proceed furthur only if status code 200 is recieved
        try:
            response = await session.get(url)
        except requests.exceptions.ConnectionError as e:
            # If error occurs while polling the server return the error and exit
            print("Unable to connect to the API!!\n Please make sure your are connected to the internet or check the URLs again..\n")
            print(e)
            exit()
        else:
            # Check for status code 200
            status = int(response.status_code)
            if(status!=200):
                # If status code is 429 i.e. too many requests, sleep for some time
                if(status==429):
                    await asyncio.sleep(20)
                if(status==403 | status==429):
                    # Get a new token
                    TOKEN = await self.getToken()
                    # Update the token in the session header
                    session.headers.update({"Authorization":"Bearer= "+str(TOKEN)})
                    # restart the last function call
                    await self.getCategoryContents(session, num, category, current)
            else:
                # If status code is 200
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