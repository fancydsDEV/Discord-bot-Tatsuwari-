from disnake.ext import commands
import disnake
import datetime


class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.snipes = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.snipes[message.channel.id] = (message.content, message.author, message.channel.name, message.created_at)

    @commands.slash_command(name="snipe", description="Snipe a deleted message")
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time = self.snipes[ctx.channel.id]

        except:
            await ctx.send("There is nothing to snipe!")
            return

        embed = disnake.Embed(description=contents, color=disnake.Color.blurple(), timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Deleted in: #{channel_name}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Snipe(bot))
