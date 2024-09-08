import asyncio
from pymongo.errors import ServerSelectionTimeoutError

from playwright.async_api import async_playwright

from twitter import connect, create_driver
from helpers import get_env_config, Logger, MongoDBManager


logger = Logger()


async def get_cookies():
    async with async_playwright() as playwright:
        browser = await create_driver(playwright)
        page = await browser.new_page()
        cookies = await connect(page)
    
    mongo_client.drop_data_from_collection("cookies")
    for index, one_cookie in enumerate(cookies):
        one_cookie["_id"] = index
        keys_to_keep = ["_id", "name", "value"]
        cookies_filtred = {key: one_cookie[key] for key in keys_to_keep if key in one_cookie}
        mongo_client.add_data_to_collection("cookies", cookies_filtred)
    
    logger.info("New cookies saved to database !")
    
env = get_env_config()
mongo_url = env("MONGODB_URL")
try:
    mongo_client = MongoDBManager(mongo_url, "data")
    mongo_client.ping()
except ServerSelectionTimeoutError:
    logger.error("Unable to connect to MongoDB, please check the url")
    exit(1)

asyncio.run(get_cookies())
