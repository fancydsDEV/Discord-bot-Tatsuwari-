from disnake.ext import commands
import disnake


class SolwMode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(manage_channels=True)
    # This command will set the slow-mode of the channel to seconds.
    async def slowmode(self, inter: disnake.ApplicationCommandInteraction, seconds: int):
        await inter.channel.edit(slowmode_delay=seconds)
        await inter.send(f"**Slow-mode** set to `{seconds}` seconds.", delete_after=50)

    @commands.slash_command()
    @commands.has_permissions(manage_channels=True)
    # Disable slow-mode
    async def slowmode_off(self, inter: disnake.ApplicationCommandInteraction):
        await inter.channel.edit(slowmode_delay=0)
        await inter.send(f"**Slow-mode** turned `off.`", delete_after=10)


def setup(bot: commands.Bot):
    bot.add_cog(SolwMode(bot))
