import discord

async def set_activity_type(client: discord.Client, activity: discord.ActivityType, name: str):
    activity = discord.Activity(type=activity, name=name)
    await client.change_presence(status=discord.Status.online, activity=activity)
    