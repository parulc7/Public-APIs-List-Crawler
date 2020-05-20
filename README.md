# Public APIs List Crawler

* Built entirely on Python without using any Scraping Framework
* Uses the SuperFast Asynchronous Programming Modules for Python -  `asyncio` and `aiohttp`
* Leverages Semaphores to limit the rate of requests made per minute, thus respecting the Rate Limit set by the Server

## Details

1. The extracted data is stored a json in `data.json` and as bson file in `db/crawler_data/apidata.bson`

2. The MongoDB used is hosted on MLab. 

## How to run?
1. Clone the repository into your system.
2. Open a Terminal Window in the Repository Folder. Make sure you have Docker installed locally on your system beforehand.
3. Run the Docker Daemon using `sudo dockerd` in a Terminal Window.
4. Now, open another terminal window in your repository and run `sudo docker build -t <image_name> .` to build the application using Docker.
5. To run the Docker image now, execute `sudo docker run -it --rm <image_name>` 

## Schema Details of the Database

I am using MongoDB to store the scraped data because of the flexibility it provides us. Also, MongoDB can store JSON data easily, without the need of storing it as a string (in MySQL).

The structure of the BSON file is- 

database Object -> Category Name -> Array of APIs(Name, Description, Auth, HTTPS, CORS, Link, Category)


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

- Letting user give the inputs so that the scraper can be used like a Framework

#### Made with Love by Parul Chandel! 