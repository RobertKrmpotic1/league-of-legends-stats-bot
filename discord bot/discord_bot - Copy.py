import discord
from config import DiscordBot
from loguru import logger
from account import getaccountID
import main, database
from config import APIConfig

token = DiscordBot.api_token
APIkey = APIConfig.api_key
client = discord.Client(intents=discord.Intents.all())
GUILD = "botbot server"


@client.event
async def on_ready():
    logger.debug("Ready")
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )


async def get_puuid_from_message(message):
    user = main.command_to_username(message)
    puuid = main.get_puuid(user, APIkey)
    return puuid, user


@client.event
async def on_message(message):
    # dont response to your own messages
    if message.author == client.user:
        return
    logger.debug(message.content)
    if message.content.startswith("!check"):
        puuid, user = await get_puuid_from_message(message)
        if puuid == "":
            await message.channel.send(
                f"{user} is invalid username. Check the spelling."
            )
            return

        percentage, game_count = main.check_winrate(puuid, APIkey)
        games_today, games_won = main.check_today_stats(puuid)

        comment = main.get_comment_for_todays_performance(games_today, games_won)

        if game_count == 0:
            await message.channel.send(
                f"{user} has no games that are in my database. Try !quickupdate or !update "
            )
        else:
            await message.channel.send(
                f"{user} has a winrate of {percentage} in {game_count} games that are in my database.\n"
                + comment
            )

    if message.content.startswith("!update"):
        puuid, user = await get_puuid_from_message(message)
        if puuid == "":
            await message.channel.send(
                f"{user} is invalid username. Check the spelling."
            )
            return

        logger.debug(f"Updating matches for {user}")
        successful_update = main.update_user_matches(puuid, APIkey, 2000)
        if successful_update:
            await message.channel.send(f"Data updated for user {user}")

    if message.content.startswith("!quickupdate"):
        puuid, user = await get_puuid_from_message(message)
        if puuid == "":
            await message.channel.send(
                f"{user} is invalid username. Check the spelling."
            )
            return

        logger.debug(f"Updating matches for {user}")
        successful_update = main.update_user_matches(puuid, APIkey, 20, 20)
        if successful_update:
            await message.channel.send(f"Quick data update for {user}. Last 20 games")


client.run(token)
