# Public APIs List Crawler

* Built entirely on Python without using any Scraping Framework
* Uses the SuperFast Asynchronous Programming Modules for Python -  `asyncio` and `aiohttp`
* Leverages Semaphores to limit the rate of requests made per minute, thus respecting the Rate Limit set by the Server

## How to run?
1. Clone the repository into your system.
2. Open a Terminal Window in the Repository Folder. Make sure you have Docker installed locally on your system beforehand.
3. Run the Docker Daemon using `sudo dockerd` in a Terminal Window.
4. Now, open another terminal window in your repository and run `sudo docker build -t <image_name .` to build the application using Docker.
5. To run the Docker image now, execute `sudo docker run -it --rm apicrawler` 

## Schema Details of the Database




## Delieverables - What have I achieved?

- [x] Object Oriented
- [x] Support for Authentication
- [x] Support for Pagination
- [x] Support for Rate Limiting
- [x] Crawls all Entries for all Categories
- [x] Support for Token Expiration


## Delieverables - What have I not achieved?


## What would I have improved on if given more days?

- Modularizing the Code
- Letting user give the inputs so that the scraper can be used like a Framework


#### Made with Love by Parul Chandel! 