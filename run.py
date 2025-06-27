import pygame
import math
import sys
import Agent
import game

# Initialize pygame
pygame.init()

# Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Select Board Size and Difficulty")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Global score variables
player_score = 0
ai_score = 0

# Function to draw buttons for difficulty selection
def draw_difficulty_selection():
    # Load background image
    background_image = pygame.image.load('background_image.png')
    screen.blit(background_image, (0, 0))

    # Draw title for difficulty selection
    title_text = title_font.render("Choose Difficulty Level", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw buttons for difficulty selection
    font = pygame.font.Font('freesansbold.ttf', 28)

    # List of difficulty levels and their corresponding depths
    difficulty_levels = [("Beginner", 2), ("Intermediate", 4), ("Advanced", 6)]

    # Calculate vertical spacing for buttons
    button_spacing = 20

    # Draw buttons for difficulty selection
    for i, (difficulty, depth) in enumerate(difficulty_levels):
        button_rect = pygame.Rect(300, 200 + i * (50 + button_spacing), 200, 50)
        pygame.draw.rect(screen, RED, button_rect, border_radius=5)
        text = font.render(difficulty, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.update()

    return difficulty_levels

# Function to draw buttons for board size selection
def draw_board_size_selection():
    # Load background image
    background_image = pygame.image.load('background_image.png')
    screen.blit(background_image, (0, 0))

    # Draw title for board size selection
    title_text = title_font.render("Select Board Size", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
    screen.blit(title_text, title_rect)

    # Draw buttons for board size selection with rounded rectangles
    button_color = (255, 0, 0)  # Red
    button_hover_color = (200, 0, 0)  # Darker red on hover
    font = pygame.font.Font('freesansbold.ttf', 28)

    # List of board sizes and their corresponding scores
    board_sizes = [(6, 7), (8, 9), (10, 11)]

    # Calculate vertical spacing for buttons
    button_spacing = 20

    # Draw buttons for board size selection
    for i, (rows, cols) in enumerate(board_sizes):
        button_rect = pygame.Rect(300, 200 + i * (50 + button_spacing), 200, 50)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=5)
        text = font.render(f"{rows}x{cols}", True, (255, 255, 255))
        text_rect = text.get_rect(center=button_rect.center)
        screen.blit(text, text_rect)

    pygame.display.update()

    return board_sizes

# Function to run the game loop and return the winner
def run_game(board_size, depth):
    global player_score, ai_score

    game_instance = game.game(board_size)  # Use game instead of Game
    AB = Agent.AlphaBetaAgent()
    MCTS=Agent.MonteCarloAgent()
    board = game_instance.create_board()  # create board
    game_instance.draw_board(board)
    pygame.display.update()

    player_score = 0
    ai_score = 0

    for _ in range(5):  # Run for 5 rounds
        while not game_instance.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Ask for Player1 input
                    if game_instance.turn == game_instance.PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx / game_instance.SQUARESIZE))
                        if game_instance.is_valid_location(board, col):
                            row = game_instance.get_next_open_row(board, col)
                            game_instance.drop_piece(board, row, col, game_instance.PLAYER_PIECE)
                            if game_instance.winning_move(board, game_instance.PLAYER_PIECE):
                                print("Player1 won !! Congrats !!")
                                player_score += 1  # Increment player score
                                game_instance.game_over = True
                            if game_instance.is_draw(board):
                                game_instance.game_over = True
                        game_instance.print_board(board)
                        game_instance.draw_board(board)
                        game_instance.turn += 1
                        game_instance.turn = game_instance.turn % 2

            # Ask for AI input
            if game_instance.turn == game_instance.AI and not game_instance.game_over:
                if depth==2:
                    col=MCTS.monte_carlo_search(board, game_instance)
                else:
                    col, minimax_score = AB.alphabeta(board, depth, True, game_instance)
                if game_instance.is_valid_location(board, col):
                    row = game_instance.get_next_open_row(board, col)
                    game_instance.drop_piece(board, row, col, game_instance.AI_PIECE)
                    if game_instance.winning_move(board, game_instance.AI_PIECE):
                        print("Player2 won !! Congrats !!")
                        ai_score += 1  # Increment AI score
                        game_instance.game_over = True
                    if game_instance.is_draw(board):
                        game_instance.game_over = True

                    game_instance.draw_board(board)
                    game_instance.turn += 1
                    game_instance.turn = game_instance.turn % 2

        # Display scores after each round
        screen.fill(BLACK)  # Clear the screen
        font = pygame.font.SysFont(None, 25)
        player_score_text = font.render(f'Player1 Score: {player_score}', True, WHITE)
        ai_score_text = font.render(f'Player2 Score: {ai_score}', True, WHITE)
        screen.blit(player_score_text, (20, 20))
        screen.blit(ai_score_text, (190, 20))
        pygame.display.flip()

        # Reset the game for the next round
        game_instance.game_over = False
        game_instance.turn = 0
        board = game_instance.create_board()
        game_instance.draw_board(board)
        pygame.display.update()

    return player_score, ai_score

# Call the function to draw the difficulty selection menu
difficulty_levels = draw_difficulty_selection()

# Event loop for selecting difficulty level
depth = None
button_spacing=20
while depth is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, (_, d) in enumerate(difficulty_levels):
                if 300 <= mouse_pos[0] <= 500 and 200 + i * (50 + button_spacing) <= mouse_pos[1] <= 250 + i * (50 + button_spacing):
                    depth = d
                    break

# Call the function to draw the board size selection menu
board_sizes = draw_board_size_selection()

# Event loop for selecting board size
board_size = None
while board_size is None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, (rows, cols) in enumerate(board_sizes):
                if 300 <= mouse_pos[0] <= 500 and 200 + i * (50 + button_spacing) <= mouse_pos[1] <= 250 + i * (50 + button_spacing):
                    board_size = (rows, cols)
                    break

# Run the game loop
player_score, ai_score = run_game(board_size, depth)

# Print final scores
print(f"Final scores - Player1: {player_score}, Player2: {ai_score}")

# Quit pygame
pygame.quit()
