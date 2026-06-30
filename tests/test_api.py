import json

import pytest

from modules.api import GameAPI


@pytest.fixture
def api():
    return GameAPI(size=8)


def play_until_win(api, target_positions, filler_positions):
    first_symbol = api.get_current_player()
    ti = fi = 0
    result = None

    while not api.is_game_over():
        current = api.get_current_player()

        if current == first_symbol:
            x, y = target_positions[ti]
            ti += 1
        else:
            x, y = filler_positions[fi]
            fi += 1

        result = api.move(x, y)

    return first_symbol, result


def test_default_size():
    api = GameAPI()
    assert api.get_size() == 25


def test_custom_size():
    api = GameAPI(size=10)
    assert api.get_size() == 10


def test_invalid_size_raises():
    with pytest.raises(ValueError):
        GameAPI(size=0)

    with pytest.raises(ValueError):
        GameAPI(size=-5)


def test_new_game_resets_board():
    api = GameAPI(size=5)
    api.move(0, 0)

    api.new_game()

    assert api.get_cell(0, 0) is None


def test_new_game_can_change_size():
    api = GameAPI(size=5)

    api.new_game(size=8)

    assert api.get_size() == 8


def test_reset_keeps_same_size():
    api = GameAPI(size=6)

    api.move(0, 0)
    api.reset()

    assert api.get_size() == 6
    assert api.get_cell(0, 0) is None


def test_str_delegates_to_board():
    api = GameAPI(size=3)

    assert str(api) == str(api.game.board)


def test_move_returns_expected_keys(api):
    result = api.move(0, 0)

    for key in (
        "success",
        "player",
        "winner",
        "is_full",
        "next_player",
        "game_over",
    ):
        assert key in result


def test_first_move_succeeds(api):
    result = api.move(0, 0)

    assert result["success"]
    assert result["player"] in ("X", "O")
    assert result["winner"] is None
    assert not result["is_full"]
    assert not result["game_over"]


def test_players_alternate(api):
    first = api.get_current_player()

    result1 = api.move(0, 0)

    assert result1["player"] == first

    second = api.get_current_player()

    assert first != second

    result2 = api.move(0, 1)

    assert result2["player"] == second


def test_move_out_of_bounds_fails(api):
    current = api.get_current_player()

    result = api.move(-1, 0)

    assert not result["success"]
    assert result["player"] is None
    assert api.get_current_player() == current

    result = api.move(api.get_size(), 0)

    assert not result["success"]


def test_move_on_occupied_cell_fails(api):
    api.move(2, 2)

    current = api.get_current_player()

    result = api.move(2, 2)

    assert not result["success"]
    assert result["player"] is None
    assert api.get_current_player() == current


def test_get_cell_and_board_reflect_moves(api):
    api.move(1, 1)

    symbol = api.get_cell(1, 1)

    assert symbol in ("X", "O")

    board = api.get_board()

    assert board[1][1] == symbol
    assert board[0][0] is None


@pytest.mark.parametrize(
    "target,filler",
    [
        (
            [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)],
            [(5, 0), (5, 1), (5, 2), (5, 3)],
        ),
        (
            [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],
            [(0, 5), (1, 5), (2, 5), (3, 5)],
        ),
        (
            [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)],
            [(0, 5), (1, 5), (2, 5), (3, 5)],
        ),
    ],
)
def test_wins(target, filler):
    api = GameAPI(size=10)

    first_symbol, result = play_until_win(
        api,
        target,
        filler,
    )

    assert result["winner"] == first_symbol
    assert result["game_over"]


def test_winner_persists():
    api = GameAPI(size=10)

    target = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)]
    filler = [(5, 0), (5, 1), (5, 2), (5, 3)]

    first_symbol, _ = play_until_win(
        api,
        target,
        filler,
    )

    assert api.get_winner() == first_symbol
    assert api.is_game_over()


def test_draw():
    api = GameAPI(size=4)

    result = None

    for x in range(4):
        for y in range(4):
            result = api.move(x, y)

    assert result["is_full"]
    assert result["winner"] is None
    assert result["game_over"]

    assert api.is_full()
    assert api.get_winner() is None
    assert api.is_game_over()


def test_save_and_load_game_round_trip(tmp_path):
    api = GameAPI(size=3)
    api.move(0, 0)
    api.move(0, 1)

    save_path = tmp_path / "savegame.json"
    assert api.save_game(save_path) is True

    with save_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    assert data["board"][0][0] in {"X", "O", " "}
    assert data["board"][0][1] in {"X", "O", " "}

    restored = GameAPI(size=3)
    assert restored.load_game(save_path) is True
    assert restored.get_cell(0, 0) == api.get_cell(0, 0)
    assert restored.get_cell(0, 1) == api.get_cell(0, 1)
    assert restored.get_current_player() == api.get_current_player()