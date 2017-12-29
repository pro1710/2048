#!/usr/bin/env python3.6

import argparse
import sys

from game.cli_game import ConsoleGame
from game.gui_game import GuiGame
from agents.computer import SimpleComputerPlayer
from agents.human_cli import HumanCliPlayer


def parse_arguments(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--gui', '-g', action='store_true', help='run with GUI')
    parser.add_argument('--size', '-s', type=int, default=4, help='game board size')

    return parser.parse_args(args)


def play_cli(game_size):
    game = ConsoleGame(game_size)
    game.set_computer(SimpleComputerPlayer())
    game.set_player(HumanCliPlayer())

    game.start()


def play_gui(game_size):
    game = GuiGame(game_size)
    game.set_computer(SimpleComputerPlayer())
    game.start()


def main():
    parsed_args = parse_arguments(sys.argv[1:])
    if parsed_args.gui:
        play_gui(parsed_args.size)
    else:
        play_cli(parsed_args.size)


if __name__ == '__main__':
    main()
