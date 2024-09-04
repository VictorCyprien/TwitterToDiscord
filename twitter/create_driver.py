from playwright.async_api import Playwright, Browser


async def create_driver(playwright: Playwright) -> Browser:
    return await playwright.webkit.launch(headless=True)
