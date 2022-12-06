# Board:
"""
| | |2|
| | | |
| | | |
| |4|2|
A = Move left
D = Move right
2, 4, 6, 8 etc..;;

"""
from numpy.random import choice
import numpy as np
from copy import deepcopy
from typing import Set, Optional, Dict, Union
import itertools
import secrets
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path
from os.path import abspath

assets_path = Path(abspath(__file__)).parent / "assets"


class Colors:
    def __init__(self) -> None:
        self.t_colors = {
            0: 0xFFA0B0BD,
            2: 0xFFDAE4EE,
            4: 0xFFCEE1EE,
            8: 0xFF7EB2F4,
            16: 0xFF6B97F6,
            32: 0xFF697EF7,
            64: 0xFF4861F7,
            128: 0xFF90D6EE,
            256: 0xFF84D3EE,
            512: 0xFF78D1EC,
            1024: 0xFF3FC5ED,
            2048: 0xFF2DC2ED
        }

    def get_color(self, k: int = 0) -> int:
        if k not in self.t_colors:
            k -= 1
            return self.t_colors[k]


colors = Colors()


class Tiles:
    def __init__(self, colors: Colors, tile_size) -> None:
        self.t_range = list(colors.t_colors.keys())
        self.t_cache, self.f_cache = [{}] * 2
        self.colors = colors
        self.tile_size = tile_size
        self.tile_outline = int((6 / 200) * self.tile_size)
        self.tile_radius = tile_size / 10

    @staticmethod
    def font_color(tile: int) -> int:
        return 0xFF656E77 if tile in {2, 4} else 0xFFF1F6F8

    def prep_font(self, font_size: int):
        font = ImageFont.truetype(str(assets_path / "AGAALER.TTF"), font_size, encoding="unic")
        self.f_cache[font_size] = font
        return font

    def build_tile(self, tile_size: int, t: int, font) -> bytes:
        t_im = Image.new("RGBA", (tile_size, tile_size), color=0x00000000)
        t_id = ImageDraw.Draw(t_im)
        t_id.rounded_rectangle(
            xy=[(0, 0), (tile_size, tile_size)],
            fill=self.colors.get_color(k=t),
            outline=0x00000000,
            width=self.tile_outline,
            radius=self.tile_radius,
        )
        if t != 0:
            tw, th = font.getsize(str(t))
            xt, yt = ((tile_size - tw) / 2), ((tile_size - th) / 2)
            t_id.text(xy=(xt, yt), text=str(t), font=font, fill=self.font_color(t))
        with BytesIO() as b_io:
            t_im.save(b_io, "PNG")
            b_io.seek(0)
            return b_io.read()

    def prep_tiles(self, tile_size: int = 200, tile_outline: int = 6) -> dict:
        font_size = int((52 / 200) * tile_size)
        font = self.f_cache.get(font_size) or self.prep_font(font_size=font_size)
        tiles = {t: self.build_tile(tile_size, t, font) for t in self.t_range}
        self.t_cache[tile_size] = tiles
        return tiles


def stack(board) -> None:
    for i, j in itertools.product(range(len(board)), range(len(board))):
        k = i
        while board[k][j] == 0 and k != len(board) - 1:
            k += 1
        if k != i:
            board[i][j], board[k][j] = board[k][j], 0


# break numbers with each other
def calculate_chars(board):
    for i, j in itertools.product(range(len(board) - 1), range(len(board))):
        if board[i][j] != 0 and board[i][j] == board[i + 1][j]:
            board[i][j] += board[i + 1][j]
            board[i + 1][j] = 0


def create_random_char(board) -> Optional[int]:
    beginning_rn_char = secrets.choice([2, 2, 4])
    row = np.random.randint(0, 4)
    if board[0][row] == 0:
        random_char = beginning_rn_char
        board[0][row] = random_char
        return random_char


