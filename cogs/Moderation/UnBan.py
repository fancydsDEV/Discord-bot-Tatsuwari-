import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
import datetime as dt


class UnBan(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(ban_members=True)
    async def unban(self,
                    ctx,
                    member: disnake.User,
                    reason="Not specified!",
                    ):
        embed = disnake.Embed(
            title="Unbanned!",
            description=f"Unbanned `{member}` with reason **{reason}**",
            colour=53759,
            timestamp=dt.datetime.now(dt.timezone.utc),
        )
        embed.set_author(
            name=self.bot.user.display_name, icon_url=f"{self.bot.user.avatar.url}"
        )
        embed.set_footer(
            text=f"Moderator : {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url,
        )
        await ctx.guild.unban(user=member, reason=reason)
        await ctx.send(embed=embed)


def setup(bot: commands.bot):
    bot.add_cog(UnBan(bot))
