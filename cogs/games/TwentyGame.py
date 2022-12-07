from .TwentyConsole import main
from disnake.ext import commands
import disnake
import datetime as dt

image = main.Twenty()


class TwentyGame(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twentyImg = image.render()
        self.count = 0

    @commands.slash_command()
    async def twenty(self, inter: disnake.ApplicationCommandInteraction):

        fn = f"{image.to_state_string()}.png"
        embed = disnake.Embed.from_dict({"color": 0x00ff00,
                                         "timestamp": dt.datetime.now().isoformat(),
                                         "image": {"url": f"attachment://{fn}"}})
        file = disnake.File(image.render(bytesio=True), filename=fn)
        components = [
            disnake.ui.Button(label="⬅️", style=disnake.ButtonStyle.gray, custom_id="3"),
            disnake.ui.Button(label="⬇️", style=disnake.ButtonStyle.gray, custom_id="2"),
            disnake.ui.Button(label="➡️", style=disnake.ButtonStyle.gray, custom_id="1"),
            disnake.ui.Button(label="🛑", style=disnake.ButtonStyle.red, custom_id="quit"),
            disnake.ui.Button(label=f"{image.get_score()}", style=disnake.ButtonStyle.blurple, custom_id="score",
                              disabled=True),
        ],
        await inter.send(embed=embed, file=file, components=components)

    @commands.Cog.listener("on_button_click")
    async def on_button_click(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        # "up": 0, "right": 1, "down": 2, "left": 3
        if inter.component.custom_id == "1":
            image.move(image.action['right'])
        elif inter.component.custom_id == "2":
            image.move(image.action['down'])
        elif inter.component.custom_id == "3":
            image.move(image.action['left'])
        elif inter.component.custom_id == "quit" or not image.lose():
            await inter.message.edit("You quited The game", delete_after=0)
            await inter.message.delete("You lose", delete_after=10)

        self.count += 1
        fn = f"{image.to_state_string()}{self.count}.png"
        file = disnake.File(image.render(bytesio=True), filename=fn)
        components = [
            disnake.ui.Button(label="⬅️", style=disnake.ButtonStyle.gray, custom_id="3"),
            disnake.ui.Button(label="⬇️", style=disnake.ButtonStyle.gray, custom_id="2"),
            disnake.ui.Button(label="➡️", style=disnake.ButtonStyle.gray, custom_id="1"),
            disnake.ui.Button(label="🛑", style=disnake.ButtonStyle.red, custom_id="quit"),
            disnake.ui.Button(label=f"{image.get_score()}", style=disnake.ButtonStyle.blurple, custom_id="score",
                              disabled=True),
        ],
        embed = disnake.Embed.from_dict({"color": 0x00ff00,
                                         "timestamp": dt.datetime.now().isoformat(),
                                         "image": {"url": f"attachment://{fn}"}})
        file = disnake.File(image.render(bytesio=True), filename=fn)
        await inter.message.edit(embed=embed, file=file, attachments=[], components=components)


def setup(bot):
    bot.add_cog(TwentyGame(bot))
