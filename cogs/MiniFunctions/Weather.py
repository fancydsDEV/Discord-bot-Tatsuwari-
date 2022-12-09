import disnake
from disnake.ext import commands
import datetime
import requests


class Weather(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.slash_command()
    async def weather(self, inter: disnake.AppCommandInteraction, contry):
        """Weather Information"""
        api_key = "YOUR APP KEY"
        city = contry
        requests_url = f"http://api.openweathermap.org/data/2.5/weather?"
        url = requests_url + "appid=" + api_key + "&q=" + city
        response = requests.get(url).json()
        weather_description = response["weather"][0]["description"]
        temperature = response["main"]["temp"] - 273.15
        country_name = response["name"]
        win_speed = response['wind']["speed"]
        offset_in_seconds = response["timezone"]

        embed = disnake.Embed(title=f"Weather",
                              description=f"*This Weather Infomation Is about {str(country_name)}*",
                              colour=0x00FFFF,
                              timestamp=datetime.datetime.now())

        embed.add_field(":clock530: Offset In seconds: ", value=offset_in_seconds, inline=True)
        embed.add_field(":dash: Wind SPEED:", value=win_speed, inline=True)
        embed.add_field("Country Name:", value=country_name, inline=True)
        embed.add_field(":thermometer: Temperature", value=round(temperature), inline=True)
        embed.add_field("🌦️ Weather:", value=weather_description, inline=False)
        embed.set_image("https://i.pinimg.com/originals/0e/f3/bb/0ef3bb66d9216fffcea9022628f7bb26.gif")

        await inter.send(embed=embed, delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(Weather(bot))
