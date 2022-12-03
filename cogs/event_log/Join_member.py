import disnake
from disnake.ext import commands
import datetime as dt


class member_is_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, inter):
        embed = disnake.Embed(title=f"**NEW MEMBER {inter.name} :wave:**",
                              description="*Member Joined Now*",
                              colour=0x3f888f,
                              timestamp=dt.datetime.now())
        embed.set_author(name=inter.guild.name,
                         icon_url=inter.guild.icon)
        embed.set_thumbnail(url=inter.avatar)
        embed.add_field(
            name=f"```Hello Welcome to the server {inter.guild.name}\n\n, if you have any wishes or anything in your "
                 f"heart, please feel free to join the admins\n\nAnd we wish you to join the se"
                 f"rver {inter.guild.name} to feel comfortable```",
            inline=True, value='.')
        embed.set_footer(text=f"User: {inter.name}",
                         icon_url=inter.avatar)
        channel = self.bot.get_channel(1007956984915562506)
        # !add_roles @User  @name_of_role reason

        await channel.send(embed=embed, delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(member_is_join(bot))
