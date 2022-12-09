import disnake
from disnake.ext import commands


class AddRoles(commands.Cog):
    """ADDING A ROLE."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # !add_roles @User  @name_of_role reason
    @commands.slash_command()
    @commands.default_member_permissions(manage_guild=True, administrator=True)
    async def add_roles(self, ctx, member: disnake.Member, roles: disnake.Role, reason: str):
        """Add a role to a member."""
        try:
            if roles is None:
                await ctx.send(f"*the role **{roles}** is not exist*", delete_after=50)
            if reason is None:
                await ctx.send("Enter a **reason!**", delete_after=50)
            else:
                if reason is not None:
                    if roles in member.roles:
                        await ctx.send(f"*the role **{roles}** has {member}*", delete_after=50)
                    await member.add_roles(roles, reason=reason, atomic=True)
                    await ctx.send(f"**{member}** get @{roles} Role!", delete_after=50)
                else:
                    await ctx.send(f"you cant give {member} this {roles} role", delete_after=50)

        except disnake.ext.commands.errors.RoleNotFound:
            await ctx.send(f"Role {roles} not found.")

    @add_roles.error
    async def add_roles_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You not have the **Permissions** to use This Command!", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(AddRoles(bot))
