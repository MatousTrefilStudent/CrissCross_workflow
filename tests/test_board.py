import pytest
from modules.board import Board


# ---------------------------------------------------------------------
# Tests that should PASS - covering current, working behavior
# ---------------------------------------------------------------------

def test_board_default_size():
    board = Board()
    assert board.size == 25
    assert len(board.board) == 25
    assert len(board.board[0]) == 25


def test_board_custom_size():
    board = Board(5)
    assert board.size == 5
    assert len(board.board) == 5
    assert len(board.board[0]) == 5


def test_board_starts_empty():
    board = Board(5)
    for row in board.board:
        for cell in row:
            assert cell is None


def test_make_move_success_returns_true():
    board = Board(5)
    result = board.make_move(0, 0, True)
    assert result is True
    assert board.board[0][0] is True


def test_make_move_stores_player_value():
    board = Board(5)
    board.make_move(2, 3, False)
    assert board.board[2][3] is False


def test_make_move_on_occupied_cell_returns_false():
    board = Board(5)
    board.make_move(1, 1, True)
    result = board.make_move(1, 1, False)
    assert result is False
    # original value should remain unchanged
    assert board.board[1][1] is True


def test_str_empty_board_uses_spaces():
    board = Board(2)
    output = str(board)
    assert output == " | |\n | |\n"


def test_str_shows_x_for_true():
    board = Board(2)
    board.make_move(0, 0, True)
    output = str(board)
    assert output.startswith("X|")


def test_str_shows_o_for_false():
    board = Board(2)
    board.make_move(0, 0, False)
    output = str(board)
    assert output.startswith("O|")


def test_str_returns_string_type():
    board = Board(3)
    assert isinstance(str(board), str)


def test_make_move_out_of_bounds_should_be_rejected():
    """There is no bounds checking, so this raises IndexError instead
    of returning False as a well-behaved API should."""
    board = Board(5)
    result = board.make_move(10, 10, True)
    assert result is False


def test_make_move_negative_coordinates_should_be_rejected():
    """Negative indices wrap around in Python lists instead of being
    rejected, so this silently succeeds on the wrong cell."""
    board = Board(5)
    result = board.make_move(-1, -1, True)
    assert result is False


def test_make_move_rejects_invalid_player_value():
    """The class does not validate that `player` is a boolean, so
    arbitrary values are accepted and break the X/O semantics."""
    board = Board(5)
    with pytest.raises(ValueError):
        board.make_move(0, 0, "not_a_boolean")


def test_str_uses_dot_for_empty_cell_not_space():
    """Asserts a different empty-cell symbol ('.') than what the
    implementation actually outputs (' '), so it fails by design."""
    board = Board(2)
    output = str(board)
    assert "." in output


def test_board_size_must_be_positive():
    """The constructor does not validate `size`, so a non-positive
    size is silently accepted instead of raising an error."""
    with pytest.raises(ValueError):
        Board(0)