def generated_metacharacter(board) -> np.ndarray:
    random_char = create_random_char(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            if random_char == board[3][j] or random_char == board[2][j] or random_char == \
                    board[1][j]:
                create_random_char(board)
        return board

    # Create random char for board


class Twenty:

    def __init__(
            self,
            size: int = 4,
            tile_size: int = 200,
            state_string: Optional[str] = None
    ) -> None:
        self.possible_moves = None
        self.__target = Set[int]
        self.random_char: int = 0
        self.board = np.zeros((4, 4), dtype=int)
        self.score: int = 0
        self.action: Dict[str, int] = {"up": 0, "right": 1, "down": 2, "left": 3}
        self.tile_size = tile_size
        self.tiles = Tiles(Colors(), tile_size)
        self.size = size
        if state_string:
            self.from_state_string(state_string=state_string)
        else:
            self.board = np.zeros((self.size, self.size), int)
            self.board = generated_metacharacter(board=self.board)
            self.board = generated_metacharacter(board=self.board)
        self.get_score()
        self.update_possible_moves()

    def __str__(self):
        return self.print_board()

    def print_board(self):
        return self.board

    def update_possible_moves(self) -> None:
        res, n, over = {}, 0, False
        for direction in list(self.action.values()):
            res[direction] = self.move(action=direction, evaluate=True)
            if not res[direction]:
                n += 1
        if n == 4:
            over = True
        res["over"] = over
        self.possible_moves = res

    def to_state_string(self) -> str:
        return ''.join(f'{self.tiles.t_range.index(i):02d}' for i in np.nditer(self.board))

    def from_state_string(self, state_string: str) -> None:
        self.board = np.reshape([self.tiles.t_range[int(state_string[i: i + 2])] for i in range(0, 32, 2)], (4, 4))

    def render(self, bytesio: bool = False) -> Union[Image.Image, BytesIO]:
        image_size = self.tile_size * self.size
        tile_outline = int((6 / 200) * self.tile_size)
        tiles = self.tiles.prep_tiles(tile_size=self.tile_size, tile_outline=tile_outline)
        im = Image.new(
            "RGB",
            (image_size + (tile_outline * 2), image_size + (tile_outline * 2)),
            0x8193A4,
        )
        for x, y in itertools.product(range(self.size), range(self.size)):
            im_t = Image.open(BytesIO(tiles[self.board[x][y]]))
            y1, x1 = self.tile_size * x, self.tile_size * y
            im.paste(im=im_t, box=(x1 + tile_outline, y1 + tile_outline), mask=im_t)
        if bytesio:
            buffer = BytesIO()
            im.save(buffer, 'PNG')
            buffer.seek(0)
            return buffer
        return im

    # Move Char to left
    def move_left(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                try:
                    if board[i][j] == self.random_char:
                        if board[i][j - 1] == 0:
                            board[i][j] = 0
                            board[i][j - 1] = self.random_char
                            break
                        if board[i][j - 1] == self.random_char:
                            board[i][j] = 0
                            self.random_char += self.random_char
                            self.score += 1
                            board[i][j - 1] = self.random_char
                            break
                except IndexError:
                    print("")
        return board

    # Move Char to right
    def move_right(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                try:
                    if board[i][j] == self.random_char:
                        if board[i][j + 1] == 0:
                            board[i][j] = 0
                            board[i][j + 1] = self.random_char
                            break
                        if board[i][j + 1] == self.random_char:
                            board[i][j] = 0
                            self.random_char += self.random_char
                            self.score += 1
                            board[i][j + 1] = self.random_char
                            break
                except IndexError:
                    print("")
        return board

    # Move Char to down
    def move(self,
             action: Union[int, str],
             evaluate: bool = False) -> Union[bool, 'Twenty']:
        if isinstance(action, str):
            action = self.action[action]
        copy_board = deepcopy(self.board)
        if action == 1:
            self.move_right(copy_board)
        elif action == 3:
            self.move_left(copy_board)
        rotate_board = np.rot90(copy_board, action)
        stack(rotate_board)
        calculate_chars(rotate_board)
        stack(rotate_board)
        copy_board = np.rot90(rotate_board, 4 - action)
        if np.array_equal(copy_board, self.board, equal_nan=False):
            return False
        if not evaluate:
            self.board = copy_board
            self.board = generated_metacharacter(board=self.board)
            return self
        return True

    def get_score(self) -> int:
        if self.score == 0:
            return 0
        return self.score

    def lose(self) -> bool:
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    return False
                if self.board[0][j] != 0 and self.board[1][j] != 0 and self.board[2][j] != 0 and self.board[3][j] != 0:
                    return True
        return True



# Run The Twenty Game
# def run():
#     twenty = Twenty()
#     tiles = Tiles(colors=colors, tile_size=4 * 4)
#     create_random_char(board=twenty.board)
#     while not twenty.lose():
#         try:
#             print(twenty.print_board())
#             moves = input("down, up, left, right: ").lower()
#             twenty.move(action=twenty.action[moves])
#             twenty.render().show()
#
#         except KeyError:
#             print("Try Again")
#     else:
#         print(f"You Lose our Score is: {twenty.get_score()}")
#         print(twenty.print_board())
#
#
# run()  # Run The Game

# CR: https://github.com/Z1R343L/libtwenty/blob/main/libtwenty/__init__.py
# inspired By Z1R343L
