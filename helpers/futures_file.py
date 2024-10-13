from typing import List, Dict
from asyncio import Task
import discord

from .logging_file import Logger
from .errors_file import ErrorHandler
from .data_file import convert_list_list_dict_to_list_dict
from .pandas_file import create_excel_file
from .cleaning_file import clean_file

from discord_helpers import send_msg_with_ping
from twitter.get_twitter_data import get_all_followings_from_user, get_all_followers_from_user


logger = Logger()


async def get_followings_from_user_future(user_id: int, cookies: List[Dict], filename: str):
    last_followings = await get_all_followings_from_user(user_id, cookies)
    if not last_followings:
        logger.error(ErrorHandler.COOKIES_EXPIRED)
        return "Error"

    last_followings = convert_list_list_dict_to_list_dict(last_followings)
    await create_excel_file(last_followings, filename)
    logger.info("Excel file created !")
    return "Ok"


async def get_followers_from_user_future(user_id: int, cookies: List[Dict], filename: str):
    last_followers = await get_all_followers_from_user(user_id, cookies)
    if not last_followers:
        logger.error(ErrorHandler.COOKIES_EXPIRED)
        return "Error"

    last_followers = convert_list_list_dict_to_list_dict(last_followers)
    await create_excel_file(last_followers, filename)
    logger.info("Excel file created !")
    return "Ok"


async def future_result(task: Task, client: discord.Client, user_id: int, channel_id: int, filename: str):
    result = task.result()
    if result == "Error":
        logger.error("Something went wrong")
        msg_to_send = "Une erreur est survenue pendant la récupération des données"
        await send_msg_with_ping(client, channel_id, user_id, msg=msg_to_send)
        return
    
    logger.info("Sending file...")
    await send_msg_with_ping(client, channel_id, user_id, filename=filename)
    logger.info("Done !")
    await clean_file(filename)
    return
