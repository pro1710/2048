class BaseGame:
    def __init__(self):
        self.displayer = None
        self.computer = None
        self.player = None
        self.is_game_over = False

    def init_game(self):
        pass

    def set_computer(self, player):
        self.computer = player

    def set_player(self, player):
        self.player = player

    def game_over(self):
        pass

    def on_game_over(self):
        pass

    def start(self):
        pass
