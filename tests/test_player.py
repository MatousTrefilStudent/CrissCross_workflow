# tests/test_player.py

import pytest
from modules.player import Player
from modules.board import Board


def test_player_initialization():
    player = Player("Alice", "X")

    assert player.name == "Alice"
    assert player.symbol == "X"



def test_make_move_invalid_board():
    player = Player("Alice", "X")

    with pytest.raises(TypeError):
        player.make_move("not a board", 0, 0)


def test_make_move_invalid_x():
    player = Player("Alice", "X")
    board = Board(5)

    with pytest.raises(TypeError):
        player.make_move(board, "0", 0)


def test_make_move_invalid_y():
    player = Player("Alice", "X")
    board = Board(5)

    with pytest.raises(TypeError):
        player.make_move(board, 0, "0")
