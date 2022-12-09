import datetime
from disnake.ext import commands, tasks
import disnake
import requests


class news(commands.Cog):

    def __init__(self, bot):
        self.index = 0
        self.bot = bot
        self.anime_news.start()
        self.channel = self.bot.get_channel(1042503230791372860)

    def cog_unload(self):
        self.anime_news.cancel()

    @tasks.loop(hours=2.0)
    async def anime_news(self):
        try:
            url = "https://anime-release.p.rapidapi.com/anime"

            headers = {
                # YOUR KEY
                "X-RapidAPI-Key": "YOUR APP KEY",
                "X-RapidAPI-Host": "anime-release.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers)
            data = response.json()

            title = data[self.index]['title']
            url = data[self.index]['url']

            embed = disnake.Embed(title='Anime News',
                                  description='her are anime/manga Releases',
                                  colour=0xFFD444,
                                  timestamp=datetime.datetime.now())

            embed.set_thumbnail(url='https://jw-webmagazine.com/wp-content/uploads/2020/03/Kimetsu-no-YaibaDemon'
                                    '-Slayer.jpg')
            embed.add_field(name='The Anime Names', value=title, inline=False)
            embed.add_field(name='The Url to the release web-site', value=url, inline=False)

            await self.channel.send(embed=embed)
            self.index += 1
        except IndexError as index:
            print(index)

    @anime_news.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

    @anime_news.error
    async def anime_news_error(self, error):
        formatted = "".join(traceback.format_exception(type(error), error, error.__traceback__))

        await self.bot.get_channel(self.channel).send(formatted)


def setup(bot: commands.bot):
    bot.add_cog(news(bot))
