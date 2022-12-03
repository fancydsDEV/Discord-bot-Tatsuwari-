from re import I
import disnake
from disnake.ext import commands
import datetime


class Ban(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(ban_members=True)
    async def ban(inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str):
        if reason is None:
            await inter.send("**you must enter a reason**")
        if reason is not None:
            await inter.send(f"`the {member.name} is successfully banned`")
            await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```you not have the Permissions to use that!```")


def setup(bot: commands.bot):
    bot.add_cog(Ban(bot))
