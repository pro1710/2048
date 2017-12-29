import random
from agents import BasePlayer


class SimpleComputerPlayer(BasePlayer):
    def make_turn(self, board):
        cells = board.get_empty_cells()
        return random.choice(cells) if cells else None
