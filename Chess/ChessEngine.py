"""
This class stores information about the current state of a chess game. It will also determine the valid moves at the
current state and keep a move log.
"""
from ChessMove import Move


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
        self.checkmate = False
        self.stalemate = False

    # Castling, promotion and en passant not yet implemented
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.piece_moved == 'wK':
            self.white_king_loc = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.black_king_loc = (move.end_row, move.end_col)

    def undo_move(self):
        if self.move_log:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == 'wK':
                self.white_king_loc = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.black_king_loc = (move.start_row, move.start_col)

    def get_valid_moves(self):
        moves = self.get_all_moves()
        s = ""
        for move in moves:
            s += (str(move) + ", ")
        print("All possible moves: " + s)
        for m in moves[::-1]:
            self.make_move(m)
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(m)
            self.white_to_move = not self.white_to_move
            self.undo_move()
        s = ""
        for move in moves:
            s += (str(move) + ", ")
        print("All valid moves: " + s)
        if not moves:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        return moves

    def in_check(self):
        if self.white_to_move:
            return self.is_under_attack(self.white_king_loc[0], self.white_king_loc[1])
        else:
            return self.is_under_attack(self.black_king_loc[0], self.black_king_loc[1])

    def is_under_attack(self, r, c):
        self.white_to_move = not self.white_to_move
        enemy_moves = self.get_all_moves()
        self.white_to_move = not self.white_to_move
        for m in enemy_moves:
            if m.end_row == r and m.end_col == c:
                return True
        return False

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
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for step in range(1, 8):
                end_row = r + d[0] * step
                end_col = c + d[1] * step
                if end_row in range(0, 8) and end_col in range(0, 8):
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break

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
        enemy_color = 'b' if self.white_to_move else 'w'
        for d in directions:
            for step in range(1, 8):
                end_row = r + d[0] * step
                end_col = c + d[1] * step
                if end_row in range(0, 8) and end_col in range(0, 8):
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else:
                        break

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
