from disnake.ext import commands
import disnake


class ChannelLock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, inter: disnake.ApplicationCommandInteraction):
        await inter.channel.set_permissions(inter.guild.default_role, send_messages=False)
        await inter.send(f"{inter.channel.mention} locked down.", delete_after=50)

    @commands.slash_command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.channel.set_permissions(inter.guild.default_role, send_messages=True)
        await inter.send(f"{inter.channel.mention} unlocked.", delete_after=50)


def setup(bot: commands.Bot):
    bot.add_cog(ChannelLock(bot))
