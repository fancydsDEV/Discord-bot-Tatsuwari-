import json
from disnake.ext import commands
import disnake
import requests
import datetime


class FootBall_stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def football(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
        querystring = {"iso_date": "2022-11-22"}
        headers = {
            # YOUR KEY
            "X-RapidAPI-Key": "KEY",
            "X-RapidAPI-Host": "football-prediction-api.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        team1 = data['data'][0]['home_team']
        team2 = data['data'][0]['away_team']
        market = data['data'][0]['market']
        competition_cluster = data['data'][0]['competition_cluster']
        season = data['data'][0]['season']
        result = data['data'][0]['result']

        embed = disnake.Embed(title='FootBall Stats',
                              description=f'Information FootBall',
                              colour=0x3A3441,
                              timestamp=datetime.datetime.now())

        embed.set_author(name=inter.guild.name,
                         icon_url=inter.guild.icon)

        embed.add_field(name='Team 1:', value=team1, inline=False)
        embed.add_field(name='Team 2:', value=team2, inline=False)
        embed.add_field(name='market:', value=market, inline=False)
        embed.add_field(name='competition cluster:', value=competition_cluster, inline=False)
        embed.add_field(name='season: ', value=season, inline=False)
        embed.add_field(name='result:', value=result, inline=False)
        embed.set_footer(text=f"ask by {inter.user.name}",
                         icon_url=inter.user.avatar)

        await inter.send(embed=embed, delete_after=100)


def setup(bot: commands.bot):
    bot.add_cog(FootBall_stats(bot))
