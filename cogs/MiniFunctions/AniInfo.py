from disnake.ext import commands
import disnake
import requests
import datetime


class ani_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://anime-db.p.rapidapi.com/anime"
        self.headers = {
            # YOUR KEY
            "X-RapidAPI-Key": "KEY",
            "X-RapidAPI-Host": "anime-db.p.rapidapi.com"}

    @commands.slash_command()
    async def animes(self, inter: disnake.ApplicationCommandInteraction, animes):
        await inter.response.defer()
        try:
            querystring = {f"page": "1", "size": "10", "search": f"{animes}"}
            response = requests.request("GET", self.url, headers=self.headers, params=querystring)
            data = response.json()
            title = data['data'][0]['title']
            # genres
            genres = ', '.join(data['data'][0]['genres'])
            # Ranking
            ranking = data['data'][0]['ranking']

            # Status
            status = data['data'][0]['status']

            # synopsis / description

            synopsis = data['data'][0]['synopsis']

            # [Written by MAL Rewrite]

            description = synopsis.replace('[Written by MAL Rewrite]', '')

            # Image

            image = data['data'][0]['image']

            # More Information

            more_information = data['data'][0]['link']

            embed = disnake.Embed(title='Anime Info',
                                  description=f'Information About {animes}',
                                  colour=0x8E3941,
                                  timestamp=datetime.datetime.now())

            embed.set_author(name=inter.guild.name,
                             icon_url=inter.guild.icon)

            embed.set_thumbnail(url=image)

            embed.add_field(name='title of the anime:', value=title, inline=False)
            embed.add_field(name='Ranking of the anime:', value=ranking, inline=False)
            embed.add_field(name='Status of the anime:', value=status, inline=False)
            embed.add_field(name='description of the anime:', value=description[:609], inline=False)
            embed.add_field(name='genres of the name: ', value=genres, inline=False)
            embed.add_field(name='More Information:', value=more_information, inline=False)

            embed.set_footer(text=f"ask by {inter.user.name}",
                             icon_url=inter.user.avatar)

            await inter.send(embed=embed, delete_after=100)

        except IndexError as error:
            await inter.send("**Anime Not Found** ~404~", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(ani_info(bot))
