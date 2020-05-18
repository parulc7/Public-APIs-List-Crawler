# Importing Required Packages
import aiohttp
import attr
import logging
import asyncio
import urllib
import time
import json
import urllib3
from urllib.parse import quote

# Global Variables
BASE_URL = "https://public-apis-api.herokuapp.com/api/v1/"
# 10 Requests allowed per minute
LIMIT = 9
# Calculate rate of sending requests - approximate delay after which next request must be sent
RATE = round(60/(LIMIT+1))

# Configuration for the Logger
LOGGER_FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=LOGGER_FORMAT, datefmt='[%H:%M:%S]')
log = logging.getLogger()
log.setLevel(logging.INFO)

# The main Fetch Class
# attrs package - allows us to write class descriptions without following the standard object protocols(dunder methods)
# and writes the __repr__ function for us
@attr.s
class Fetch:
    # Attributes as defined under attr package
    limit = attr.ib()
    rate = attr.ib(default=5, converter=int)

    async def getToken(self, url):
        "Function to get the Authentication Token"
        "Since getting a token is an individual request, including it in the session is not a smart decision"
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
            token = json_data["token"]
            print("Connection to the API established!!\n")
            return token
        except json.decoder.JSONDecodeError:
            print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
            exit()

    async def getList(self, session, url):
        "Function to get the list of all the Categories of APIs"
        async with session.get(url) as response:
            try:
                # Log the Request
                status = response.status
                log.info(f"Made Request : {url}, Status : {status}")
                # Get the JSON data and extract the Categories Array
                json = await response.json()
                categories = json['categories']
                print("Categories List Retrieved!!\n")
                return categories
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Error Locating the API Enpoint...\nPlease Check the URLs Again!!")
                exit()

    async def getCategoryContents(self, session, url):
        "Function to fetch the API Endpoints within each Category"
        async with session.get(url) as response:
            try:
                #Log the request
                status = response.status
                log.info(f"Made Request : {url}, Status : {status}")
                # Return the obtained JSON data
                json_data = await response.json()
                return json_data
            except aiohttp.client_exceptions.ContentTypeError:
                print(f"Error Locating the API Endpoint...\nPlease Check the URLs Again!!")
                exit()

    async def request(self, url):
        # Only make "Limit" number of Requests per minute (here 10 allowed) - 0 based index
        async with self.limit:
            # Get Authentication Token
            authToken = await self.getToken(BASE_URL+'auth/token/')
            # Start the Client Session and pass the Authentication Token Data in the Header
            async with aiohttp.ClientSession(headers={"Authorization":"bearer "+authToken}) as session:
                # Output Object
                result = {}

                # Iterate over all the pages
                for page_number in range(1,6):
                    # Get the Category list on Each Page
                    categories = await (self.getList(session, BASE_URL+'apis/categories?page='+str(page_number)))
                    # Sleep to maintain the rate limit
                    await asyncio.sleep(self.rate)
                    # For every category in the category page
                    for category in categories:
                        # If we have not encoutered an invalid/empty category
                        if category is not None:
                            # Get the Contents (API Endpoint) belonging to the category
                            url = BASE_URL+'apis/entry?page=1&category='+quote(category)
                            current = await self.getCategoryContents(session, url)
                            # Insert the returned Object in to the output object
                            print(current['categories'])
                            print("\n")
                            # Sleep to maintain the rate limit
                            await asyncio.sleep(self.rate)
                        else:
                            # If the category is NULL
                            break
                return result

async def main(url, rate, limit):
    # Definition of Semaphore - To share the rate of request made every minute
    limit = asyncio.Semaphore(limit)
    # Create an Instance of Fetch Object
    f = Fetch(rate=rate, limit=limit)
    # Run the Request Function to execute the Scraper
    results = json.dumps(await f.request(url=url), indent=4)
    # Return Results as JSON Object
    print(results)

# perf_counter is used for measuring time for calculation
time_before = time.perf_counter()
# Run the main function asynchronously using the Global Parameters defined - to maintain consistency
asyncio.run(main(BASE_URL, RATE, LIMIT))
# Calculate Total Time Taken for Scraping Data = Time After Done - Time Before Done
time_taken = time.perf_counter()-time_before
print(f'Time Take to complete:{time_taken:0.2f} seconds.')
