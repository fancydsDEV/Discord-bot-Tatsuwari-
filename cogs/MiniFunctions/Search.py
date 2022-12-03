import disnake
from disnake.ext import commands
import webbrowser
import datetime


class Search(commands.Cog):
    """This will be for a searching(google) command."""

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def search(self, inter, serch):
        from serpapi import GoogleSearch

        params = {
            "engine": "google",
            "q": f"{serch}",
            "api_key": "KEY"
        }
        data = list(params.values())

        site_search = f"https://www.google.com/search?q={data[1]}"
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results["organic_results"]

        # title of the result
        title = organic_results[0]['title']
        # sites of result
        link_sites = organic_results[0]['link']
        # google picture from the result
        # image = organic_results[0]['thumbnail']

        # description
        description = organic_results[0]['about_this_result']['source']['description']

        embed = disnake.Embed(title='Search',
                              description=f'Information About {serch}',
                              colour=0x8A1941,
                              timestamp=datetime.datetime.now())

        embed.set_author(name=inter.guild.name,
                         icon_url=inter.guild.icon)

        # embed.set_thumbnail(url=image)

        embed.add_field(name='title of your result: ', value=title, inline=False)
        embed.add_field(name='page to your results:', value=link_sites, inline=False)
        embed.add_field(name='description of the name: ', value=description, inline=False)
        embed.add_field(name='link: ', value=site_search, inline=False)

        await inter.send(embed=embed, delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(Search(bot))
