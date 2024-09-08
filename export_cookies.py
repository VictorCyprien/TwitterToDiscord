from typing import List, Dict
import discord
import asyncio
from discord.ext import commands, tasks
from pymongo.errors import ServerSelectionTimeoutError
from table2ascii import table2ascii as t2a

from playwright.async_api import async_playwright, Playwright

from twitter import connect, create_driver, get_last_followers_from_user, get_last_followings_from_user, get_user_id_with_username
from helpers import open_json, save_json, get_env_config, create_excel_file, clean_file, Logger, MongoDBManager
from discord_helpers import build_msg, send_msg, set_activity_type


logger = Logger()


async def get_cookies():
    async with async_playwright() as playwright:
        browser = await create_driver(playwright)
        page = await browser.new_page()
        cookies = await connect(page)
    
    mongo_client.set_collection("cookies")
    mongo_client.drop_data_from_collection()
    for index, one_cookie in enumerate(cookies):
        one_cookie["_id"] = index
        keys_to_keep = ["_id", "name", "value"]
        cookies_filtred = {key: one_cookie[key] for key in keys_to_keep if key in one_cookie}
        mongo_client.add_data_to_collection(cookies_filtred)
    
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
