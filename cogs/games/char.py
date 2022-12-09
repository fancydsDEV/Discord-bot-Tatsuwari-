import random


class Player:
    def __init__(self, coins, luck):
        self.coins = coins
        self.luck = luck


p = Player(0, random.randint(0, 5))
