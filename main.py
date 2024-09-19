import discord
from discord.ext import commands, tasks
from pymongo.errors import ServerSelectionTimeoutError
from table2ascii import table2ascii as t2a
from datetime import datetime
import pytz

from twitter import get_last_followings_from_user, get_user_id_with_username, get_all_followers_from_user, get_all_followings_from_user
from helpers import convert_list_dict_to_dicts, get_env_config, create_excel_file, clean_file, Logger, MongoDBManager, ErrorHandler, RequestStatus
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


async def get_data_from_twitter(user_id: int):
    cookies = mongo_client.get_all_data_from_collection("cookies")
    if not cookies:
        logger.error(ErrorHandler.NO_COOKIES_IN_DATABASE)
        return []
    return await get_last_followings_from_user(user_id, cookies)


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
    users_data = mongo_client.get_all_data_from_collection("users")
    current_user_data = convert_list_dict_to_dicts(users_data)

    for user_id in current_user_data.keys():
        if current_user_data[user_id]["username"] == profil_name:
            await interaction.response.send_message(f"La profil de {profil_name} est déjà dans mon répertoire !")
            return


    cookies = mongo_client.get_all_data_from_collection("cookies")
    if not cookies:
        logger.error(ErrorHandler.COOKIES_EXPIRED)
        await interaction.response.send_message(ErrorHandler.DISCORD_MSG_ERROR)
        return
    user_id = await get_user_id_with_username(profil_name, cookies)
    if user_id is None:
        await interaction.response.send_message(f"Le profil {profil_name} n'a pas été trouvé sur Twitter.")
        return
    
    new_user_data = {
        "_id": user_id,
        "username": profil_name,
        "latest_following": "",
        "notifying_discord_channel": discord_channel.id,
        "last_check": None
    }

    mongo_client.add_data_to_collection("users", new_user_data)

    await interaction.response.send_message(f"Le profil de {profil_name} a été ajouté !")


@client.tree.command(name="remove_twitter_profile")
async def remove_twitter_profile(interaction: discord.Interaction, profil_name: str):
    """ Remove a twitter profile to the list
    """
    users_data = mongo_client.get_all_data_from_collection("users")
    current_user_data = convert_list_dict_to_dicts(users_data)

    for user_id in current_user_data.keys():
        if current_user_data[user_id]["username"] == profil_name:
            del current_user_data[user_id]
            mongo_client.remove_one_data_from_collection("users", {"username": profil_name})
            await interaction.response.send_message(f"Le profil de {profil_name} a été retiré !")
            return
        
    await interaction.response.send_message(f"Le profil de {profil_name} n'est pas dans la liste.")


@client.tree.command(name="get_list")
async def get_list(interaction: discord.Interaction):
    """ Get list of user
    """
    users_data = mongo_client.get_all_data_from_collection("users", {"_id": 0, "notifying_discord_channel": 0})
    
    filename = "Liste des utilisateurs suivi.xlsx"
    await create_excel_file(users_data, filename)
    await rename_column(filename, {'username': 'Utilisateur', 'latest_following': 'Dernier abonnement', 'last_check': 'Date du dernier abonnement'})

    await interaction.response.send_message(file=discord.File(filename))
    await clean_file(filename)


@client.tree.command(name="get_followers")
async def get_followers(interaction: discord.Interaction, profil_name: str):
    """ Get all followers of a user and send a Excel file
    """
    cookies = mongo_client.get_all_data_from_collection("cookies")
    if not cookies:
        logger.error(ErrorHandler.NO_COOKIES_IN_DATABASE)
        await interaction.response.send_message(ErrorHandler.DISCORD_MSG_ERROR)
        return
    
    user_id = await get_user_id_with_username(profil_name, cookies)
    if user_id is None:
        await interaction.response.send_message(f"Le profil {profil_name} n'a pas été trouvé sur Twitter.")
        return
    
    await interaction.response.defer(thinking=True)
    filename = f"{profil_name} - Followers.xlsx"
    logger.info(f"Getting data for user {profil_name} and creating followers list...")
    last_followers = await get_all_followers_from_user(user_id, cookies)
    if not last_followers:
        logger.error(ErrorHandler.COOKIES_EXPIRED)
        await interaction.followup.send(ErrorHandler.DISCORD_MSG_ERROR)
    await create_excel_file(last_followers, filename)

    logger.info("Excel file created !\nSending to Discord...")
    await interaction.followup.send(file=discord.File(filename))

    logger.info("Excel file sended !")
    await clean_file(filename)


