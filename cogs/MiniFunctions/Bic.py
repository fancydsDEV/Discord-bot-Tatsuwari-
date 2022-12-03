import disnake
from disnake.ext import commands
import requests
import datetime


class BITCOIN(commands.Cog):
    """This will be for a ping command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def bic(self, inter: disnake.AppCommandInteraction):
        """Get the bots current websocket latency."""
        url = 'https://rest.coinapi.io/v1/exchangerate/BTC/EUR'
        headers = {'X-CoinAPI-Key': 'KEY'} # YOUR KEY
        response = requests.get(url, headers=headers)

        current_rate = response.json()
        embed = disnake.Embed(title='BIC KURS TODAY',
                              description='this is to show you what the BTC class looks like today', colour=0xffff00,
                              timestamp=datetime.datetime.now())
        embed.set_thumbnail(url='https://media.giphy.com/media/JQpS5az5AyUQdRd36r/giphy.gif')
        embed.add_field(name='EUR-BTC', value=current_rate['asset_id_quote'])
        embed.add_field(name='EUR-BTC PRICE', value=f"{current_rate['rate']}€")
        embed.set_footer(text=f"ask by {inter.author.name}",
                         icon_url=inter.author.avatar)
        await inter.send(embed=embed, delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(BITCOIN(bot))
