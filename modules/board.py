class Board:
    def __init__(self, size=25):
        if size <= 0:
            raise ValueError("size must be positive")
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]


    def __str__(self):
        board_str = ""
        for x in self.board:
            for y in x:
                if y is None:
                    board_str += "."
                elif y == True:
                    board_str += "X"
                elif y == False:
                    board_str += "O"
                
                board_str += "|"
            board_str += "\n"
        return board_str
    
    def make_move(self, x, y, player):
        """Place a move for player at (x, y).

        x and y must be within bounds [0, size-1].
        player must be a boolean: True for X, False for O.
        Returns True if the move was placed, False otherwise.
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False
        if player not in (True, False):
            return False
        if self.board[x][y] is None:
            self.board[x][y] = player
            return True
        return False