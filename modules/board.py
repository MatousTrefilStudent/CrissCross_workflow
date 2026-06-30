class Board:
    def __init__(self, size=25):
        self.size = size
        self.board = [[None for _ in range(size)] for _ in range(size)]

    def __str__(self):
        board_str = ""
        for x in self.board:
            for y in x:
                if y is None:
                    board_str += " "
                elif y == True:
                    board_str += "X"
                elif y == False:
                    board_str += "O"
                
                board_str += "|"
            board_str += "\n"
        return board_str
    
    def make_move(self, x, y, player):
        if self.board[x][y] is None:
            self.board[x][y] = player
            return True
        return False