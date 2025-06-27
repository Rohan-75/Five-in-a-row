# Importing Python modules
import numpy as np
import pygame
import math
import random
import sys

class game:
    
    def __init__(self, board_size):
        self.BLUE=(0,100,255)
        self.BLACK=(0,0,0)
        self.RED=(200, 0, 0)
        self.YELLOW=(255,255,0)
        # Declaring global variables
        self.TARGET = 5  # minimum of dots that should be in a row to game to finish
        self.ROW_COUNTS, self.COLUMN_COUNTS = board_size  # number of Rows and Columns in a board

        self.PLAYER = 0      # Player's turn
        self.AI = 1          # AI's turn

        self.PLAYER_PIECE = 1    # Indicating player's piece
        self.AI_PIECE = 2        # Indicating AI's piece

        self.EMPTY = 0   # Indicating empty spots

        self.WINDOW_LENGTH = 5   # Indicating the length of list or window to be evaluated

        self.game_over = False 
        self.turn = 0  # It's player1 turn if variable = 0 otherwise it's player2 turn, variable remains 0 or 1 only

        pygame.init()
        self.SQUARESIZE = int(50)
        self.RADIUS = int(self.SQUARESIZE/2 - 2) # 45
        self.width = self.COLUMN_COUNTS * self.SQUARESIZE
        self.height = (self.ROW_COUNTS + 1) * self.SQUARESIZE
        size = (self.width, self.height)

        self.screen = pygame.display.set_mode(size)

    """
    Creating Board using matrix with initial values 0.
    """
    def create_board(self):
        board = np.zeros((self.ROW_COUNTS, self.COLUMN_COUNTS))
        return board

    def drop_piece(self, board, row, col, piece):
        board[row][col] = piece

    """
    Finding first open position i.e. 0 in this case, in the particular column col, and replacing it with 1 or 2
    """
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNTS):
            if board[r, col].any() == self.EMPTY:   # bug fix .any() used
                return r

    """
    Checking input from user is valid or not
    """
    def is_valid_location(self, board, col):
        return board[self.ROW_COUNTS - 1, col].any() == self.EMPTY  # bug fix .any() used

    """
    This function is called in order to print the board
    """
    def print_board(self, board):
        print(np.flip(board, 0))
        print("************************************")
        print()

    """
    Everytime player 1 or 2 make their move this function checks whether winning condition is met or not,
    if condition is fulfilled, loops end there.
    """
    def winning_move(self, board, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNTS - self.TARGET + 1):
            for r in range(self.ROW_COUNTS):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece and board[r][c+4] == piece:
                    return True
        # Check vertical locations for win
        for r in range(self.ROW_COUNTS - self.TARGET + 1):
            for c in range(self.COLUMN_COUNTS):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece and board[r+4][c] == piece:
                    return True
        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNTS - self.TARGET + 1):
            for r in range(self.ROW_COUNTS - self.TARGET + 1):
                if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece and board[r+4][c+4] == piece:
                    return True
        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNTS - self.TARGET + 1):
            for r in range(self.TARGET - 1, self.ROW_COUNTS):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece and board[r-4][c+4] == piece:
                    return True

    def is_draw(self,board):
        for c in range(self.COLUMN_COUNTS):
            for r in range(self.ROW_COUNTS):
                if board[r][c] == 0:
                    return False
        return True;

    def draw_board(self, board):
        for c in range(self.COLUMN_COUNTS):
            for r in range(self.ROW_COUNTS):
                pygame.draw.rect(self.screen, self.BLUE, (c*self.SQUARESIZE, (r*self.SQUARESIZE)+self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, self.BLACK, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), int((r*self.SQUARESIZE)+(self.SQUARESIZE*1.5))), self.RADIUS)
                
        for c in range(self.COLUMN_COUNTS):
            for r in range(self.ROW_COUNTS):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.YELLOW, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int((r*self.SQUARESIZE)+(self.SQUARESIZE*0.5))), self.RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.RED, (int(c*self.SQUARESIZE+self.SQUARESIZE/2), self.height-int((r*self.SQUARESIZE)+(self.SQUARESIZE*0.5))), self.RADIUS)
        pygame.display.update()


    def get_valid_locations(self, board):
        valid_locations = []
        for col in range(self.COLUMN_COUNTS):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations
    
    def isTerminalNode(self, board):
        return self.winning_move(board, self.PLAYER_PIECE) or self.winning_move(board, self.AI_PIECE) or len(self.get_valid_locations(board)) == 0
