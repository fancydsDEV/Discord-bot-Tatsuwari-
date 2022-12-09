from disnake.ext import commands


class bot_is_on(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"--{self.bot.user}-WOKE-UP-FROM-BED-😈--")


def setup(bot: commands.bot):
    bot.add_cog(bot_is_on(bot))
