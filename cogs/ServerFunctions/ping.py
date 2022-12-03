import disnake
from disnake.ext import commands


class PingCommand(commands.Cog):
    """This will be for a ping command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def ping(self, inter: disnake.AppCommandInteraction):
        """Get the bots current websocket latency."""
        await inter.response.send_message(f"Ping! `{round(self.bot.latency * 100)}ms`", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(PingCommand(bot))
