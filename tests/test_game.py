from modules.game import Game


class TestGame:
    def test_game_initialization(self):
        game = Game()

        assert game is not None
        assert game.board is not None
        assert game.get_size() == 25
        assert game.get_current_player() in {"X", "O"}

    def test_board_size(self):
        game = Game()

        assert game.board.size == 25
        assert len(game.board.board) == 25
        assert all(len(row) == 25 for row in game.board.board)

    def test_initial_board_empty(self):
        game = Game()

        for row in game.get_board():
            for cell in row:
                assert cell is None

    def test_move_succeeds_and_updates_state(self):
        game = Game()
        first_player = game.get_current_player()

        result = game.move(0, 0)

        assert result["success"] is True
        assert result["player"] == first_player
        assert game.get_cell(0, 0) == first_player
        assert game.get_current_player() != first_player

    def test_move_on_occupied_cell_fails(self):
        game = Game()
        game.make_move(0, 0, "X")

        result = game.move(0, 0)

        assert result["success"] is False
        assert result["player"] is None
        assert game.get_cell(0, 0) == "X"

    def test_move_out_of_bounds_fails(self):
        game = Game()
        first_player = game.get_current_player()

        result = game.move(25, 25)

        assert result["success"] is False
        assert result["player"] is None
        assert game.get_current_player() == first_player
        assert game.get_cell(0, 0) is None

    def test_check_winner_horizontal(self):
        game = Game()

        for col in range(5):
            game.make_move(0, col, "X")

        assert game.get_winner() == "X"

    def test_check_winner_vertical(self):
        game = Game()

        for row in range(5):
            game.make_move(row, 0, "X")

        assert game.get_winner() == "X"

    def test_check_winner_diagonal(self):
        game = Game()

        for index in range(5):
            game.make_move(index, index, "X")

        assert game.get_winner() == "X"

    def test_check_no_winner(self):
        game = Game()

        assert game.get_winner() is None

    def test_is_board_full(self):
        game = Game(3)
        moves = [
            (0, 0, "X"),
            (0, 1, "O"),
            (0, 2, "X"),
            (1, 0, "O"),
            (1, 1, "X"),
            (1, 2, "O"),
            (2, 0, "O"),
            (2, 1, "X"),
            (2, 2, "O"),
        ]

        for row, col, player in moves:
            game.make_move(row, col, player)

        assert game.is_board_full() is True

    def test_reset_game(self):
        game = Game()
        game.move(0, 0)

        game.reset()

        assert game.get_cell(0, 0) is None
        assert game.get_board()[0][0] is None
        assert game.get_size() == 25
