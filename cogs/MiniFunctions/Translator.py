import disnake
from disnake.ext import commands
import datetime as dt


class TL(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def translator(self, inter, language, text):
        from googletrans import Translator

        translator = Translator()
        translation = translator.translate(str(text), dest=language)
        embed = disnake.Embed(title="**Translator**", description="**you can use it to translate sentences or words**",
                              timestamp=dt.datetime.now(), colour=0x272775)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/eb/8d/84/eb8d84d6eca572d8defdaa4983690267.gif")
        embed.add_field(name="`The word do you translate: `", value=f"**{text}**", inline=True)
        embed.add_field(name="`in this language do trasnlate: `", value=f"**{language}**", inline=True)
        embed.add_field(name="`The word do tranlate is: `", value=f"**{translation.text}**", inline=False)
        embed.set_footer(text=f"ask by {inter.author.name}",
                         icon_url=inter.author.avatar)
        await inter.send(embed=embed, delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(TL(bot))
