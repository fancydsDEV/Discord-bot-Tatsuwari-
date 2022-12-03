import disnake
from disnake.ext import commands


class reply_to_users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.count = 0

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        self.count += 1
        messages = await message.channel.history(limit=100).flatten()

        if message.content.startswith('hello'):
            await message.channel.send("hi", delete_after=50)

        elif "!help" in message.content:
            await message.channel.send("type --> **/help**", delete_after=50)

        elif "!end" in message.content:
            # messages = msg.content
            with open("ticket.txt", 'w') as f:
                for msg in messages:
                    ticket_msg = msg.content
                    f.write(f"{msg.author}: {ticket_msg}")
                    f.write('\n')


def setup(bot: commands.bot):
    bot.add_cog(reply_to_users(bot))
