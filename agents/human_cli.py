from agents import BasePlayer
from game.board import Move


class HumanCliPlayer(BasePlayer):
    def make_turn(self, board):
        action_dict = {'w': Move.UP,
                       's': Move.DOWN,
                       'a': Move.LEFT,
                       'd': Move.RIGHT,
                       'q': Move.EXIT}
        action = None
        while action not in action_dict:
            action = input()

        return action_dict[action]
