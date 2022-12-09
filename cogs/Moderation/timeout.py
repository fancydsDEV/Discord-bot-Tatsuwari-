import disnake
from disnake.ext import commands
import datetime


class Timeout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # EIN 
    @commands.slash_command()
    @commands.default_member_permissions(kick_members=True)
    async def timeout(self, ctx, user: disnake.Member, duration: float, unitl: int, reason: str):
        """Timeout a member from the server."""

        if reason is None:
            await ctx.send("`enter pls a reason`")

        if user is None:
            await ctx.send("`enter pls a member`")

        else:
            await ctx.send("`successfully timed out`")
            await user.timeout(duration=duration, until=unitl, reason=reason)

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("```you not have the Permissions to use that!```")


def setup(bot: commands.bot):
    bot.add_cog(Timeout(bot))
