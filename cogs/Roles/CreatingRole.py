import disnake
from disnake.ext import commands


class CreatingRoles(commands.Cog):
    """CREATING A ROLE."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(
        description="if you want to enter a color only in english and please connect words with '_'")
    @commands.has_permissions(manage_roles=True)
    async def admin_create_role(self, ctx, *, name, reason,
                                colour: disnake.Colour):
        """Create a role."""
        if reason is None:
            await ctx.send("You must enter a **reason**", delete_after=50)
        else:
            await ctx.send(f"The role **@{name}** is created...", delete_after=50)
            await ctx.guild.create_role(name=name, mentionable=True, permissions=disnake.Permissions(administrator=True), reason=reason,
                                        hoist=False, colour=colour)

    @admin_create_role.error
    async def admin_create_role_error(self, ctx, error):
        """Error handler for admin_create_role."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you not have the **Permissions** to use that!", delete_after=50)

    # !mod_create_role name reason
    @commands.slash_command(
        description="if you want to enter a color only in english and please connect words with '_'")
    @commands.has_permissions(manage_roles=True)
    async def mod_create_role(self, ctx, *, name, reason,
                              colour: disnake.Colour):
        """Create a role."""
        if reason is None:
            await ctx.send("you must enter a **reason**", delete_after=50)
        if reason is not None:
            await ctx.send(f"the role @**{name}** is created...", delete_after=50)
            await ctx.guild.create_role(name=name, mentionable=True, permissions=disnake.Permissions(ban_members=True, kick_members=True), reason=reason,
                                        hoist=False, colour=colour)

    @mod_create_role.error
    async def mod_create_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you not have the **Permissions** to use that!", delete_after=50)

    # !create_role name reason
    @commands.slash_command(
        description="if you want to enter a color only in english and please connect words with '_'")
    @commands.has_permissions(manage_roles=True)
    async def create_role(self, ctx, *, name, reason, colour: disnake.Colour):
        """Create a role."""

        if reason is None:
            await ctx.send("you must enter a **reason**", delete_after=50)
        if reason is not None:
            await ctx.send(f"*the role **{name}** is created...*", delete_after=50)
            await ctx.guild.create_role(name=name, mentionable=True, reason=reason, hoist=False, colour=colour)

    @create_role.error
    async def create_role_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("you not have the **Permissions** to use that!", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(CreatingRoles(bot))
