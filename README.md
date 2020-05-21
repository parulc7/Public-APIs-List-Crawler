# Public APIs List Crawler

* Built entirely on Python without using any dedicated Scraping Framework like Scrapy etc.
* Uses the SuperFast Asynchronous Modules for Python - `aysncio`, `aiohttp` and `request-sync`
* Leverages Semaphores to control the rate of requests made per minute, thus respecting the Rate Limit set by the Server
* Uses `pymongo` to write the json file to a Mongo Database hosted on Mlab, locally stored in `db/crawler_data`

## Details

1. First, we need to get the API token. Then all the successive requests have to contain this request in the header. Hence, we will need a Global Session to maintain persistence between requests.

2. The rate limit is 10 request per minute and the token expires after 5 minutes. 

3. To regulate the rate limit, the semaphore is used to throttle the current request by adding sleep and making sure that only allowed number of requests are made per minute.

4. To handle the token expiration, we search for requests where `status_code != 200`. However, multiple such cases are possible, and we can create a new token for every such request, but for `status_code==429` i.e. too many requests, the server will not allow us to get a new token. Hence, we need to throttle the request and wait for some time before getting the token again.  

5. The extracted data is stored a json in `data.json` and this JSON file can then be used to write into a Database(preferrably NoSQL Databases). An image of my Database hosted on MLab has been stored as bson file in `db/crawler_data/apidata.bson`

## How to run?
1. Clone the repository into your system.
2. Open a Terminal Window in the Repository Folder. Make sure you have Docker installed locally on your system beforehand.
3. Run the Docker Daemon using `sudo dockerd` in a Terminal Window.
4. Now, open another terminal window in your repository and run `sudo docker build -t <image_name> .` to build the application using Docker.
5. To run the Docker image now, execute `sudo docker run <image_name>`
6. The data will be saved to `data.json`.
7. This JSON file can now be used to write into any database.

As an example, I have made a seperate `db.py` file that writes to a Mongo Database hosted on MLab. A copy of the database image is stored in `db/crawler_data/apidata.bson`. 

## Schema Details of the Database

I am using MongoDB to store the scraped data because of the flexibility it provides us. Also, MongoDB can store JSON data easily, without the need of storing it as a string (in MySQL).

The structure of the BSON file is- 

database Object -> Category Name -> Array of APIs(Name, Description, Auth, HTTPS, CORS, Link, Category)

```json

{
    "database":{
        "Animals":[
            {
                "name":"",
                "description":"",
                "cors":"",
                "https":"",
                "auth":"",
                "link":"",
                "category":""
            },
            {

            }
            .
            .
        ]
    }
}


```
## Delieverables - What have I achieved?

- [x] Object Oriented
- [x] Support for Authentication
- [x] Support for Pagination
- [x] Support for Rate Limiting
- [x] Crawls all Entries for all Categories
- [x] Support for Token Expiration


## Delieverables - What have I not achieved?

I have successfully tried to achieve all the required targets.

## What would I have improved on if given more days?

-  Migrating the code to Node.js to leverage JavaScript's default Asynchronous Behaviour without using any external libraries (requires in-depth knowledge of Node.js on my part. Hence Python xD)

#### Made with Love by Parul Chandel! 