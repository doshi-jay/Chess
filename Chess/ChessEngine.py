"""
Store chess board state.
Determine valid moves and keep a move log
"""
class GameState():
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
        self.move_log = []
