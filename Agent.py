from game import game
import math
import random
from EvaluationFunction import evaluationFunction
import copy

class MinimaxAgent():

    def __init__(self):
        self.evaluation_function=evaluationFunction()
        pass

    def minimax(self, board, depth, maximizingPlayer, gameState: game):
        if depth == 0 or gameState.isTerminalNode(board):
            if gameState.isTerminalNode(board):
                if gameState.winning_move(board,gameState.AI_PIECE):
                    return None, 10000000
                elif gameState.winning_move(board, gameState.PLAYER_PIECE):
                    return None, -10000000
                else:
                    return None, 0
            else:
                obj=self.evaluation_function
                return None, obj.score_positions(board, gameState.AI_PIECE, gameState)
        
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(gameState.get_valid_locations(board))
            for col in gameState.get_valid_locations(board):
                row = gameState.get_next_open_row(board, col)
                b_copy = board.copy()
                gameState.drop_piece(b_copy, row, col, gameState.AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, False, gameState)[1]
                if new_score > value:
                    value = new_score
                    column = col
            return column, value
            
        else:
            value = math.inf
            column = random.choice(gameState.get_valid_locations(board))
            for col in gameState.get_valid_locations(board):
                row = gameState.get_next_open_row(board, col)
                b_copy = board.copy()
                gameState.drop_piece(b_copy, row, col, gameState.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, True, gameState)[1]
                if new_score < value:
                    value = new_score
                    column = col
            return column, value
        


# # inst=MinimaxAgent()
        
class AlphaBetaAgent():
    def __init__(self):
        self.evaluation_function = evaluationFunction()

    def alphabeta(self, board, depth, maximizingPlayer, gameState:game, alpha=-math.inf, beta=math.inf):

        if depth == 0 or gameState.isTerminalNode(board):
            if gameState.isTerminalNode(board):
                # Evaluate the terminal state
                if gameState.winning_move(board, gameState.AI_PIECE):
                    return None, 10000000  # Large reward for winning AI
                elif gameState.winning_move(board, gameState.PLAYER_PIECE):
                    return None, -10000000  # Large penalty for losing AI
                else:
                    return None, 0  # Tie

            else:  # Non-terminal state (evaluate using evaluation function)
                score = self.evaluation_function.score_positions(board, gameState.AI_PIECE, gameState)
                return None, score

        # Maximizing Player (explore all valid moves)
        if maximizingPlayer:
            value = -math.inf
            best_column = None
            for col in gameState.get_valid_locations(board):
                row = gameState.get_next_open_row(board, col)
                b_copy = board.copy()
                gameState.drop_piece(b_copy, row, col, gameState.AI_PIECE)
                _, new_score = self.alphabeta(b_copy, depth - 1, False, gameState, alpha, beta)
                if new_score > value:
                    value = new_score
                    best_column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    return best_column, value  # Beta cut-off

        # Minimizing Player
        else:
            value = math.inf
            best_column = None
            for col in gameState.get_valid_locations(board):
                row = gameState.get_next_open_row(board, col)
                b_copy = board.copy()
                gameState.drop_piece(b_copy, row, col, gameState.PLAYER_PIECE)
                _, new_score = self.alphabeta(b_copy, depth - 1, True, gameState, alpha, beta)
                if new_score < value:
                    value = new_score
                    best_column = col
                beta = min(beta, value)
                if beta <= alpha:
                    return best_column, value  # Alpha cut-off

        return best_column, value


