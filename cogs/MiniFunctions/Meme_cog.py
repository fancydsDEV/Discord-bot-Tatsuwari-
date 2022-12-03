from disnake.ext import commands
import disnake
import requests
import datetime


class meme_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = -1

    @commands.slash_command()
    async def meme(self, inter: disnake.ApplicationCommandInteraction):
        """Meme/joke about anything"""

        url = "https://memes9.p.rapidapi.com/api/list"

        querystring = {"genre": "memes", "type": "top"}

        headers = {
            # YOUR KEY
            "X-RapidAPI-Key": "KEY",
            "X-RapidAPI-Host": "memes9.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        self.counter += 1
        meme = data['memes_list'][self.counter]['url']

        embed = disnake.Embed(title='Memes',
                              description=f'MEMES about anything',
                              colour=0x8E3941,
                              timestamp=datetime.datetime.now())

        embed.set_author(name=inter.guild.name,
                         icon_url=inter.guild.icon)

        # embed.set_thumbnail(url=meme)
        embed.set_image(url=meme)

        embed.set_footer(text=f"ask by {inter.user.name}",
                         icon_url=inter.user.avatar)

        await inter.send(embed=embed, delete_after=100)


def setup(bot: commands.bot):
    bot.add_cog(meme_cog(bot))
