from .board import Board

class Player:
    def __init__(self, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
    
    def make_move(self, board, x: int, y: int):
        if not isinstance(board, Board):
            raise TypeError("board must be an instance of Board")
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be integers")

        result = board.make_move(x, y)
        if result is not True:
            raise ValueError("board.make_move() did not return True (you can´t place your symbol there)")
        return result

    def test(self):
        print("something")