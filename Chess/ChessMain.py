"""
View chess board state and take user input
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512 # Chess board is square
DIMENSION = 8 # Since chess board is 8x8
SQ_SIZE = WIDTH // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = dict()


def load_images():
    """
    Loading images is slow, cannot load at every frame because game might lag
    Load each image once to optimize
    This is called exactly once. It also allow flexibility in using user selected images
    :return: None
    """
    print("[+] UPDATE - Begin loading images")

    colors = ["w", "b"]
    piece_types = ["p", "R", "N", "B", "K", "Q"]
    for color in colors:
        for type in piece_types:
            piece = color + type
            IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece  + ".png"), (SQ_SIZE, SQ_SIZE))

    print("[+] UPDATE - Images loaded")


def main():
    """
    Main driver of code
    Handles user inputs and updating graphics
    :return:
    """
    p.init() # Initializing pygame object
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    valid_moves = gs.get_valid_moves()

    # Flag to control the number of times get valid moves is called
    # Only if the user makes a valid move, it is called
    move_made = False

    load_images()
    game_running = True

    sq_selected = tuple() # (row, col), keeps track of user click
    player_clicks = list() # 2 tuples in the list, [(row, col), (row, col)]

    while game_running:

        for e in p.event.get():
            if e.type == p.QUIT:
                game_running = False

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undo_move()
                    move_made = True # On undo we need to generate all valid moves again

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # Gets (col, row) location of mouse click
                row = location[1] // SQ_SIZE
                col = location[0] // SQ_SIZE

                # If user clicks on the same square again, i.e. as source and destination,
                # then we deselect it and reset player clicks
                if sq_selected == (row, col):
                    sq_selected = tuple()
                    player_clicks = list()
                else:
                    if not (len(player_clicks) == 0 and gs.board[row][col] == gs.EMPTY_SQ):
                        sq_selected = (row, col)
                        player_clicks.append(sq_selected) # Append both first and second clicks

                # After second click only
                if len(player_clicks) == 2:
                    move = ChessEngine.Move(start_sq=player_clicks[0], end_sq=player_clicks[1], board=gs.board)
                    # move.print_move()
                    for i in range(len(valid_moves)):

                        if move == valid_moves[i]:
                            gs.make_move(valid_moves[i])
                            move_made = True

                            player_clicks = list() # Resetting to restart the 2 click move logic
                            sq_selected = tuple()
                    if not move_made:
                        player_clicks = [sq_selected]

        if move_made:
            valid_moves = gs.get_valid_moves()
            move_made = False

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_board(screen):
    """
    Draw the squares on the board
    Note: Top left square on chess board is always white, regardless of which color you play!
    :param screen:
    :return:
    """
    colors = [p.Color("white"), p.Color("dark gray")]

    for row in range(DIMENSION):
        for col in range(DIMENSION):
            # For all light squares: row + col => even
            #         dark squares:  row + col => odd
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draw pieces on the chess board using the board argument
    :param screen:
    :param board:
    :return:
    """
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board[row][col]
            # Check for empty square
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))



def draw_game_state(screen, gs):
    """
    Handles all graphics within current game state
    :param screen:
    :param gs:
    :return:
    """
    draw_board(screen)
    draw_pieces(screen, gs.board)


if __name__ == "__main__":
    main()
