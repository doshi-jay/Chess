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

    print(gs.board)

    load_images()

    game_running = True

    while game_running:
        for e in p.event.get():
            if e.type == p.QUIT:
                game_running = False

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
