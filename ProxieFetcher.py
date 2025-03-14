#By Wjatscheslaw Schezkin
import asyncio
import aiohttp
import re
import logging
class ProxyFetcher:
    def __init__(self, log_level=logging.DEBUG, log_file=None):
        if log_file:
            logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(self.__class__.__name__)
        self.proxies = []
        self.valid_proxies = []

    async def fetch_proxies(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.sslproxies.org/") as response:
                text = await response.text()
                proxy_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+:\d+)')
                matches = proxy_pattern.findall(text)
                self.proxies = [f"http://{match}" for match in matches]

    async def validate_proxy(self, proxy, semaphore):
        async with semaphore:
            for attempt in range(3):  # Retry up to 3 times
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get("http://httpbin.org/ip", proxy=proxy, timeout=10) as response:
                            if response.status == 200:
                                self.logger.info(f"Valid proxy: {proxy}")
                                return proxy
                except (aiohttp.ClientError, asyncio.TimeoutError, ConnectionResetError) as e:
                    self.logger.warning(f"Attempt {attempt + 1}: Invalid proxy: {proxy} - {e}")
                    await asyncio.sleep(1)  
        return None

    async def get_valid_proxies(self):
        await self.fetch_proxies()
        semaphore = asyncio.Semaphore(10)  # Limit concurrent connections
        tasks = [self.validate_proxy(proxy, semaphore) for proxy in self.proxies]
        results = await asyncio.gather(*tasks)
        self.valid_proxies = [proxy for proxy in results if proxy is not None]

    def run(self):
        asyncio.run(self.get_valid_proxies())
        self.logger.info(f"Valid proxies: {self.valid_proxies}")

if __name__ == "__main__":
    proxy_fetcher = ProxyFetcher()
    proxy_fetcher.run()
