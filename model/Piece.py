from enum import Enum

class Piece(Enum):
    W_KING = 0; W_QUEEN = 1; W_ROOK = 2; W_BISHOP = 3; W_KNIGHT = 4; W_PAWN = 5
    B_KING = 6; B_QUEEN = 7; B_ROOK = 8; B_BISHOP = 9; B_KNIGHT = 10; B_PAWN = 11
    EMPTY = 12
