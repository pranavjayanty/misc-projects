from square import Square
from piece import Piece
from typing import Dict, List

class Board:
    def __init__(self):
        """Initialize an empty board with a dictionary mapping squares to pieces."""
        self.pieces: Dict[Square, Piece] = {}

    def add_piece(self, piece: Piece) -> None:
        """Add a piece to the board at its position."""
        self.pieces[piece.pos] = piece

    def move_piece(self, curr_pos: Square, new_pos: Square) -> None:
        """Move a piece from curr_pos to new_pos, updating its position."""
        if curr_pos not in self.pieces:
            raise ValueError(f"No piece at {curr_pos}")
        piece = self.pieces[curr_pos]
        del self.pieces[curr_pos]
        piece.pos = new_pos
        self.pieces[new_pos] = piece

    def get_piece(self, square: Square) -> Piece | None:
        """Return the piece at a given square, or None if empty."""
        return self.pieces.get(square)

    def get_king(self, color: str) -> Piece:
        """Return the king of the specified color."""
        for piece in self.pieces.values():
            if piece.type == "king" and piece.clr == color:
                return piece
        raise ValueError(f"No {color} king found on the board")

    def is_in_check(self, clr: str) -> bool:
        """Check if the king of the given color is in check."""
        king = self.get_king(clr)
        king_pos = king.pos
        for piece in self.pieces.values():
            if piece.clr != clr:  # Opponent's pieces
                if piece.type == "king" and piece.pos.is_adjacent_to(king_pos):
                    return True
                elif piece.type == "queen":
                    # Check if queen attacks king without being blocked
                    if self._is_square_attacked_by_queen(king_pos, piece.pos):
                        return True
        return False

    def _is_square_attacked_by_queen(self, target: Square, q_pos: Square) -> bool:
        """Check if the target square is attacked by the queen at q_pos."""
        if target.row != q_pos.row and target.col != q_pos.col and \
           abs(target.row - q_pos.row) != abs(target.col - q_pos.col):
            return False  # Not on same row, col, or diagonal
        # Determine direction
        if target.row == q_pos.row:
            step = 1 if target.col > q_pos.col else -1
            for c in range(q_pos.col + step, target.col, step):
                if Square(q_pos.row, c) in self.pieces:
                    return False
            return True
        elif target.col == q_pos.col:
            step = 1 if target.row > q_pos.row else -1
            for r in range(q_pos.row + step, target.row, step):
                if Square(r, q_pos.col) in self.pieces:
                    return False
            return True
        else:  # Diagonal
            dr = 1 if target.row > q_pos.row else -1
            dc = 1 if target.col > q_pos.col else -1
            r, c = q_pos.row + dr, q_pos.col + dc
            while (r, c) != (target.row, target.col):
                if Square(r, c) in self.pieces:
                    return False
                r += dr
                c += dc
            return True

    def is_checkmate(self, clr: str) -> bool:
        """Check if the given color is in checkmate."""
        if not self.is_in_check(clr):
            return False
        king = self.get_king(clr)
        # Try all possible moves for this color
        for piece in self.pieces.values():
            if piece.clr == clr:
                moves = piece.get_moves(self)
                curr_pos = piece.pos
                for new_pos in moves:
                    # Simulate the move
                    self.move_piece(curr_pos, new_pos)
                    if not self.is_in_check(clr):
                        # Undo the move
                        self.move_piece(new_pos, curr_pos)
                        return False
                    self.move_piece(new_pos, curr_pos)
        return True

    def get_legal_moves(self, clr: str) -> List[tuple[Square, Square]]:
        """Get all legal moves for the given color."""
        moves = []
        original_pieces = self.pieces.copy()
        for piece in original_pieces.values():
            if piece.clr == clr:
                curr_pos = piece.pos
                for new_pos in piece.get_moves(self):
                    self.move_piece(curr_pos, new_pos)
                    if not self.is_in_check(clr):
                        moves.append((curr_pos, new_pos))
                    self.pieces = original_pieces.copy()  # Reset board
        return moves