import asyncio
from playwright.async_api import async_playwright, Playwright

from twitter import connect, create_driver, get_last_following_from_user, get_last_followings_from_user, get_headers
from helpers import open_json

async def run(playwright: Playwright):
    browser = await create_driver(playwright)
    page = await browser.new_page()
    cookies = open_json("cookies.json")
    if not cookies:
        cookies = await connect(page)
    await page.context.add_cookies(cookies)
    await get_last_followings_from_user(page)

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())

