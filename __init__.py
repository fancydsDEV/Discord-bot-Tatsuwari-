import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv

load_dotenv('token.env')


activity = disnake.Activity(
    name=f"""--🔮-|/help | created by **laggy-bytes#5084**|-🔮--""",
    type=disnake.ActivityType.playing,
)

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all(), activity=activity)
bot.remove_command("help")

# When tse bot is ready, run this Files.

# MiniFunctions

bot.load_extension("cogs.MiniFunctions.Search")
bot.load_extension("cogs.MiniFunctions.Weather")
bot.load_extension("cogs.MiniFunctions.Wikipedia")
bot.load_extension("cogs.MiniFunctions.Translator")
bot.load_extension("cogs.MiniFunctions.Bic")
bot.load_extension("cogs.MiniFunctions.AniNews")
bot.load_extension("cogs.MiniFunctions.AniInfo")
bot.load_extension("cogs.MiniFunctions.Meme_cog")
bot.load_extension("cogs.MiniFunctions.FootballPrediction")

# ServerFunctions

bot.load_extension("cogs.ServerFunctions.DeletingMessage")
bot.load_extension("cogs.ServerFunctions.MusicCog")
bot.load_extension("cogs.ServerFunctions.UserInfo")
bot.load_extension("cogs.ServerFunctions.ServerInfo")
bot.load_extension("cogs.ServerFunctions.Help")
bot.load_extension("cogs.ServerFunctions.tag")
bot.load_extension("cogs.ServerFunctions.ping")
bot.load_extension("cogs.ServerFunctions.Ticket")
bot.load_extension("cogs.ServerFunctions.ChannelLock")
bot.load_extension("cogs.ServerFunctions.SlowMode")
bot.load_extension("cogs.ServerFunctions.AutoMod")

# CREATE CHANNEL
bot.load_extension("cogs.CreateChannel.crate_voice_channel")
bot.load_extension("cogs.CreateChannel.create_text_channel")

# Moderation
bot.load_extension("cogs.Moderation.ban")
bot.load_extension("cogs.Moderation.kick")
bot.load_extension("cogs.Moderation.timeout")
bot.load_extension("cogs.Moderation.UnBan")

# Roles
bot.load_extension("cogs.Roles.RemoveRoles")
bot.load_extension("cogs.Roles.AddRoles")
bot.load_extension("cogs.Roles.CreatingRole")

# games
bot.load_extension("cogs.games.game")
bot.load_extension("cogs.games.TicTacToe")
bot.load_extension("cogs.games.landmine")
bot.load_extension("cogs.games.TwentyGame")

# Event Log
bot.load_extension("cogs.event_log.bot_is_on")
bot.load_extension("cogs.event_log.Join_member")
bot.load_extension("cogs.event_log.reply_to_user")

# Run
bot.run(os.getenv('token'))
