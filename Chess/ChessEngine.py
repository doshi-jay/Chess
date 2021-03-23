"""
Store chess board state.
Determine valid moves and keep a move log
"""
class GameState():
    EMPTY_SQ = "--"
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
            ["--", "--", "--", "wR", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.move_functions = dict()
        self.move_functions['p'] = self.get_pawn_moves
        self.move_functions['R'] = self.get_rook_moves
        self.move_functions['N'] = self.get_knight_moves
        self.move_functions['B'] = self.get_bishop_moves
        self.move_functions['Q'] = self.get_queen_moves
        self.move_functions['K'] = self.get_king_moves

        self.white_to_move = True
        self.move_log = [] # Stores objects of class 'Move'

    def make_move(self, move):
        """
        Takes move as param, executes it.
        Does not work with pawn promotion, en-passant and castling
        :param move:
        :return:
        """
        # If move starts from an empty piece, ignore it
        if move.piece_moved == self.EMPTY_SQ:
            return

        self.board[move.start_row][move.start_col] = self.EMPTY_SQ
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move # Switch turns between white and black

    def undo_move(self):
        # Undo only if valid moves have been made
        if len(self.move_log) > 0:
            move_to_undo = self.move_log.pop()
            self.board[move_to_undo.start_row][move_to_undo.start_col] = move_to_undo.piece_moved
            self.board[move_to_undo.end_row][move_to_undo.end_col] = move_to_undo.piece_captured
            self.white_to_move = not self.white_to_move # Switch back turns

    def get_valid_moves(self):
        """
        All valid moves considering checks
        :return:
        """
        return self.get_all_possible_moves()

    def get_all_possible_moves(self):
        """
        All valid moves without considering checks
        :return:
        """
        moves = list()
        # Sample moves.
        # TODO AI Will generate this later
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0] # Either 'b' or 'w', thereby denoting whose turn
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[row][col][1]
                    # if piece == "K":
                    #     moves = self.get_king_moves(row, col, moves)
                    #     # elif piece == "R":
                    #     #     self.get_rook_moves(row, col, moves)
                    #     print("Piece: ", piece)
                    #     print(row, col)
                    moves = self.move_functions[piece](row, col, moves)

        return moves

    def check_move_validity(self, end_row, end_col):
        """
        Returns: true iff, the end row and end col are within bounds and the end
                square is either empty or has an opp colored piece
        :param end_row:
        :param end_col:
        :param opp_color:
        """
        opp_color = "b" if self.white_to_move else "w"
        return end_row < len(self.board) and end_row >= 0 and end_col < len(self.board[0]) and end_col >= 0 \
               and (self.board[end_row][end_col][0] == opp_color or self.board[end_row][end_col] == self.EMPTY_SQ)


    def get_pawn_moves(self, row, col, moves):
        """
        Get all pawn moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """
        # White pawn starts on row 6
        # Also, at row 6 it can move 2 squares forward
        # print(self.white_to_move)
        if self.white_to_move:
            # row - 1 => moving up the board on same file
            if self.board[row-1][col] == self.EMPTY_SQ: # 1 square pawn advance
                move = Move((row, col), (row-1, col), self.board)
                moves.append(move)

                if row == 6 and self.board[row-2][col] == self.EMPTY_SQ:
                    move = Move((row, col), (row-2, col), self.board)
                    moves.append(move)

            # - All capture moves, they need a black piece on the diagonally forward square
            # Captures to left
            if col - 1 >= 0 :
                if self.board[row-1][col-1][0] == "b":
                    move = Move((row, col), (row-1, col-1), self.board)
                    moves.append(move)

            # Captures to right
            if col + 1 < len(self.board[row]):
                if self.board[row-1][col+1][0] == "b":
                    move = Move((row, col), (row-1, col+1), self.board)
                    moves.append(move)

        # Black pawm moves, same logic, they just move from top -> bottom
        else:
            # - Moves without captures
            if self.board[row+1][col] == self.EMPTY_SQ:
                move = Move((row, col), (row+1, col), self.board)
                moves.append(move)

                if row == 1 and self.board[row+2][col] == self.EMPTY_SQ:
                    move = Move((row, col), (row+2, col), self.board)
                    moves.append(move)

            # - All capture moves, they need a white piece on the diagonally downward square
            # Captures to left
            if col - 1 >= 0:
                if self.board[row+1][col - 1][0] == "w":
                    move = Move((row, col), (row+1, col-1), self.board)
                    moves.append(move)

            # Captures to right
            if col + 1 < len(self.board[row]):
                if self.board[row+1][col + 1][0] == "w":
                    move = Move((row, col), (row+1, col+1), self.board)
                    moves.append(move)

        return moves


    def get_rook_moves(self, row, col, moves):
        """
        Get all rook moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """
        possible_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        moves += self.get_range_moves(possible_directions, row, col)
        return moves

    def get_knight_moves(self, row, col, moves):
        """
        Get all rook moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """
        possible_knight_moves = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, 2), (1, 2), (-1, -2), (1, -2)]

        for (i, j) in possible_knight_moves:
            k_row, k_col = row + i, col + j
            if self.check_move_validity(k_row, k_col):
                move = Move((row, col), (k_row, k_col), self.board)
                moves.append(move)

        return moves

    def get_bishop_moves(self, row, col, moves):
        """
        Get all rook moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """
        possible_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        moves += self.get_range_moves(possible_directions, row, col )
        return moves

    def get_range_moves(self, possible_directions, row, col):
        moves = []

        for i, j in possible_directions:
            direction_valid = True
            curr_row, curr_col = row, col

            while direction_valid:
                curr_row = curr_row + i
                curr_col = curr_col + j
                if self.check_move_validity(curr_row, curr_col):
                    move = Move((row, col), (curr_row, curr_col), self.board)
                    moves.append(move)
                    if (self.board[curr_row][curr_col][0] == "w" and not self.white_to_move) or \
                            (self.board[curr_row][curr_col][0] == "b" and self.white_to_move):
                        direction_valid = False
                else:
                    direction_valid = False

        return moves

    def get_queen_moves(self, row, col, moves):
        """
        Get all rook moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """
        return self.get_rook_moves(row, col, moves) + self.get_bishop_moves(row, col, moves)

    def get_king_moves(self, row, col, moves):
        """
        Get all rook moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """

        possible_king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

        for (i, j) in possible_king_moves:
            k_row, k_col = row + i, col + j
            if self.check_move_validity(k_row, k_col):
                move = Move((row, col), (k_row, k_col), self.board)
                moves.append(move)

        return moves



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
        self.move_id = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        # print(self.move_id)


    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]

    def __eq__(self, other):
        """
        Overriding equals to compare moves
        :param other:
        :return:
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id

    def print_move(self):
        print(str(self.start_row) + str(self.start_col) + " -> " + str(self.end_row)+ str(self.end_col))