@client.tree.command(name="get_followings")
async def get_followings(interaction: discord.Interaction, profil_name: str):
    """ Get all followings of a user and send a Excel file
    """
    cookies = mongo_client.get_all_data_from_collection("cookies")
    if not cookies:
        logger.error(ErrorHandler.NO_COOKIES_IN_DATABASE)
        await interaction.response.send_message(ErrorHandler.DISCORD_MSG_ERROR)
        return
    
    user_id = await get_user_id_with_username(profil_name, cookies)
    if user_id is None:
        await interaction.response.send_message(f"Le profil {profil_name} n'a pas été trouvé sur Twitter.")
        return
    
    await interaction.response.defer(thinking=True)
    filename = f"{profil_name} - Followings.xlsx"
    logger.info(f"Getting data for user {profil_name} and creating follwings list...")
    last_followings = await get_all_followings_from_user(user_id, cookies)
    if not last_followings:
        logger.error(ErrorHandler.COOKIES_EXPIRED)
        await interaction.followup.send(ErrorHandler.DISCORD_MSG_ERROR)
    await create_excel_file(last_followings, filename)

    logger.info("Excel file created !\nSending to Discord...")
    await interaction.followup.send(file=discord.File(filename))

    logger.info("Excel file sended !")
    await clean_file(filename)


@tasks.loop(minutes=15)
async def check_new_following():
    await set_activity_type(client, Activity.WATCHING, "les derniers following de la liste")
    users_data = mongo_client.get_all_data_from_collection("users")
    current_user_data = convert_list_dict_to_dicts(users_data)

    for user_id, user_data in current_user_data.items():
        username = user_data["username"]
        latest_following = user_data["latest_following"]
        discord_channel_id = user_data["notifying_discord_channel"]

        logger.info(f"Getting infos of {username}...")
        data_from_twitter = await get_data_from_twitter(int(user_id))
        if RequestStatus.status == "AUTH_PROBLEM":
            logger.error(ErrorHandler.COOKIES_EXPIRED)
            return
        elif RequestStatus.status == "USER_PROBLEM":
            logger.error("Unable to get user's data, maybe his account is private ?")
            continue

        try:
            last_following = data_from_twitter[0]["username"]
        except IndexError:
            logger.warning(f"The user {username} follow nobody right now, searching for next person...")
            continue

        if last_following == None:
            logger.warning(f"The last following of {username} cannot be seen...")
            continue

        if last_following == latest_following:
            logger.warning(f"Nothing new for {username}, searching for next person...")
            continue

        logger.info(f"New follower for {username} !")
        logger.info("Posting to channel...")
        mongo_client.update_one_data_from_collection(
            "users",
            {
                "_id": int(user_id)
            }, 
            {
                "$set": {
                    "latest_following": last_following, 
                    "last_check": pytz.timezone('Europe/Paris').localize(datetime.now()).strftime("%d/%m/%Y %H:%M:%S")
                }
            }
        )
        logger.info("Saved to database !")
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
    logger.error(ErrorHandler.ENV_NOT_SET)
    exit(0)

mongo_url = env("MONGODB_URL")
try:
    mongo_client = MongoDBManager(mongo_url, "data")
    mongo_client.ping()
except ServerSelectionTimeoutError:
    logger.error(ErrorHandler.DATABASE_ERROR_CONNECT)
    exit(1)

logger.info("Connected to MongoDB !")
client.run(token)
