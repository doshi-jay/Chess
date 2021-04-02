"""
Store chess board state.
Determine valid moves and keep a move log
"""
from pprint import pprint

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
            ["--", "--", "--", "--", "--", "--", "--", "--"],
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

        # Keeping track of kings for castling and moves resulting in check
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)

        self.check_mate = False
        self.state_mate = False

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

        # print(f"Making move at {move.start_row, move.start_col} to {move.end_row, move.end_col}")

        self.board[move.start_row][move.start_col] = self.EMPTY_SQ
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move # Switch turns between white and black

        # Updating king location if moves
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)

        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            # Making a queen with the same color
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"



    def undo_move(self):
        # Undo only if valid moves have been made
        if len(self.move_log) > 0:
            move_to_undo = self.move_log.pop()
            self.board[move_to_undo.start_row][move_to_undo.start_col] = move_to_undo.piece_moved
            self.board[move_to_undo.end_row][move_to_undo.end_col] = move_to_undo.piece_captured
            self.white_to_move = not self.white_to_move # Switch back turns

            # Undo king location if it was moved
            if move_to_undo.piece_moved == "wK":
                self.white_king_location = (move_to_undo.start_row, move_to_undo.start_col)

            elif move_to_undo.piece_moved == "bK":
                self.black_king_location = (move_to_undo.start_row, move_to_undo.start_col)

            self.check_mate = self.state_mate = False

    def in_check(self):
        """
        Determine if current player is in check
        :return:
        """
        if self.white_to_move:
            return self.square_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_under_attack(self.black_king_location[0], self.black_king_location[1])

    def square_under_attack(self, row, col):
        """
        Determine if enemy can attack square with row, col
        :param row:
        :param col:
        :return:
        """
        # Switching to opponent, to see all their possible moves
        self.white_to_move = not self.white_to_move

        opp_moves = self.get_all_possible_moves()

        # Switch turns back to maintain whose move it is
        self.white_to_move = not self.white_to_move

        for move in opp_moves:
            if (move.end_row, move.end_col) == (row, col):
                return True
        return False

    def get_valid_moves(self):
        """
        All valid moves considering checks
        :return:
        """
        moves = self.get_all_possible_moves()
        moves = list(set(moves))

        for i in range(len(moves)-1, -1, -1): # Removing elements from list, thus going backward
            self.make_move(moves[i])

            # On calling make move above, turns got swtiched.
            # We must undo that turn change because we are not actually making the move
            # we are only computing all valid moves.
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])

            self.white_to_move = not self.white_to_move
            self.undo_move()

        # print(f"Generating {len(moves)}")
        # self.show_move_per_piece(moves)

        # Checking for checkmate or statelate
        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.state_mate = True


        return moves

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

    def show_move_per_piece(self, moves):
        moves_per_piece = dict()
        for move in moves:
            if move.piece_moved in moves_per_piece:
                moves_per_piece[move.piece_moved].append(((move.start_row, move.start_col),
                                                          (move.end_row, move.end_col)))
            else:
                moves_per_piece[move.piece_moved] = [((move.start_row, move.start_col), (move.end_row, move.end_col))]

        pprint(moves_per_piece)
        return

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

            # TODO add pawn promotions

        return moves

    def get_rook_moves(self, row, col, moves):
        """
        Get all rook moves at row, col and add them to moves list
        :param row:
        :param col:
        :param moves:
        :return:
        """
        # row, col format to specify directions
        possible_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return moves + self.get_range_moves(possible_directions, row, col)

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
        return moves + self.get_range_moves(possible_directions, row, col)

    def get_range_moves(self, possible_directions, row, col):
        moves = []
        opp_color = "b" if self.white_to_move else "w"

        for i, j in possible_directions:
            direction_valid = True
            curr_row, curr_col = row, col

            while direction_valid:
                curr_row = curr_row + i
                curr_col = curr_col + j
                if self.check_move_validity(curr_row, curr_col):
                    move = Move((row, col), (curr_row, curr_col), self.board)
                    moves.append(move)

                    if self.board[curr_row][curr_col][0] == opp_color:
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
        self.is_pawn_promotion = False

        # Pawn promotion
        if (self.piece_moved == "wp" and self.end_row == 0) or (self.piece_moved == "bp" and self.end_row == 7):
            self.is_pawn_promotion = True

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

    def __hash__(self):
        return self.move_id

    def print_move(self):
        print(str(self.start_row) + str(self.start_col) + " -> " + str(self.end_row)+ str(self.end_col))