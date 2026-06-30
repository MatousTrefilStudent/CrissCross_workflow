import random

from .board import Board
from .player import Player


class Game:
    WIN_LENGTH = 5

    def __init__(self, size=25):
        self.size = size
        self.board = Board(size)
        self.player1 = Player("Player 1", "X")
        self.player2 = Player("Player 2", "O")
        self.current_player = random.choice([self.player1, self.player2])

    def make_move(self, x, y, player=None):
        if player is None:
            target_player = self.current_player
            try:
                success = target_player.make_move(self.board, x, y)
            except Exception:
                return False

            if success:
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
            return self.board.make_move(x, y, symbol)
        except Exception:
            return False

    def play(self, x, y):
        return self.make_move(x, y)

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
        self.board = Board(self.size)
        self.player1 = Player("Player 1", "X")
        self.player2 = Player("Player 2", "O")
        self.current_player = random.choice([self.player1, self.player2])