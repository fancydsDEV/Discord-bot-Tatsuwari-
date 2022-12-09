import disnake
from disnake.ext import commands
import youtube_dl
import asyncio
import datetime


class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def connect(self, inter: disnake.ApplicationCommandInteraction, cls: disnake.VoiceChannel):
        """Connect to a voice channel."""
        # inter.guild.voice_client
        if inter.guild.voice_client is not None:
            return await inter.guild.voice_client.move_to(cls)

        await inter.send(f"***{self.bot.user}*** is joined {cls} call!!", delete_after=50)

    @commands.slash_command()
    async def disconnect(self, inter: disnake.ApplicationCommandInteraction, cls: disnake.VoiceChannel):
        """If the bot is in a voice channel, disconnect it from there."""

        if not bool(len(cls.members)):
            await inter.send("`bot isint in call!?`", delete_after=50)
        else:
            await inter.send(f"***{self.bot.user}*** is leaving *{cls}* call!!", delete_after=50)
            await disnake.VoiceClient(client=self.bot, channel=cls).disconnect(force=True)

    @commands.slash_command()
    async def music(self, inter, cls: disnake.VoiceChannel, music_link):
        """Music for any VoiceChannel channel :)/* IT WORKS ONLY WITH YouTube Link!!!"""
        await inter.response.defer()
        try:

            yt_dl_opts = {'format': 'bestaudio/best'}
            ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

            ffmpeg_options = "C:/PATH_Programs/ffmpeg.exe"
            url = music_link

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            if 'list' in music_link:
                song = data['entries'][1]['url']
                embed = disnake.Embed(title=data['entries'][1]['title'], description=data['entries'][1]['description'],
                                      timestamp=datetime.datetime.now(), colour=0xED4245)
                embed.add_field(name='**Stats**', value='Played')
                embed.add_field(name='**VoiceChannel**', value=cls)
                embed.add_field(name='**Playlist**',
                                value=f"Loading playlist... it takes {len(data['entries'])} seconds, the music ***{data['entries'][1]['title']}*** is played...")
                embed.set_thumbnail('https://i.pinimg.com/originals/56/d0/f8/56d0f8eea832d52459f0fc0ae2466462.gif')
                embed.set_image(url=data['entries'][1]['thumbnail'])
                embed.set_footer(text=f"ask by {inter.author.name}",
                                 icon_url=inter.author.avatar)
                await inter.send(embed=embed, delete_after=50)
            else:
                song = data['url']
                embed = disnake.Embed(title=data['title'], description=data['description'],
                                      timestamp=datetime.datetime.now(), colour=0xED4245)
                embed.add_field(name='**Stats**', value='Played')
                embed.add_field(name='**VoiceChannel**', value=cls)
                embed.set_thumbnail('https://i.pinimg.com/originals/56/d0/f8/56d0f8eea832d52459f0fc0ae2466462.gif')
                embed.set_image(url=data['thumbnail'])
                embed.set_footer(text=f"ask by {inter.author.name}",
                                 icon_url=inter.author.avatar)

                await inter.send(embed=embed, delete_after=50)

            connect = await cls.connect()
            player = disnake.FFmpegPCMAudio(song, executable=ffmpeg_options)
            connect.play(player)

        except Exception as err:
            print(err)


def setup(bot: commands.bot):
    bot.add_cog(MusicCog(bot))
