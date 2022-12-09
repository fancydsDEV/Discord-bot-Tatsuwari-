import disnake
from disnake.ext import commands


class KickMod(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.has_permissions(kick_members=True)
    @commands.slash_command()
    async def kick(self, member: disnake.Member, inter: disnake.ApplicationCommandInteraction, reason):
        """Kick a member from the server."""
        if reason is None:
            await inter.send("**you must enter a reason**")
        if reason is not None:
            await inter.send(f"`the {member.name} is successfully kicked`")
            await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.send("`you not have the Permissions to use that!`")


def setup(bot):
    bot.add_cog(KickMod(bot))
