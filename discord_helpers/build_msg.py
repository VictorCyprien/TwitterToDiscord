from typing import Dict
import discord

from helpers import Logger


logger = Logger()


async def build_msg(client, data_from_twitter: Dict, current_user: str) -> discord.Embed:
    username = data_from_twitter["username"]
    name = data_from_twitter["name"]
    description = data_from_twitter["description"]
    profile_image = data_from_twitter["profile_image"]
    created_at = data_from_twitter["created_at"]
    followers_number = data_from_twitter["followers_number"]
    following_number = data_from_twitter["following_number"]
    urls = data_from_twitter.get("urls", "")
    tweets_count = data_from_twitter["tweets_count"]

    embed = discord.Embed(
        title=f"{current_user} vient de s'abonner à {name}",
        color=discord.Color.green()
    )
    embed.description = f"https://x.com/{username}"

    embed.set_thumbnail(url=profile_image)
    embed.add_field(name="Nom", value=name)
    embed.add_field(name="Description", value=description)
    embed.add_field(name="Crée le", value=created_at)
    embed.add_field(name="Nombre de followers", value=followers_number)
    embed.add_field(name="Nombre de following", value=following_number)
    embed.add_field(name="Nombre de tweets", value=tweets_count)

    if urls != "":
        embed.add_field(name="Liens", value=urls)

    logger.info("Msg builded !")
    return embed


async def send_msg(client: discord.Client, embed: discord.Embed, filename: str, discord_channel_id: int):
    discord_channel = client.get_channel(discord_channel_id)
    await discord_channel.send(embed=embed)
    await discord_channel.send(file=discord.File(filename))
    logger.info("Msg sended !")
