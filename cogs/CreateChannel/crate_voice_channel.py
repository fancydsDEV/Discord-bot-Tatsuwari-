import disnake
from disnake.ext import commands


class VoiceChannelCrate(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def create_voice_channel(
            self,
            inter,
            name: str,
            nsfw: bool,
            news: bool,
            reason: str,
    ):
        """Create a voice channel"""
        await inter.send(f"**THE {name} is created**", delete_after=50)
        await inter.guild.create_voice_channel(name=name, reason=reason, news=news, nsfw=nsfw)

    @create_voice_channel.error
    async def create_voice_channel_error(self, inter, error):
        if isinstance(error, commands.MissingPermissions):
            await inter.send("```you not have the Permissions to use that!```", delete_after=50)


def setup(bot: commands.bot):
    bot.add_cog(VoiceChannelCrate(bot))
