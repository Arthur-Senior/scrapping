#By Wjatscheslaw Schezkin
import asyncio
import aiohttp
import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PROXY_SOURCES = [
    "https://www.sslproxies.org/",
    "https://free-proxy-list.net/",
    "https://www.us-proxy.org/",
    "https://free-proxy-list.net/uk-proxy.html",
 
]

class ProxyFetcher:
    def __init__(self):
        self.proxies = set()
        self.valid_proxies = []

    async def fetch_proxies_from_source(self, session, url):
        try:
            async with session.get(url) as response:
                text = await response.text()
                proxy_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+:\d+)')
                matches = proxy_pattern.findall(text)
                for match in matches:
                    self.proxies.add(f"http://{match}")
                logger.info(f"Fetched {len(matches)} proxies from {url}")
        except Exception as e:
            logger.error(f"Error fetching proxies from {url}: {e}")

    async def fetch_all_proxies(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_proxies_from_source(session, url) for url in PROXY_SOURCES]
            await asyncio.gather(*tasks)

    async def validate_proxy(self, session, proxy):
        try:
            async with session.get("http://httpbin.org/ip", proxy=proxy, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"Valid proxy: {proxy}")
                    return proxy
        except Exception as e:
            logger.warning(f"Invalid proxy: {proxy} - {e}")
        return None

    async def validate_all_proxies(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.validate_proxy(session, proxy) for proxy in self.proxies]
            results = await asyncio.gather(*tasks)
            self.valid_proxies = [proxy for proxy in results if proxy is not None]

    def run(self):
        asyncio.run(self.fetch_all_proxies())
        asyncio.run(self.validate_all_proxies())
        logger.info(f"Total valid proxies: {len(self.valid_proxies)}")

if __name__ == "__main__":
    proxy_fetcher = ProxyFetcher()
    proxy_fetcher.run()
