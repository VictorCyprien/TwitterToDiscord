import asyncio
import discord
from playwright.async_api import async_playwright, Playwright

from discord.ext import commands, tasks

from twitter import connect, create_driver, get_last_following_from_user, get_last_followings_from_user
from helpers import open_json, save_json, get_env_config, Logger

logger = Logger()

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix="/", 
    description="Twitter2DiscordBot", 
    intents=intents
)


async def run(playwright: Playwright, user_id: int):
    browser = await create_driver(playwright)
    page = await browser.new_page()
    cookies = open_json("cookies.json")
    if not cookies:
        cookies = await connect(page)
    return await get_last_followings_from_user(user_id)


@client.event
async def on_ready():
    await client.wait_until_ready()
    logger.info("Twitter2DiscordBot en ligne !")
    try:
        #synced = await client.tree.sync()
        #logger.info(f"Synced : {len(synced)} command(s) !")
        check_new_following.start()
    except Exception as e:
        logger.info(e)


@client.tree.command(name="talk")
async def talk(interaction: discord.Interaction):
    """ Talk to bot !
    """
    await interaction.response.send_message("Hello !")


@tasks.loop(seconds=10)
async def check_new_following():
    current_user_data = open_json("accounts_data.json")

    for index, one_user in enumerate(current_user_data):
        for user_id, user_data in one_user.items():
            username = user_data["name"]
            latest_following = user_data["latest_following"]
            discord_channel_id = user_data["notifying_discord_channel"]

            async with async_playwright() as playwright:
                data = await run(playwright, user_id)
                logger.info(f"Data retrived for {username}")

            last_following = data[0]["username"]
            if last_following != latest_following:
                logger.info(f"New follower !\nPosting to channel...")
                user_data["latest_following"] = last_following
                save_json("accounts_data.json", current_user_data)

                discord_channel = client.get_channel(discord_channel_id)
                await discord_channel.send(f"{username} vient d'ajouter {last_following} dans sa liste d'abonnement !")
                logger.info("Msg send to discord !")
            else:
                logger.info("Nothing new, searching for next person...")


env = get_env_config()
client.run(env("DISCORD_BOT_TOKEN"))
