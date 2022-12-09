import disnake
from disnake.ext import commands
import datetime


class ServerInfoCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def serverinfo(self, inter: disnake.AppCommandInteraction):
        """Server Information"""
        role_names = [str(i) for i in inter.guild.roles]
        if '@everyone' in role_names:
            role_names.remove('@everyone')
        embed = disnake.Embed(title="**Server Info**",
                              description="*This Information Is about the server*",
                              colour=0xF0C43F,
                              timestamp=datetime.datetime.now())
        embed.set_author(name=inter.guild.name,
                         icon_url=inter.guild.icon)
        embed.set_thumbnail(url=inter.guild.icon)
        embed.add_field(name="**The server is created in:**", value=inter.guild.created_at.strftime("%d.%m.%Y"),
                        inline=True)
        embed.add_field(name="**Number of roles**:", value=len(role_names), inline=True)
        embed.add_field(name="**Highest role**",
                        value=inter.user.top_role,
                        inline=True)
        embed.add_field(name="**The region of the server:**", value=inter.guild.region, inline=True)
        embed.add_field(name="**Member Count:**", value=inter.guild.member_count, inline=True)
        embed.add_field(name="**Owner of this server:**", value=inter.guild.owner)
        embed.set_footer(text=f"ask by {inter.user.name}",
                         icon_url=inter.user.avatar)
        await inter.response.send_message(embed=embed, delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(ServerInfoCommand(bot))
