import random
import platform

from .game import Game
from .board import Board, Move


class ConsoleDisplayer:
    COLOR_MAP = {
        0: 97,
        2: 40,
        4: 100,
        8: 47,
        16: 107,
        32: 46,
        64: 106,
        128: 44,
        256: 104,
        512: 42,
        1024: 102,
        2048: 43,
        4096: 103,
        8192: 45,
        16384: 105,
        32768: 41,
        65536: 101}

    TEMPLATE = '\x1b[%dm%7s\x1b[0m '

    def __init__(self):
        if 'Windows' == platform.system():
            self.display = self.win_display
        else:
            self.display = self.unix_display

    def display(self, board):
        pass

    @staticmethod
    def win_display(board):
        for i in range(board.size):
            for j in range(board.size):
                print('%6d  ' % board.get_cell_value((i, j)), end='')
            print('')
        print('')

    @staticmethod
    def unix_display(board):
        for i in range(3 * board.size):
            for j in range(board.size):
                v = board.get_cell_value((i // 3, j))

                if i % 3 == 1:
                    string = str(v).center(7, ' ')
                else:
                    string = ' '

                print(ConsoleDisplayer.TEMPLATE % (ConsoleDisplayer.COLOR_MAP[v], string), end='')
            print('')

            if i % 3 == 2:
                print('')


class ConsoleGame(Game):
    def __init__(self, game_size=Board.DEFAULT_BOARD_SIZE):
        super().__init__(game_size)
        self.displayer = ConsoleDisplayer()

    def on_game_over(self):
        print('Game Over.\nYour score is:', self.board.score())
        ans = input('Would you like to play again?(yes/no)')
        if ans.lower()[0] == 'y':
            self.is_game_over = False
            self.init_game()
        else:
            print('Goodbye!')

    def start(self):
        self.init_game()

        player_turn = 1

        while not self.game_over():
            self.displayer.display(self.board)
            cloned_board = self.board.clone()

            if player_turn:
                print('Player turn!', end='')
                move = self.player.make_turn(cloned_board)
                if move in Move.VMOVES:
                    if self.board.can_move([move]):
                        print(move)
                        if not self.board.make_move(move):
                            continue
                    else:
                        print('Cannot make player move: ', move)
                        self.is_game_over = True
                else:
                    print('Invalid player move: ', move)
                    self.is_game_over = True
            else:
                print('Computer turn!', end='')
                move = self.computer.make_turn(cloned_board)

                if move and self.board.get_cell_value(move) == 0:
                    print(move)
                    self.board.set_cell_value(move, random.choice(self.values))
                else:
                    print('Invalid computer move: ', move)

            if not self.game_over():
                player_turn ^= 1
            else:
                self.on_game_over()
