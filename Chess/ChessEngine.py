"""
Store chess board state.
Determine valid moves and keep a move log
"""
class GameState():
    EMPTY = "--"
    def __init__(self):
        # Board is 8 x 8 2-D list
        # The first char of each piece represents the color: b => Black, w => White
        # The second char denotes the piece type
        # "--" denotes empty square
        # Starting from black at the top, [0, 0] represents a8
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = [] # Stores objects of class 'Move'

    def make_move(self, move):

        # If move starts from an empty piece, ignore it
        if move.piece_moved == self.EMPTY:
            return

        self.board[move.start_row][move.start_col] = self.EMPTY
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move # Switch turns between white and black


class Move():

    ranks_to_rows = { "1": 7, "2": 6, "3": 5, "4": 4,
                      "5": 3, "6": 2, "7": 1, "8": 0 }
    files_to_cols = { "a": 0, "b": 1, "c": 2, "d": 3,
                      "e": 4, "f": 5, "g": 6, "h": 7 }

    rows_to_ranks = {value: key for key, value in ranks_to_rows.items()}
    cols_to_files = {value: key for key, value in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        """

        :param start_sq: tuple coordinates
        :param end_sq: tuple coordinates
        :param board: needed understand which pieces are being captured
                      especially needed during undo moves
        """
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]


