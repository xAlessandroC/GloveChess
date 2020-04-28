def getPossibleMoves(node, role):

    state = node.getState()

    # [[<Piece.W_ROOK: 2> <Piece.W_PAWN: 5> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.B_PAWN: 11>
    #   <Piece.B_ROOK: 8>]
    #  [<Piece.W_KNIGHT: 4> <Piece.W_PAWN: 5> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.B_PAWN: 11> <Piece.B_KNIGHT: 10>]
    #  [<Piece.W_BISHOP: 3> <Piece.W_PAWN: 5> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.B_PAWN: 11> <Piece.B_BISHOP: 9>]
    #  [<Piece.W_QUEEN: 1> <Piece.W_PAWN: 5> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.B_PAWN: 11> <Piece.B_QUEEN: 7>]
    #  [<Piece.W_KING: 0> <Piece.W_PAWN: 5> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.B_PAWN: 11>
    #   <Piece.B_KING: 6>]
    #  [<Piece.W_BISHOP: 3> <Piece.W_PAWN: 5> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.B_PAWN: 11> <Piece.B_BISHOP: 9>]
    #  [<Piece.W_KNIGHT: 4> <Piece.W_PAWN: 5> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.B_PAWN: 11> <Piece.B_KNIGHT: 10>]
    #  [<Piece.W_ROOK: 2> <Piece.W_PAWN: 5> <Piece.EMPTY: 12> <Piece.EMPTY: 12>
    #   <Piece.EMPTY: 12> <Piece.EMPTY: 12> <Piece.B_PAWN: 11>
    #   <Piece.B_ROOK: 8>]]

    if role == "WHITE":
        white_pieces = []
        for i in range(len(8)):
            for j in range(len(8)):
                if state[i][j].name.startsWith("W"):
                    white_pieces.append([i,j])

        

    if role == "BLACK":
        black_pieces = []
        for i in range(len(8)):
            for j in range(len(8)):
                if state[i][j].name.startsWith("B"):
                    black_pieces.append([i,j])
