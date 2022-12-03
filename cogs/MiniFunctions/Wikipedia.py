from http.client import HTTPSConnection
import disnake
from disnake.ext import commands
import wikipediaapi
import datetime


class wikipedia(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # !wikipedia language name
    @commands.slash_command()
    async def wikipedia(self, inter, language, name):
        """enter language in country abbreviation"""
        try:
            embed = disnake.Embed(title=f"INFORMATION ABOUT {name}",
                                  description=f"Here you will find information about {name} in {language}",
                                  color=0xD2691E,
                                  timestamp=datetime.datetime.now())

            wiki_wiki = wikipediaapi.Wikipedia(language=language)
            page = wiki_wiki.page(name)
            if page.exists():
                embed.add_field(name=f"THE WEB LINK ABOUT {name}", value=page.fullurl, inline=True)
                # embed.set_thumbnail(url=f"{name}")
                embed.set_footer(text=f"ask by {inter.author.name}",
                                 icon_url=inter.author.avatar)
                await inter.send(embed=embed, delete_after=50)

            else:
                await inter.send("**the page is not exist**", delete_after=50)
        except disnake.ext.commands.errors.CommandInvokeError:
            print("ERR" + inter.author.name + "has error")


def setup(bot):
    bot.add_cog(wikipedia(bot))
