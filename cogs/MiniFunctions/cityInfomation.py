import disnake
from disnake.ext import commands
import requests
import datetime as dt


class City:
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description="it looks from which country your ip comes and gives information about the "
                                        "country")
    async def city_information(self, inter):
        try:
            url = "https://find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com/iplocation"
            querystring = {"apikey": "873dbe322aea47f89dcf729dcc8f60e8"}
            headers = {
                "X-RapidAPI-Key": "9093768468msh6d66ff881e9e524p1d23ebjsnb28346341fac",
                "X-RapidAPI-Host": "find-any-ip-address-or-domain-location-world-wide.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()

            embed = disnake.Embed(title="CountyInformation", description="Shows Your Country", colour=0xFF0000,
                                  timestamp=dt.datetime.now())
            embed.add_field(name='country:', value=data['country'])
            embed.add_field(name='zipCode:', value=data['zipCode'])
            embed.add_field(name='city:', value=data['city'])
            embed.add_field(name='currencyName:', value=data['currencyName'])
            embed.add_field(name='phoneCode:', value=data['phoneCode'])
            embed.add_field(name='languages:', value=data['languages'])
            embed.add_field(name='org:', value=data['org'])
            embed.set_thumbnail(data['currencySymbol'])
            embed.add_field(name='continent:', value=data['continent'])

            await inter.send(embed=embed, delete_after=100)
        except:
            await inter.send("**Page Not Found** *~404~*~**")
