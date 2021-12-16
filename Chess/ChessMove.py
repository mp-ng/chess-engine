"""
This class stores information about a chess move and determines the corresponding chess notation.
"""


class Move:
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                     '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                     'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row, self.start_col = start_sq[0], start_sq[1]
        self.end_row, self.end_col = end_sq[0], end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        # A unique ID in the range [0, 7777]
        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        return isinstance(other, Move) and self.move_ID == other.move_ID

    def __str__(self):
        return self.get_chess_notation()

    def get_chess_notation(self):
        # Check, checkmate, castling and promotion not yet implemented
        # Ambiguity is not be avoided for simplicity
        name_moved = self.piece_moved[1]
        name_captured = self.piece_captured[1]
        if name_moved == 'P':
            if name_captured == '-':
                return self.get_rank_file(self.end_row, self.end_col)
            else:
                return self.cols_to_files[self.start_col] + 'x' + self.get_rank_file(self.end_row, self.end_col)
        else:
            if name_captured == '-':
                return name_moved + self.get_rank_file(self.end_row, self.end_col)
            else:
                return name_moved + 'x' + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]