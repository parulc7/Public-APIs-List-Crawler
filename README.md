# Public APIs List Crawler

* Built entirely on Python without using any Scraping Framework
* Uses the SuperFast Asynchronous Programming Modules for Python -  `asyncio` and `aiohttp`
* Leverages Semaphores to limit the rate of requests made per minute, thus respecting the Rate Limit set by the Server

## How to run?
1. Clone the repository into your system.
2. Open a Terminal Window in the Repository Folder. Make sure you have Docker installed locally on your system beforehand.
3. Run the Docker Daemon using `sudo dockerd` in a Terminal Window.
4. Now, open another terminal window in your repository and run `sudo docker build -t apiCrawler` to build the application using Docker.
5. To run the Docker image now, execute `sudo docker run apiCrawler` 

## Schema Details of the Database


## Delieverables - What have I achieved?

- [x] Object Oriented
- [x] Support for Authentication
- [x] Support for Pagination
- [x] Support for Rate Limiting
- [x] Crawls all Entries for all Categories

## Delieverables - What have I not achieved?
- [ ] Support for Token Expiration -> I can't figure out a way to replace the old token with the new and resume the tasks from where it stopped. I thought about using a task queue for the same.

## What would I have improved on if given more days?

- Modularizing the Code
- Letting user give the inputs so that the scraper can be used like a Framework


#### Made with Love by Parul Chandel! 