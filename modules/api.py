"""Jednoduché API nad třídou Game.

Tato vrstva (facade) schovává vnitřní strukturu tříd Board / Player / Game
a nabízí jednoduché metody a "obyčejná" data (str, bool, dict, list),
se kterými se snadno pracuje z GUI nebo z testů.
"""

from .game import Game


class GameAPI:
    """Tenká vrstva nad třídou Game."""

    def __init__(self, size: int = 25):
        self.size = size
        self.game = Game(size)

    # --- Ovládání hry ----------------------------------------------------

    def new_game(self, size: int = None) -> None:
        """Založí novou hru. Pokud je zadáno `size`, změní i velikost desky."""
        if size is not None:
            self.size = size
        self.game = Game(self.size)

    def reset(self) -> None:
        """Restartuje aktuální hru (stejná velikost desky)."""
        self.game.reset()

    def move(self, x: int, y: int) -> dict:
        """Provede tah aktuálního hráče na pozici (x, y).

        Vrací slovník popisující stav hry po tahu:
            success     - True, pokud byl tah platný a proveden
            player      - symbol hráče, který tah provedl ("X"/"O"), nebo None
            winner      - symbol vítěze ("X"/"O"), nebo None
            is_full     - True, pokud je deska plná
            next_player - symbol hráče, který je na tahu jako další
            game_over   - True, pokud hra skončila (výhrou nebo remízou)
        """
        player_symbol = self.get_current_player()
        success = self.game.make_move(x, y)

        winner = self.get_winner() if success else None
        is_full = self.is_full()

        return {
            "success": success,
            "player": player_symbol if success else None,
            "winner": winner,
            "is_full": is_full,
            "next_player": self.get_current_player(),
            "game_over": winner is not None or is_full,
        }

    # --- Dotazy na stav ----------------------------------------------------

    def get_current_player(self) -> str:
        """Vrátí symbol hráče, který je právě na tahu."""
        return self.game.current_player.symbol

    def get_winner(self):
        """Vrátí symbol vítěze, nebo None pokud hra zatím nemá vítěze."""
        return self.game.check_winner()

    def is_full(self) -> bool:
        """True, pokud je celá deska zaplněná."""
        return self.game.is_board_full()

    def is_game_over(self) -> bool:
        """True, pokud hra skončila výhrou nebo remízou."""
        return self.get_winner() is not None or self.is_full()

    def get_size(self) -> int:
        return self.game.size

    def get_cell(self, x: int, y: int):
        """Vrátí obsah políčka (x, y) jako "X", "O" nebo None."""
        value = self.game.board.board[x][y]
        if value is True:
            return "X"
        if value is False:
            return "O"
        return None

    def get_board(self):
        """Vrátí celou desku jako 2D list symbolů ("X" / "O" / None)."""
        return [
            ["X" if cell is True else "O" if cell is False else None for cell in row]
            for row in self.game.board.board
        ]

    def __str__(self) -> str:
        return str(self.game.board)
