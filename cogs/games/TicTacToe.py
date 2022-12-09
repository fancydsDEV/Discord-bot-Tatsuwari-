from typing import List

import disnake
from disnake.ext import commands


# </script>

# Tic Tac Toe Dings
class TIC_TAC_TOE_Frontend(disnake.ui.Button["TicTacToe"]):
    def __init__(self, y: int, x: int):
        # \u200b
        super().__init__(style=disnake.ButtonStyle.gray, label="\u200b", row=y)
        self.y = y
        self.x = x

    async def callback(self, interaction: disnake.MessageInteraction):
        view: TIC_TAC_TOE_BACKEND = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return
        if view.active_player == view.X:
            self.style = disnake.ButtonStyle.success
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.active_player = view.O
            content = "O is turn"
        else:
            self.style = disnake.ButtonStyle.red
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.active_player = view.X
            content = "X is turn"

        if view.check_win():
            if view.X == 3:
                content = f"X has Won :)"
            else:
                content = f"O has been won :)"
            for i in range(len(view.children)):
                view.children[i].disabled = True

        if view.is_full_board():
            content = "Draw"

        await interaction.response.edit_message(content=content, view=view)


# Tic Tac Toe Fetchers
class TIC_TAC_TOE_BACKEND(disnake.ui.View):
    active_player: int
    children: List[TIC_TAC_TOE_Frontend]

    X = 2
    O = 1

    def __init__(self):
        super().__init__()
        self.active_player = self.X
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

        for x in range(3):
            for y in range(3):
                self.add_item(TIC_TAC_TOE_Frontend(x, y))

    def check_win(self):
        # vertical
        if self.board[0][0] == self.X and self.board[1][1] == self.X and self.board[2][2] == self.X:
            self.X = 3
            return True
        if self.board[0][0] == self.O and self.board[1][1] == self.O and self.board[2][2] == self.O:
            return True
        if self.board[0][2] == self.X and self.board[1][1] == self.X and self.board[2][0] == self.X:
            self.X = 3
            return True
        if self.board[0][2] == self.O and self.board[1][1] == self.O and self.board[2][0] == self.O:
            return True
        # hochkant
        if self.board[0][0] == self.X and self.board[1][0] == self.X and self.board[2][0] == self.X:
            self.X = 3
            return True
        if self.board[0][0] == self.O and self.board[1][0] == self.O and self.board[2][0] == self.O:
            return True
        if self.board[0][1] == self.X and self.board[1][1] == self.X and self.board[2][1] == self.X:
            self.X = 3
            return True
        if self.board[0][1] == self.O and self.board[1][1] == self.O and self.board[2][1] == self.O:
            return True
        if self.board[0][2] == self.X and self.board[1][2] == self.X and self.board[2][2] == self.X:
            self.X = 3
            return True
        if self.board[0][2] == self.O and self.board[1][2] == self.O and self.board[2][2] == self.O:
            return True
        # parallel
        if self.board[0][0] == self.X and self.board[0][1] == self.X and self.board[0][2] == self.X:
            self.X = 3
            return True
        if self.board[0][0] == self.O and self.board[0][1] == self.O and self.board[0][2] == self.O:
            return True
        if self.board[1][0] == self.X and self.board[1][1] == self.X and self.board[1][2] == self.X:
            self.X = 3
            return True
        if self.board[1][0] == self.O and self.board[1][1] == self.O and self.board[1][2] == self.O:
            return True
        if self.board[2][0] == self.X and self.board[2][1] == self.X and self.board[2][2] == self.X:
            self.X = 3
            return True
        if self.board[2][0] == self.O and self.board[2][1] == self.O and self.board[2][2] == self.O:
            return True
        return

    def is_full_board(self):
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x] == 0:
                    return False
        return True


# <script>

# DISCORD --> looks like Tic Tac Toe FrontEnd
class ttt(commands.Cog):
    """if the user click of the bomb then he validates coins"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def tic_tac_toe(self, inter):
        """Starts a tic-tac-toe game with yourself."""
        await inter.send("Tic Tac Toe:\n`X are begin`", view=TIC_TAC_TOE_BACKEND(), delete_after=400)


def setup(bot: commands.bot):
    bot.add_cog(ttt(bot))
