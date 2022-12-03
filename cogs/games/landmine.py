from cogs.games.char import *
import disnake
from typing import List
from disnake.ext import commands
import numpy as np


class landmine_frontend(disnake.ui.Button["Mine"]):
    def __init__(self, y: int, x: int):
        super().__init__(style=disnake.ButtonStyle.gray, label="\u200b", row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: disnake.MessageInteraction):

        view: landmine_backend = self.view
        # for debugging;
        # print(view.board)
        # print(view.bomb_define_num, view.board[self.y][self.x])
        if 0 == view.board[self.y][self.x]:
            for table in range(len(view.board)):
                for nums in range(len(view.board[table])):
                    view.board[self.y][self.x] = view.player_one
                    self.disabled = True
                    self.label = "✅"

            content = "***you are save you have totals NOICE***"

        elif view.bomb_define_num == view.board[self.y][self.x]:
            # content="`Unfortunately they caught a bomb, so they lost :(`"
            p.coins -= 10
            custom_size = np.array([range(25)])
            numerate = custom_size.reshape((5, 5))
            for k, v in np.ndenumerate(numerate):
                view.children[v].custom_id = f"{str(k[0])}_{str(k[1])}"
                x, y = view.children[v].custom_id.split('_')
                if view.bomb_define_num == view.board[int(x)][int(y)]:
                    view.children[v].label = '💣'
                    content = "`Unfortunately they caught a bomb so they lost :(`"
                elif view.bomb_define_num != view.board[int(x)][int(y)]:
                    for i in range(len(view.children)):
                        view.children[i].disabled = True
                        view.children[v].label = "✅"

        elif 0 != view.board[self.y][self.x]:
            content = "`YOU WON YAY!!! YOU GET 1k`"

        await interaction.response.edit_message(content=content, view=view)


class landmine_backend(disnake.ui.View):
    children: List[landmine_frontend]
    player_one = 1

    active_player = player_one

    def __init__(self):
        self.board = [[0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        self.bomb_define_num = 2

        for i in range(len(self.board)):
            random_num_for_indexing_self_board = random.randint(0, 4)
            self.board[i][random_num_for_indexing_self_board] = self.bomb_define_num

        super().__init__()
        for x in range(5):
            for y in range(5):
                self.add_item(landmine_frontend(y, x))


class run_landmine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def landmine(self, inter):
        embed = disnake.Embed(title="**LETS GO, Dodge the bombs,...HHU**💣",
                              description=f"The Game is created by {inter.author.name}\nif you see any bug's in the "
                                          f"button game then please contact the admin so that we can fix the "
                                          f"bug\n*and if you win this game you can get 1000 coins ;)",
                              colour=0x5ba082)
        await inter.send(embed=embed, view=landmine_backend(), delete_after=400)


def setup(bot: commands.bot):
    bot.add_cog(run_landmine(bot))
