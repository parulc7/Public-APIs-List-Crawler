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

#### Made with Love by Parul Chandel! 