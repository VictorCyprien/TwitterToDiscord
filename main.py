from typing import List, Dict
import discord
from discord.ext import commands, tasks

from table2ascii import table2ascii as t2a

from playwright.async_api import async_playwright, Playwright

from twitter import connect, create_driver, get_last_followers_from_user, get_last_followings_from_user, get_user_id_with_username
from helpers import open_json, save_json, get_env_config, create_excel_file, clean_file, Logger, MongoDBManager
from discord_helpers import build_msg, send_msg, set_activity_type

logger = Logger()

intents = discord.Intents.all()


class Activity():
    WATCHING = discord.ActivityType.watching.value
    PLAYING = discord.ActivityType.playing.value
    LISTENING = discord.ActivityType.listening.value


client = commands.Bot(
    command_prefix="/", 
    description="Twitter2DiscordBot", 
    intents=intents
)


async def run(playwright: Playwright, user_id: int):
    cookies: List = open_json("cookies.json")
    if not cookies:
        browser = await create_driver(playwright)
        page = await browser.new_page()
        await connect(page)
    return await get_last_followings_from_user(user_id)


@client.event
async def on_ready():
    await client.wait_until_ready()
    logger.info("Twitter2DiscordBot en ligne !")
    try:
        synced = await client.tree.sync()
        logger.info(f"Synced : {len(synced)} command(s) !")
        check_new_following.start()
    except Exception as e:
        logger.info(e)


@client.tree.command(name="talk")
async def talk(interaction: discord.Interaction):
    """ Talk to bot !
    """
    await interaction.response.send_message("Hello !")


@client.tree.command(name="add_twitter_profile")
async def add_twitter_profile(interaction: discord.Interaction, profil_name: str, discord_channel: discord.TextChannel):
    """ Add a twitter profile to the list
    """
    data: Dict = open_json("accounts_data.json")

    for user_id in data.keys():
        if data[user_id]["username"] == profil_name:
            await interaction.response.send_message(f"La profil de {profil_name} est déjà dans mon répertoire !")
            return


    user_id = await get_user_id_with_username(profil_name)
    if user_id is None:
        await interaction.response.send_message(f"Le profil {profil_name} n'a pas été trouvé sur Twitter.")
        return


    data[str(user_id)] = {}
    data[str(user_id)]["username"] = profil_name
    data[str(user_id)]["latest_following"] = ""
    data[str(user_id)]["notifying_discord_channel"] = discord_channel.id

    save_json("accounts_data.json", data)
    await interaction.response.send_message(f"Le profil de {profil_name} a été ajouté !")


@client.tree.command(name="remove_twitter_profile")
async def remove_twitter_profile(interaction: discord.Interaction, profil_name: str):
    """ Remove a twitter profile to the list
    """
    data: dict = open_json("accounts_data.json")

    for user_id in data.keys():
        if data[user_id]["username"] == profil_name:
            del data[user_id]
            save_json("accounts_data.json", data)
            await interaction.response.send_message(f"Le profil de {profil_name} a été retiré !")
            return
        
    await interaction.response.send_message(f"Le profil de {profil_name} n'est pas dans la liste.")


@client.tree.command(name="get_list")
async def get_list(interaction: discord.Interaction):
    """ Get list of user
    """
    data: Dict = open_json("accounts_data.json")

    table_string = t2a(
        header=["Nom", "Salon associé"],
        body=[[one_user['username'], client.get_channel(one_user["notifying_discord_channel"]).name] for one_user in data.values()],
        first_col_heading=True
    )

    await interaction.response.send_message(f"```\n{table_string}\n```")


@client.tree.command(name="get_followers")
async def get_followers(interaction: discord.Interaction, profil_name: str):
    user_id = await get_user_id_with_username(profil_name)
    if user_id is None:
        await interaction.response.send_message(f"Le profil {profil_name} n'a pas été trouvé sur Twitter.")
        return
    
    filename = f"{profil_name} - Followers.xlsx"
    logger.info(f"Getting data for user {profil_name} and creating followers list...")
    last_followers = await get_last_followers_from_user(user_id)
    if not last_followers:
        logger.error("Unable to get the latest data, please refresh cookies")
        await interaction.response.send_message("Impossible d'avoir les dernières données")
    await create_excel_file(last_followers, filename)

    logger.info("Excel file created !\nSending to Discord...")
    await interaction.response.send_message(file=discord.File(filename))

    logger.info("Excel file sended !")
    await clean_file(filename)


@client.tree.command(name="get_followings")
async def get_followings(interaction: discord.Interaction, profil_name: str):
    user_id = await get_user_id_with_username(profil_name)
    if user_id is None:
        await interaction.response.send_message(f"Le profil {profil_name} n'a pas été trouvé sur Twitter.")
        return
    
    filename = f"{profil_name} - Followings.xlsx"
    logger.info(f"Getting data for user {profil_name} and creating follwings list...")
    last_followings = await get_last_followings_from_user(user_id)
    if not last_followings:
        logger.error("Unable to get the latest data, please refresh cookies")
        await interaction.response.send_message("Impossible d'avoir les dernières données")
    await create_excel_file(last_followings, filename)

    logger.info("Excel file created !\nSending to Discord...")
    await interaction.response.send_message(file=discord.File(filename))

    logger.info("Excel file sended !")
    await clean_file(filename)


@tasks.loop(minutes=5)
async def check_new_following():
    await set_activity_type(client, Activity.WATCHING, "les derniers following de la liste")
    current_user_data = open_json("accounts_data.json")

    for user_id, user_data in current_user_data.items():
        username = user_data["username"]
        latest_following = user_data["latest_following"]
        discord_channel_id = user_data["notifying_discord_channel"]

        async with async_playwright() as playwright:
            data_from_twitter = await run(playwright, user_id)

        if not data_from_twitter:
            logger.error("Unable to get the latest data, please refresh cookies")
            return

        try:
            last_following = data_from_twitter[0]["username"]
        except IndexError:
            logger.warning(f"The user {username} follow nobody right now, searching for next person...")
            continue

        if last_following == latest_following:
            logger.warning(f"Nothing new for {username}, searching for next person...")
            continue

        logger.info(f"New follower for {username} !\nPosting to channel...")
        user_data["latest_following"] = last_following
        save_json("accounts_data.json", current_user_data)
        embed = await build_msg(data_from_twitter[0], user_data["username"])
        await send_msg(client, discord_channel_id, embed)
        logger.info("Message sended !")
    
    await set_activity_type(client, Activity.PLAYING, "trade du $MAD")


env = get_env_config()
current_environement = env("ENVIRONEMENT")
if current_environement == "PROD":
    token = env("DISCORD_BOT_TOKEN")
    logger.info("Running on prod")
elif current_environement == "DEV":
    token = env("DISCORD_BOT_TOKEN_DEV")
    logger.info("Running on dev")
else:
    logger.error("Please set an environement in .env file")
    exit(0)

mongo_url = env("MONGODB_URL")
mongo_client = MongoDBManager(mongo_url, "data")
logger.info("Connected to MongoDB !")
client.run(token)
