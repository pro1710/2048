import pygame
import random
import time

from .game import Game
from .board import Board, Move


class GuiDisplayer:
    COLOR_MAP = {0: (100, 100, 100),
                 2: (153, 152, 146),
                 4: (153, 152, 146),
                 8: (196, 142, 66),
                 16: (168, 117, 47),
                 32: (239, 148, 112),
                 64: (220, 148, 100),
                 128: (226, 212, 86),
                 256: (188, 175, 60),
                 512: (60, 188, 147),
                 1024: (46, 209, 157),
                 2048: (158, 121, 206),
                 4096: (171, 129, 226),
                 9192: (222, 128, 226),
                 18384: (247, 68, 255),
                 32768: (202, 54, 209)}

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BACKGROUND = (153, 255, 204)

    SMALL_TEXT = None

    def __init__(self, width=600, height=600):
        pygame.init()
        pygame.display.set_caption('2048')

        self._width = width
        self._height = height
        self.SMALL_TEXT = pygame.font.Font('freesansbold.ttf', 7)
        self.TEXT = None
        self._game_display = pygame.display.set_mode((self._width, self._height))

    @property
    def game_display(self):
        return self._game_display

    def text_objects(self, text, font, color=BLACK):
        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()

    def draw_cell(self, pos, size, val, border):
        x, y = pos
        b_w, b_h = size

        pygame.draw.rect(self._game_display,
                         self.BLACK,
                         [x, y, b_w, b_h])

        pygame.draw.rect(self._game_display,
                         self.COLOR_MAP[val],
                         [x + border, y + border, b_w - 2 * border, b_h - 2 * border])

        if not self.TEXT:
            self.TEXT = pygame.font.Font('freesansbold.ttf', max((b_w//5, 7)))

        text_surface, text_rect = self.text_objects(str(val) if val else '', self.TEXT, self.BLACK)
        text_rect.center = (x + b_w // 2, y + b_h // 2)
        self._game_display.blit(text_surface, text_rect)

    def display(self, board, border=0):
        board_size = min(self._width, self._height) - 2 * border
        x, y = border, border

        board_block_size = len(board)
        block_width, block_height = board_size // board_block_size, board_size // board_block_size

        pygame.draw.rect(self._game_display, self.BLACK, [border//2, border//2, board_size+border, board_size+border])

        for line_idx in range(board_block_size):
            x = border
            for col_idx in range(board_block_size):
                self.draw_cell((x, y), (block_width, block_height), board.get_cell_value((line_idx, col_idx)), border//2)
                x += block_width
            y += block_height


class GuiGame(Game):
    KEY_TO_MOVES = {pygame.K_UP: Move.UP,
                    pygame.K_DOWN: Move.DOWN,
                    pygame.K_LEFT: Move.LEFT,
                    pygame.K_RIGHT: Move.RIGHT}

    def __init__(self, game_size=Board.DEFAULT_BOARD_SIZE):
        super().__init__(game_size)
        self._clock = pygame.time.Clock()
        self.displayer = GuiDisplayer()

    def _game_loop(self):
        game_exit = False

        is_player_turn = 1

        while not game_exit:
            if self.game_over():
                self.on_game_over()

            if is_player_turn:
                if not self.board.can_move():
                    print('game over')
                    self.is_game_over = True
                    continue
                else:
                    for event in pygame.event.get():

                        if event.type == pygame.QUIT:
                            game_exit = True
                            self.on_exit()

                        if is_player_turn and event.type == pygame.KEYDOWN:
                            if event.key in self.KEY_TO_MOVES:
                                    is_player_turn ^= self.board.make_move(self.KEY_TO_MOVES[event.key])

            else:
                cloned_board = self.board.clone()
                move = self.computer.make_turn(cloned_board)
                if move:
                    if self.board.get_cell_value(move) == 0:
                        self.board.set_cell_value(move, random.choice(self.values))
                else:
                    self.is_game_over = True
                is_player_turn ^= 1

            self.displayer.game_display.fill(GuiDisplayer.BACKGROUND)

            self.displayer.display(self.board, border=4)
            pygame.display.update()
            self._clock.tick(60)

    def on_game_over(self):
        # TODO: implement
        print('GAME OVER\nYour score is:', self.board.score())
        time.sleep(3)
        self.init_game()
        self.is_game_over = False

    def on_exit(self):
        pygame.quit()
        quit()

    def start(self):
        self.init_game()
        self._game_loop()
        self.on_game_over()
