# auto-mod cog for the bot

import disnake
from disnake.ext import commands


class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.black_list_words = None
        self.bot = bot

    # Auto mod setup to get black listed words and check if the black list words are in the message and delete it and
    # give a warning and time out the user

    # Saved the black list as set() and if the message takes black listed words it will delete the message and give a
    # warning and time out the user
    @commands.has_role('Admin')
    @commands.slash_command()
    async def auto_mod_setup(self, inter, black_list_words: str):
        try:
            self.black_list_words = set(black_list_words.split())
            await inter.send('Auto mod is now on', delete_after=5)
        except:
            await inter.send('NO WORDS FOUND', delete_after=5)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author.bot:
            return
        if self.black_list_words is not None:
            if any(word in message.content for word in self.black_list_words):
                await message.delete()
                # give time out 3 hours
                await message.author.timeout(duration=10800, reason='Auto mod')
                await message.channel.send(f'{message.author.mention} you have been muted for 3 hours for using black '
                                           f'listed words', delete_after=5)

    @commands.slash_command()
    async def show_black_list_words(self, inter):
        if self.black_list_words is not None:
            await inter.send(f'Black list words are {self.black_list_words}', delete_after=20)
        else:
            await inter.send('No black list words found', delete_after=5)

    @commands.has_role('Mod')
    @commands.slash_command()
    async def add_words_black_list(self, inter, black_list_words: str):
        try:
            self.black_list_words.update(black_list_words.split())
            await inter.send('Added the black listed words', delete_after=5)
        except:
            await inter.send('No words found', delete_after=5)

    @commands.has_role('Mod')
    @commands.slash_command()
    async def remove_words_black_list(self, inter, black_list_words: str):
        try:
            self.black_list_words.difference_update(black_list_words.split())
            await inter.send('Removed the black listed words', delete_after=5)
        except:
            await inter.send('No words found', delete_after=5)

    @commands.has_role('Admin')
    @commands.slash_command()
    async def auto_mod_off(self, inter):
        try:
            self.black_list_words = None
            await inter.send('Auto mod is now off', delete_after=5)
        except:
            pass
        await inter.send('Auto mod is already off', delete_after=5)


def setup(bot):
    bot.add_cog(AutoMod(bot))
