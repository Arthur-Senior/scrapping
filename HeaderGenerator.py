#by Wjatscheslaw Schezkin
import random

class HeaderGenerator:
    def __init__(self):
        self.chrome_versions = [f"{major}.{minor}.{build}.{patch}" for major in range(80, 92) for minor in range(0, 2) for build in range(4000, 4500) for patch in range(100, 150)]
        self.firefox_versions = [f"{major}.0" for major in range(85, 90)]
        self.safari_versions = [f"{major}.0.{minor}" for major in range(13, 15) for minor in range(1, 4)]
        self.android_versions = [f"{major}.{minor}" for major in range(8, 12) for minor in range(0, 3)]
        self.android_devices = ["SM-G975F", "Pixel 3", "Nexus 5X", "OnePlus 7T", "Huawei P30"]

        self.user_agents = [
            # Desktop Browsers
            lambda: f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(self.chrome_versions)} Safari/537.36",
            lambda: f"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(self.chrome_versions)} Safari/537.36",
            lambda: f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{random.choice(self.firefox_versions)}) Gecko/20100101 Firefox/{random.choice(self.firefox_versions)}",
            lambda: f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:{random.choice(self.firefox_versions)}) Gecko/20100101 Firefox/{random.choice(self.firefox_versions)}",
            lambda: f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.choice(self.safari_versions)} Safari/605.1.15",
            # Mobile Browsers
            lambda: f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{random.choice(self.safari_versions)} Mobile/15E148 Safari/604.1",
            lambda: f"Mozilla/5.0 (Linux; Android {random.choice(self.android_versions)}; {random.choice(self.android_devices)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(self.chrome_versions)} Mobile Safari/537.36"
        ]

        self.accept_languages = [
            "en-US,en;q=0.9",
            "en-GB,en;q=0.8",
            "en;q=0.7",
            "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
            "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
            "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
            "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7"
        ]

        self.accept_encodings = [
            "gzip, deflate, br",
            "gzip, deflate",
            "br"
        ]

        self.connections = [
            "keep-alive",
            "close"
        ]

        self.upgrade_insecure_requests = [
            "1",
            "0"
        ]

        self.accepts = [
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
        ]

        self.referers = [
            "https://www.google.com/",
            "https://www.bing.com/",
            "https://www.yahoo.com/",
            "https://www.duckduckgo.com/",
            "https://www.baidu.com/"
        ]

        self.dnt = [
            "1",
            "0"
        ]

    def generate_headers(self):
        headers = {
            "User-Agent": random.choice(self.user_agents)(),
            "Accept-Language": random.choice(self.accept_languages),
            "Accept-Encoding": random.choice(self.accept_encodings),
            "Connection": random.choice(self.connections),
            "Upgrade-Insecure-Requests": random.choice(self.upgrade_insecure_requests),
            "Accept": random.choice(self.accepts),
            "Referer": random.choice(self.referers),
            "DNT": random.choice(self.dnt)
        }
        return headers

    def test_header_diversity(self, num_samples=1000):
        generated_headers = [str(self.generate_headers()) for _ in range(num_samples)]
        unique_headers = set(generated_headers)
        unique_percentage = (len(unique_headers) / num_samples) * 100
        return unique_percentage

# Example usage
if __name__ == "__main__":
    header_gen = HeaderGenerator()
    headers = header_gen.generate_headers()
    print(headers)

    # Test header diversity
    run_counts = 1000000
    diversity_percentage = header_gen.test_header_diversity(run_counts)
    print(f"Unique headers percentage: {diversity_percentage:.2f}% by running {run_counts} times")
