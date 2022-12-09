from re import I
import disnake
from disnake.ext import commands
import datetime


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.AppCommandInteraction, member: disnake.Member, reason: str):
        """Ban a member from the server."""
        if reason is None:
            await inter.send("**you must enter a reason**", delete_after=50)
        if reason is not None:
            await inter.send(f"`the {member.name} is successfully banned`", delete_after=50)
            await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, inter: disnake.AppCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.send("`you not have the Permissions to use that!`", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(Ban(bot))
