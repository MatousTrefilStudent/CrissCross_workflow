"""Minimal wrapper around the game logic."""

from .game import Game


class GameAPI:
    """Thin facade that exposes the game API to the GUI and tests."""

    def __init__(self, size: int = 25):
        self.game = Game(size)

    def new_game(self, size: int = None) -> None:
        self.game.new_game(size)

    def reset(self) -> None:
        self.game.reset()

    def move(self, x: int, y: int) -> dict:
        return self.game.move(x, y)

    def get_current_player(self) -> str:
        return self.game.get_current_player()

    def get_winner(self):
        return self.game.get_winner()

    def is_full(self) -> bool:
        return self.game.is_full()

    def is_game_over(self) -> bool:
        return self.game.is_game_over()

    def get_size(self) -> int:
        return self.game.get_size()

    def get_cell(self, x: int, y: int):
        return self.game.get_cell(x, y)

    def get_board(self):
        return self.game.get_board()

    def __str__(self) -> str:
        return str(self.game)
