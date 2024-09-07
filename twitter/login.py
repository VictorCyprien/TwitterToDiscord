from typing import List
import asyncio
from playwright.async_api import Page, Cookie, TimeoutError

from helpers import save_json, get_env_config, Logger

logger = Logger()

async def connect(page: Page) -> List[Cookie]:
    env = get_env_config()

    logger.info("Logging to Twitter...")
    logger.info("Entering email...")
    await page.goto("https://x.com/login")
    await page.is_visible("input[type=text]")
    await asyncio.sleep(2)
    await page.fill("input[type=text]", env("TWIITER_LOGIN_EMAIL"))
    await asyncio.sleep(2)
    await page.locator('span:text("Suivant"), span:text("Next")').click()

    logger.info("Done !")
    await asyncio.sleep(2)
    logger.info("Entering username...")
    try:
        await page.fill("input[type=text]", env("TWITTER_LOGIN_USERNAME"), timeout=5000)
        await page.locator('span:text("Suivant"), span:text("Next")').click()
    except TimeoutError:
        logger.warning("Username not required, proceed...")
    await asyncio.sleep(2)
    logger.info("Done !")
    logger.info("Entering password...")
    await asyncio.sleep(2)
    await page.is_visible("input[type=password]")
    await page.fill("input[type=password]", env("TWITTER_LOGIN_PASSWORD"))
    await asyncio.sleep(2)
    await page.locator('span:text("Se connecter"), span:text("Log in")').click()
    logger.info("Done !")
    await asyncio.sleep(2)
    try:
        await page.fill("input[type=tel]", env("TWIITER_LOGIN_PHONE"), timeout=5000)
        await page.locator('span:text("Suivant"), span:text("Next")').click()
    except TimeoutError:
        logger.warning("Phone number not required, proceed...")
    await asyncio.sleep(3)
    logger.info("Connected !")

    cookies = await page.context.cookies()
    save_json("cookies.json", cookies)
    logger.info("Cookies saved for next login !")

    return cookies
