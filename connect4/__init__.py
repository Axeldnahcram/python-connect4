"""
A pure Python chess library with move generation and validation, Polyglot
opening book probing, PGN reading and writing, Gaviota tablebase probing,
Syzygy tablebase probing and XBoard/UCI engine communication.
"""

__author__ = "Axel Marchand"

__email__ = "axel-marchand@hotmail.fr"

__version__ = "0.0.1"

import pygame
import numpy as np

#Color = bool
COLORS = [WHITE, BLACK] = [True, False]
#COLOR_NAMES = ["black", "white"]


class Piece:
    """A piece with type and color."""

    def __init__(self, color) -> None:
        self.color = color

    def symbol(self) -> str:
        """
        Gets the symbol ``R``, ``B`` if the color is white or black
        """
        if self.color:
            return "R"
        else:
            return "B"


    def __hash__(self) -> int:
        return hash(self.color)

    def __repr__(self) -> str:
        return f"Piece.from_symbol({self.symbol()!r})"

    def __str__(self) -> str:
        return self.symbol()


    def __eq__(self, other: object) -> bool:
        if isinstance(other, Piece):
            return (self.color) == (other.color)
        else:
            return NotImplemented


class Board:
    """A board with pieces"""
    dict_piece = {WHITE:1, BLACK:2}

    def __init__(self, size=6, board=None):
        self.size = size
        self.squares = np.zeros((self.size, self.size))
        if board is not None:
            self.squares = board
        #### Les blancs commencent
        self.turn = WHITE
        self.piece = self.dict_piece[self.turn]

    def __repr__(self):
        return (f"""{self.squares}""")

    def play(self, column):
        """Play a coin in the column going from 0 to size - 1"""
        height = self.check_height(column)
        if height is not False:
            self.squares[height, column] = self.piece
            self.turn = not self.turn
            self.piece = self.dict_piece[self.turn]

    def check_height(self, column):
        col = self.squares[:, column]
        nb_available = np.where((col == 0) == True)[-1]
        if len(nb_available)>0:
            height = nb_available[-1]
        else:
            height = False
        return height

    def get_moves(self):
        list_col_avl = []
        for i in range(self.size):
            cur_height = self.check_height(i)
            if cur_height is not False:
                list_col_avl.append(i)
        return list_col_avl

    def print_board(self):
        print(self.squares)

    def check_win(self, player):
        for c in range(self.size - 3):
            for r in range(self.size):
                if self.squares[r][c] == player and \
                        self.squares[r][c + 1] == player and \
                        self.squares[r][c + 2] == player and \
                        self.squares[r][c + 3] == player:
                    return True

            # Check vertical locations for win
        for c in range(self.size - 3):
            for r in range(self.size):
                if self.squares[r][c] == player and \
                        self.squares[r+1][c] == player and \
                        self.squares[r+2][c] == player and \
                        self.squares[r+3][c] == player:
                    return True

            # Check positively sloped diaganals
        for c in range(self.size - 3):
            for r in range(self.size-3):
                if self.squares[r][c] == player and \
                        self.squares[r+1][c+1] == player and \
                        self.squares[r+2][c+2] == player and \
                        self.squares[r+3][c+3] == player:
                    return True

            # Check negatively sloped diaganals
        for c in range(self.size - 3):
            for r in range(3, self.size):
                if self.squares[r][c] == player and \
                        self.squares[r-1][c+1] == player and \
                        self.squares[r-2][c+2] == player and \
                        self.squares[r-3][c+3] == player:
                    return True
        return False

    def no_move(self):
        list_move = self.get_moves()
        if len(list_move)>0:
            return False
        else:
            return True

    def result(self):
        player_w = self.check_win(1)
        player_b = self.check_win(2)
        if player_w:
            return '1-0'
        elif player_b:
            return '0-1'
        elif self.no_move():
            return '1/2-1/2'
        else:
            return '*'

    def push(self, mov):
        self.past_squares = np.copy(self.squares)
        self.play(mov)

    def pop(self):
        self.squares = self.past_squares


    # def draw_board(self):
    #     pygame.init()
    #
    #     SQUARESIZE = 100
    #
    #     width = self.size * SQUARESIZE
    #     height = (self.size + 1) * SQUARESIZE
    #
    #     size = (width, height)
    #
    #     RADIUS = int(SQUARESIZE / 2 - 5)
    #
    #     screen = pygame.display.set_mode(size)
    #     myfont = pygame.font.SysFont("monospace", 75)
    #
    #     for c in range(self.size):
    #         for r in range(self.size):
    #             pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
    #             pygame.draw.circle(screen, BLACK, (
    #             int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    #
    #     for c in range(self.size):
    #         for r in range(self.size):
    #             if self.squares[r][c] == 1:
    #                 pygame.draw.circle(screen, RED, (
    #                 int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    #             elif self.squares[r][c] == 2:
    #                 pygame.draw.circle(screen, YELLOW, (
    #                 int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    #     pygame.display.update()




