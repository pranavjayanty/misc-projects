class Square:
    def __init__(self, row: int, col: int) -> None:
        """Initialize a square with row and column coordinates."""
        if not (0 <= row < 8 and 0 <= col < 8):
            raise ValueError("Square coordinates must be between 0 and 7")
        self.row = row
        self.col = col

    def __eq__(self, other) -> bool:
        """Check if two squares are equal based on position."""
        if not isinstance(other, Square):
            return False
        return self.row == other.row and self.col == other.col

    def __hash__(self) -> int:
        """Make Square hashable for use as a dictionary key."""
        return hash((self.row, self.col))

    def __str__(self) -> str:
        """Return chess notation (e.g., 'e4') for the square."""
        files = 'abcdefgh'
        ranks = '87654321'
        return f"{files[self.col]}{ranks[self.row]}"

    def is_adjacent_to(self, other: 'Square') -> bool:
        """Check if this square is adjacent to another (including diagonals)."""
        dr = abs(self.row - other.row)
        dc = abs(self.col - other.col)
        return max(dr, dc) == 1 and (dr != 0 or dc != 0)
