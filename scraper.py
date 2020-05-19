# Importing Required Packages
import aiohttp
import logging
import asyncio
import time
import json
import urllib3
import pymongo
import fetch

# Global Variables
BASE_URL = "https://public-apis-api.herokuapp.com/api/v1/"
# 10 Requests allowed per minute
LIMIT = 9
# Calculate rate of sending requests - approximate delay after which next request must be sent
RATE = round(60/(LIMIT+1))


# The main Fetch Class
# attrs package - allows us to write class descriptions without following the standard object protocols(dunder methods)
# and writes the __repr__ function for us

async def main(rate, limit):
    # Definition of Semaphore - To share the rate of request made every minute
    limit = asyncio.Semaphore(limit)
    # Create an Instance of Fetch Object
    f = fetch.Fetch(rate=rate, limit=limit)
    # Run the Request Function to execute the Scraper
    results = json.dumps(await f.request(), indent=4)
    # results = json.dumps(await f.request(), indent=4)
    # Return Results as JSON Object
    return results


# perf_counter is used for measuring time for calculation
time_before = time.perf_counter()
# Run the main function asynchronously using the Global Parameters defined - to maintain consistency
results = asyncio.run(main(RATE,LIMIT))
# Calculate Total Time Taken for Scraping Data = Time After Done - Time Before Done
time_taken = time.perf_counter()-time_before
print(f'Time Take to complete:{time_taken:0.2f} seconds.')

# Storing the data in MongoDBs

db_url = "mongodb://pc77:Parul1415@ds157819.mlab.com:57819/crawler_data"
client = pymongo.MongoClient()