class MonteCarloAgent:
    def __init__(self, simulations=200):
        self.simulations = simulations
        self.evaluation_function = evaluationFunction()

    def monte_carlo_search(self, board, gameState:game):
        root = Node(board, None, gameState)
       

        for _ in range(self.simulations):
            node = root
            piece=gameState.AI_PIECE
            # print(node.visits)
            temp_game_state = copy.copy(gameState)
            temp_board = board.copy()

            # Selection phase
            while not node.is_terminal():
                if not node.is_fully_expanded():
                    node = node.expand(piece)
                    temp_board=node.board
                    # temp_game_state.print_board(temp_board)
                    if piece==gameState.AI_PIECE:
                        piece=gameState.PLAYER_PIECE
                    else:
                        piece=gameState.AI_PIECE
                    break
                else:
                    node = node.select_child(piece, gameState)
                    temp_board=node.board
                    # temp_game_state.print_board(temp_board)
                    if piece==gameState.AI_PIECE:
                        piece=gameState.PLAYER_PIECE
                    else:
                        piece=gameState.AI_PIECE
                    if node.visits==0:
                        # print("hello",_)
                        break

            # Simulation phase
            winner = node.simulate(temp_board, temp_game_state, piece) 
            # temp_game_state.print_board(temp_board)
            # Backpropagation phase
            while node is not None:
                node.update(winner)
                # print(node.wins," ",node.visits)
                node = node.parent

        # Choose the best move based on the most visited child
        return root.best_child(gameState).move


class Node:
    def __init__(self, board, move, game_state, parent=None):
        self.board = board
        self.move = move
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.score=0  #scoring positions
        self.evaluation_function = evaluationFunction()

    def get_number_of_visits(self):
        return self.visits

    def is_terminal(self):
        return self.game_state.isTerminalNode(self.board)

    def is_fully_expanded(self):
        return len(self.children) == len(self.game_state.get_valid_locations(self.board))

    def expand(self, piece):
        valid_moves = self.game_state.get_valid_locations(self.board)
        for move in valid_moves:
            temp_board = self.board.copy()
            # print(temp_board)
            temp_game_state = self.game_state
            row = temp_game_state.get_next_open_row(temp_board, move)
            temp_game_state.drop_piece(temp_board, row, move, piece)
            self.children.append(Node(temp_board, move, temp_game_state, self))
        return random.choice(self.children)

    def select_child(self, piece, game_state:game):
        C = 1.414  # Exploration parameter
        selected_child = None
        max_uct = -math.inf
        min_uct = math.inf

        for child in self.children:
            try:
                # if piece==game_state.PLAYER_PIECE:
                #     uct = 1-(child.wins / child.visits) + C * math.sqrt(math.log(self.visits) / child.visits)
                # else:
                uct=(child.wins / child.visits) + C * math.sqrt(math.log(self.visits) / child.visits)
                # uct=child.wins + C * math.sqrt(math.log(self.visits) / child.visits)
            except ZeroDivisionError:
                uct=math.inf
            
            #considering that the players chooses optimal moves
            if piece==game_state.AI_PIECE:
                if uct > max_uct:
                    max_uct = uct
                    selected_child = child
            else:
                if uct < min_uct:
                    min_uct = uct
                    selected_child = child
        # print(max_uct)

        return selected_child

    def simulate(self, board, game_state, piece):        
        temp_board = board.copy()
        temp_game_state = copy.copy(game_state)
        #adding
        # piece = temp_game_state.PLAYER_PIECE
        while not temp_game_state.isTerminalNode(temp_board):
            valid_moves = temp_game_state.get_valid_locations(temp_board)
            random_move = random.choice(valid_moves)
            row = temp_game_state.get_next_open_row(temp_board, random_move)
            temp_game_state.drop_piece(temp_board, row, random_move, piece)

            # self.score+=self.evaluation_function.score_positions(temp_board, piece, temp_game_state)    # different scoring

            # game_state.print_board(temp_board)

            if temp_game_state.winning_move(temp_board, piece):
                return piece
            
            if(piece==temp_game_state.PLAYER_PIECE):
                piece=temp_game_state.AI_PIECE
            else:
                piece=temp_game_state.PLAYER_PIECE

        return 0  # Tie

    def update(self, winner):
        self.visits += 1
        if winner == self.game_state.AI_PIECE:
            self.wins += 1
        elif winner==self.game_state.PLAYER_PIECE:
            self.wins += 0
        # self.score=0

    def best_child(self,game_state):
        # return self.select_child(game_state.AI_PIECE, game_state)
        return self.select_child(game_state.AI_PIECE, game_state)


