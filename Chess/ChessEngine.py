"""
This class stores information about the current state of a chess game. It will also determine the valid moves at the
current state and keep a move log.
"""


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_mappings = {'P': self.get_pawn_moves, 'R': self.get_rook_moves, 'N': self.get_knight_moves,
                              'B': self.get_bishop_moves, 'K': self.get_king_moves, 'Q': self.get_queen_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_loc = (7, 4)
        self.black_king_loc = (0, 4)

    # Castling, promotion and en passant not yet implemented
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == 'wk':
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == 'bk':
            self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        if self.move_log:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == 'wk':
                self.white_king_loc = (move.start_row, move.start_col)
            elif move.piece_moved == 'bk':
                self.black_king_loc = (move.start_row, move.start_col)

    def get_valid_moves(self):
        return self.get_all_moves()

    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                if (color == 'w' and self.white_to_move) or (color == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    self.move_mappings[piece](r, c, moves)
        return moves

    def get_pawn_moves(self, r, c, moves):
        enemy_color = 'b' if self.white_to_move else 'w'
        if self.white_to_move:
            if self.board[r - 1][c] == '--':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == '--':
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c > 0:
                if self.board[r - 1][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c < 7:
                if self.board[r - 1][c + 1][0] == enemy_color:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
        else:
            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c > 0:
                if self.board[r + 1][c - 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c < 7:
                if self.board[r + 1][c + 1][0] == enemy_color:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
        # Add pawn promotions later

    def get_rook_moves(self, r, c, moves):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            for step in range(1, 8):
                end_row = r + d[0] * step
                end_col = c + d[1] * step
                if end_row in range(0, 8) and end_col in range(0, 8):
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_knight_moves(self, r, c, moves):
        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if end_row in range(0, 8) and end_col in range(0, 8):
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_bishop_moves(self, r, c, moves):
        directions = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            for step in range(1, 8):
                end_row = r + d[0] * step
                end_col = c + d[1] * step
                if end_row in range(0, 8) and end_col in range(0, 8):
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] != ally_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_king_moves(self, r, c, moves):
        directions = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
        ally_color = 'w' if self.white_to_move else 'b'
        for d in directions:
            end_row = r + d[0]
            end_col = c + d[1]
            if end_row in range(0, 8) and end_col in range(0, 8):
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

    def get_queen_moves(self, r, c, moves):
        self.get_rook_moves(r, c, moves)
        self.get_bishop_moves(r, c, moves)


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
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

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
