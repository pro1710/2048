import random

from game import BaseGame
from .board import Board


class Game(BaseGame):
    def __init__(self, game_size=Board.DEFAULT_BOARD_SIZE):
        super().__init__()
        self.board = Board(game_size)
        self.init_cells_count = max((game_size // 2, 2))
        self.values = [2, 4]

    def init_game(self):
        self.board.init()
        for pos in random.sample(self.board.get_empty_cells(), self.init_cells_count):
            self.board.set_cell_value(pos, random.choice(self.values))

    def game_over(self):
        return self.is_game_over or not self.board.can_move()

    def on_game_over(self):
        pass

    def start(self):
        pass
