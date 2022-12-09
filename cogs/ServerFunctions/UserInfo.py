import disnake
from disnake.ext import commands
import datetime


class UserInfoCommand(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def userinfo(self, member: disnake.Member, inter: disnake.ApplicationCommandInteraction):
        """User Information"""
        role_names = [str(i) for i in member.roles]
        if '@everyone' in role_names:
            role_names.remove('@everyone')

        embed = disnake.Embed(title=f"{member.name} Info",
                              description=f"*This Information Is about {member.name}*",
                              colour=0x3f888f,
                              timestamp=datetime.datetime.now())
        embed.set_author(name=inter.guild.name,
                         icon_url=inter.guild.icon)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="**You are join discord on:**", value=member.created_at.strftime("%d.%m.%Y"), inline=True)
        embed.add_field(name="**Your top role is:**", value=member.top_role, inline=True)
        embed.add_field(name="**You are join the server on:**", value=member.joined_at.strftime("%d.%m.%Y"),
                        inline=True)
        embed.add_field(name="**Number of roles**:",
                        value=len(role_names),
                        inline=True)
        embed.add_field(name="**BOT**", value=member.bot, inline=True)
        embed.add_field(name="**Activity**", value=member.activity, inline=True)
        embed.add_field(name="**nickname**", value=member.nick, inline=True)
        embed.add_field(name="**Stats:**",
                        value=member.status,
                        inline=True)
        embed.add_field(name="Your Tag:", value=member, inline=True)
        embed.set_footer(text=f"ask by {inter.author.name}",
                         icon_url=inter.author.avatar)
        await inter.send(embed=embed, delete_after=50)

    @userinfo.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("I could not find that member...", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(UserInfoCommand(bot))
