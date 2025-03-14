#Wjatscheslaw Schezkin
import scrapy
from facebook_scraper.HeadGenerator import HeaderGenerator
import re

header_gen = HeaderGenerator()

username = "username"
password = "password"

class FacebookLoginSpider(scrapy.Spider):
    name = "facebook_login"
    allowed_domains = ["facebook.com"]
    start_urls = ["https://www.facebook.com/"]

    custom_settings = {
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "args": ["--disable-blink-features=AutomationControlled"],
        }
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.facebook.com/nieoznakowaneradiowozy",
            callback=self.login,
            meta={"playwright": True, "playwright_include_page": True},
            headers=header_gen.generate_headers(),
        )

    async def login(self, response):
        page = response.meta.get("playwright_page")

        if not page:
            self.logger.error("Playwright page not found in response meta!")
            return

        try:
            cookie_button = await page.query_selector('button[data-testid="cookie-policy-manage-dialog-accept-button"]')
            if cookie_button:
                await cookie_button.click()
                await page.wait_for_timeout(2000)
                self.logger.info("Accepted cookies.")
        except Exception as e:
            self.logger.error(f"Error handling cookies: {e}")

        await page.fill("#email", username)
        await page.fill("#pass", password)
        await page.click("button[name='login']")
        await page.wait_for_timeout(5000)

        try:
            popups = await page.query_selector_all('button[aria-label="Close"]')
            for popup in popups:
                await popup.click()
                self.logger.info("Closed post-login popup.")
        except Exception as e:
            self.logger.error(f"Error closing post-login popups: {e}")

        await page.screenshot(path="facebook_login.png")

        is_logged_in = await page.query_selector("[role='navigation']")

        if is_logged_in:
            self.logger.info("Successfully logged in.")
            yield scrapy.Request(
                url="https://www.facebook.com/nieoznakowaneradiowozy",
                callback=self.scrape_number_plates,
                meta={"playwright": True, "playwright_include_page": True},
                headers=header_gen.generate_headers(),
            )
        else:
            self.logger.error("Login failed! Check screenshot.")

    async def scrape_number_plates(self, response):
        page = response.meta.get("playwright_page")

        if not page:
            self.logger.error("Playwright page not found in response meta!")
            return

        await page.wait_for_selector("div[data-pagelet='MainFeed']", timeout=10000)
        self.logger.info("Loaded Facebook page content.")

        posts = await page.query_selector_all("div[data-ad-preview='message']")
        number_plates = []
        pattern = re.compile(r"[A-Z]{2,3}\s?\d{1,4}[A-Z]{0,2}")

        for post in posts:
            post_text = await page.evaluate('(el) => el.innerText', post)
            matches = pattern.findall(post_text)
            if matches:
                number_plates.extend(matches)

        self.logger.info(f"Extracted {len(number_plates)} number plates: {number_plates}")
        print("Extracted Number Plates:", number_plates)

        await page.screenshot(path="scraped_facebook_page.png")
        await page.close()
