import pytest
from modules.game import Game


class TestGame:
    def test_game_initialization(self):
        """Test that game initializes with correct default state"""
        game = Game()
        assert game is not None
        assert game.board is not None
    
    def test_board_size(self):
        """Test that board has correct dimensions"""
        game = Game()
        assert game.board.size == 25
        assert len(game.board.board) == 25
        assert all(len(row) == 25 for row in game.board.board)
    
    def test_initial_board_empty(self):
        """Test that initial board is empty"""
        game = Game()
        for row in game.board.board:
            for cell in row:
                assert cell is None or cell == "."
    
    def test_make_move_valid(self):
        """Test making a valid move"""
        game = Game()
        result = game.play(0, 0)

        assert result is True
        assert game.board.board[0][0] in (True, False)
    def test_make_move_invalid_occupied(self):
        """Test that move on occupied cell fails"""
        game = Game()
        game.make_move(0, 0, "X")
        result = game.make_move(0, 0, "O")
        assert result is False

    def test_make_move_invalid_position(self):
        """Test that move on an out-of-bounds position fails"""
        game = Game()
        result = game.make_move(25, 25, "X")
        assert result is False

    def test_check_winner_horizontal(self):
        """Test horizontal win detection"""
        game = Game()
        for col in range(5):
            game.make_move(0, col, "X")
        winner = game.check_winner()
        assert winner == "X"
    
    def test_check_winner_vertical(self):
        """Test vertical win detection"""
        game = Game()
        for row in range(5):
            game.make_move(row, 0, "X")
        winner = game.check_winner()
        assert winner == "X"
    
    def test_check_winner_diagonal(self):
        """Test diagonal win detection"""
        game = Game()
        for index in range(5):
            game.make_move(index, index, "X")
        winner = game.check_winner()
        assert winner == "X"
    
    def test_check_no_winner(self):
        """Test that no winner is detected when board is empty"""
        game = Game()
        winner = game.check_winner()
        assert winner is None

    def test_is_board_full(self):
        """Test board full detection"""
        game = Game(3)
        moves = [(0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
                 (1, 0, "O"), (1, 1, "X"), (1, 2, "O"),
                 (2, 0, "O"), (2, 1, "X"), (2, 2, "O")]
        for row, col, player in moves:
            game.make_move(row, col, player)
        assert game.is_board_full() is True

    def test_reset_game(self):
        """Test game reset functionality"""
        game = Game()
        game.make_move(0, 0, "X")
        game.reset()
        for row in game.board:
            for cell in row:
                assert cell is None or cell == ""

