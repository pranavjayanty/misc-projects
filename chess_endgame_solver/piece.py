from square import Square
from board import Board

class Piece:
    def __init__(self, type: str, pos: Square, clr: str) -> None:
        self.type = type
        self.pos = pos
        self.clr = clr
    
    def get_moves(self, board: Board):
        pass
