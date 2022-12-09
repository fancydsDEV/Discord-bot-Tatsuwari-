import disnake
from disnake.ext import commands
from asyncio import sleep


class DeletingMsg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(kick_members=True)
    async def clear(self, *, inter: disnake.ApplicationCommandInteraction, amount: int):
        """Clears the chat"""
        await inter.response.defer()
        await inter.send(f'Deleted {amount} message(s)')
        await sleep(3)
        await inter.channel.purge(limit=amount)

    @clear.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You not have the **Permissions** to use This Command!")


def setup(bot: commands.bot):
    bot.add_cog(DeletingMsg(bot))
