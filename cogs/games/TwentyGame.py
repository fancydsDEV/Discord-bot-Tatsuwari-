from disnake.ext import commands
import disnake


class TwentyGame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def twenty(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        await inter.send("Game will be created in 4 Days")


def setup(bot):
    bot.add_cog(TwentyGame(bot))
