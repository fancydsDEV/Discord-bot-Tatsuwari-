import disnake
from disnake.ext import commands


class Remove_ROLE(commands.Cog):
    """Remove Role."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.default_member_permissions(administrator=True)
    @commands.slash_command()
    async def remove_roles(self, ctx, member: disnake.Member, roles: disnake.Role, reason: str,
                           atomic: bool):
        if roles is None:
            await ctx.send("`the role is not exist`", delete_after=50)
        else:
            if reason is not None:
                await ctx.send("`the role be removed`", delete_after=50)
                await member.remove_roles(roles, reason=reason, atomic=atomic)
            else:
                await ctx.send("*Enter a reason!*", delete_after=50)

    @remove_roles.error
    async def remove_roles_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You not have the **Permissions** to use This Command!", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(Remove_ROLE(bot))
