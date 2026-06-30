import json
import random
from pathlib import Path

from .board import Board
from .player import Player


class Game:
    WIN_LENGTH = 5

    def __init__(self, size=25):
        self.size = size
        self.win_length = self.WIN_LENGTH
        self.board = Board(size)
        self.player1 = Player("Player 1", "X")
        self.player2 = Player("Player 2", "O")
        self.current_player = random.choice([self.player1, self.player2])
        self.score_x = 0
        self.score_o = 0
        self.history = []

    def make_move(self, x, y, player=None):
        if player is None:
            target_player = self.current_player
            try:
                success = target_player.make_move(self.board, x, y)
            except Exception:
                return False

            if success:
                self.history.append((target_player.symbol, x, y))
                self.current_player = self.player2 if target_player == self.player1 else self.player1
            return success

        if isinstance(player, Player):
            symbol = player.symbol
        elif isinstance(player, str):
            symbol = player.upper()
        elif player in (True, False):
            symbol = "X" if player else "O"
        else:
            return False

        try:
            success = self.board.make_move(x, y, symbol)
        except Exception:
            return False

        if success:
            self.history.append((symbol, x, y))
        return success

    def play(self, x, y):
        return self.make_move(x, y)

    def new_game(self, size=None):
        if size is not None:
            self.size = size
        self.reset()

    def move(self, x, y):
        player_symbol = self.get_current_player()
        success = self.make_move(x, y)

        winner = self.get_winner() if success else None
        is_full = self.is_board_full()

        if success and winner is not None:
            if winner == "X":
                self.score_x += 1
            else:
                self.score_o += 1

        return {
            "success": success,
            "player": player_symbol if success else None,
            "winner": winner,
            "is_full": is_full,
            "next_player": self.get_current_player(),
            "game_over": winner is not None or is_full,
        }

    def get_current_player(self):
        return self.current_player.symbol

    def get_winner(self):
        return self.check_winner()

    def is_full(self):
        return self.is_board_full()

    def is_game_over(self):
        return self.get_winner() is not None or self.is_full()

    def get_size(self):
        return self.size

    def get_cell(self, x, y):
        value = self.board.board[x][y]
        if value is True:
            return "X"
        if value is False:
            return "O"
        return None

    def get_board(self):
        return [
            ["X" if cell is True else "O" if cell is False else None for cell in row]
            for row in self.board.board
        ]

    def _has_winning_line(self, row, col, row_step, col_step):
        start_value = self.board.board[row][col]
        if start_value is None:
            return False

        for offset in range(1, self.WIN_LENGTH):
            next_row = row + row_step * offset
            next_col = col + col_step * offset
            if not (0 <= next_row < self.board.size and 0 <= next_col < self.board.size):
                return False
            if self.board.board[next_row][next_col] != start_value:
                return False
        return True

    def check_winner(self):
        for row in range(self.board.size):
            for col in range(self.board.size - self.WIN_LENGTH + 1):
                if self._has_winning_line(row, col, 0, 1):
                    return "X" if self.board.board[row][col] else "O"

        for row in range(self.board.size - self.WIN_LENGTH + 1):
            for col in range(self.board.size):
                if self._has_winning_line(row, col, 1, 0):
                    return "X" if self.board.board[row][col] else "O"

        for row in range(self.board.size - self.WIN_LENGTH + 1):
            for col in range(self.board.size - self.WIN_LENGTH + 1):
                if self._has_winning_line(row, col, 1, 1):
                    return "X" if self.board.board[row][col] else "O"

        return None

    def is_board_full(self):
        return all(cell is not None for row in self.board.board for cell in row)

    def reset(self):
        if self.size <= 0:
            raise ValueError("size must be positive")

        self.board = Board(self.size)
        self.player1 = Player("Player 1", "X")
        self.player2 = Player("Player 2", "O")
        self.current_player = random.choice([self.player1, self.player2])
        self.history = []

    def save_game(self, path="savegame.json"):
        payload = {
            "board": [
                [" " if cell is None else "X" if cell is True else "O" for cell in row]
                for row in self.board.board
            ],
            "win_length": self.win_length,
            "history": list(self.history),
            "score_x": self.score_x,
            "score_o": self.score_o,
            "current_player": self.get_current_player(),
            "size": self.size,
        }
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
        return True

    def load_game(self, path="savegame.json"):
        target = Path(path)
        if not target.exists():
            return False

        with target.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)

        board_data = payload.get("board")
        if not board_data:
            return False

        self.size = int(payload.get("size", len(board_data)))
        self.win_length = int(payload.get("win_length", self.WIN_LENGTH))
        self.board = Board(self.size)
        self.player1 = Player("Player 1", "X")
        self.player2 = Player("Player 2", "O")

        for row_index, row in enumerate(board_data):
            for col_index, cell in enumerate(row):
                if cell == "X":
                    self.board.board[row_index][col_index] = True
                elif cell == "O":
                    self.board.board[row_index][col_index] = False
                else:
                    self.board.board[row_index][col_index] = None

        self.history = list(payload.get("history", []))
        self.score_x = int(payload.get("score_x", 0))
        self.score_o = int(payload.get("score_o", 0))

        current_player = payload.get("current_player", "X")
        self.current_player = self.player1 if current_player == "X" else self.player2
        return True

    def __str__(self):
        return str(self.board)