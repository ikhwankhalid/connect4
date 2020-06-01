from connectn.common import PLAYER1, PLAYER2, GameState, BoardPiece, SavedState, check_end_state
from connectn.common import apply_player_action
from typing import Optional
import numpy as np


def heuristic(board):
    """
    Performs a heuristic on a given game board and returns a score for it. Higher (positive) scores are
    advantageous to player 1 while lower (negative) scores are advantageous to player 2.

    Parameters
    ----------
    board : np.ndarray
        The configuration of the game board.

    Returns
    -------
    score : int
        A score for a given game board configuration.
    """
    score = 0

    for r in range(0, 6):
        for c in range(0, 7):
            # Check vertical scores
            try:
                # Add PLAYER1 scores
                if board[r][c] == board[r + 1][c] == PLAYER1:
                    score += 10
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == PLAYER1:
                    score += 100
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == PLAYER1:
                    score += 100000

                # Subtract PLAYER2 scores
                if board[r][c] == board[r + 1][c] == PLAYER2:
                    score -= 10
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == PLAYER2:
                    score -= 100
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == PLAYER2:
                    score -= 100000
            except IndexError:
                pass

            # Check horizontal scores
            try:
                # Add PLAYER1 scores
                if board[r][c] == board[r][c + 1] == PLAYER1:
                    score += 10
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == PLAYER1:
                    score += 100
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == PLAYER1:
                    score += 100000

                # Subtract PLAYER2 scores
                if board[r][c] == board[r][c + 1] == PLAYER2:
                    score -= 10
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == PLAYER2:
                    score -= 100
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r][c + 3] == PLAYER2:
                    score -= 100000
            except IndexError:
                pass

            # Check upward diagonals
            try:
                # Add PLAYER1 scores
                if not r + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == PLAYER1:
                    score += 10
                if not r + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][
                    c + 2] == PLAYER1:
                    score += 100
                if not r + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] \
                        == board[r + 3][c + 3] == PLAYER1:
                    score += 100000

                # Subtract PLAYER2 scores
                if not r + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == PLAYER2:
                    score -= 10
                if not r + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == PLAYER2:
                    score -= 100
                if not r + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] \
                        == board[r + 3][c + 3] == PLAYER2:
                    score -= 100000
            except IndexError:
                pass

            # Check downward diagonals
            try:
                # Add PLAYER1 scores
                if not r - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == PLAYER1:
                    score += 10
                if not r - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][
                    c - 2] == PLAYER1:
                    score += 100
                if not r - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][c - 2] \
                        == board[r - 3][c - 3] == PLAYER1:
                    score += 100000

                # Subtract PLAYER2 scores
                if not r - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == PLAYER2:
                    score -= 10
                if not r - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][c - 2] == PLAYER2:
                    score -= 100
                if not r - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][c - 2] \
                        == board[r - 3][c - 3] == PLAYER2:
                    score -= 100000
            except IndexError:
                pass

    return score


def generate_move_mmab(board, player, saved_state: Optional[SavedState]):
    """
    Takes in a given board configuration and player as input, then uses the minimax algorithm
    with alpha-beta pruning to generate a move. Depth of the game tree has been fixed to be 8

    Parameters
    ----------
    board : np.ndarray
        The configuration of the board currently in play.
    player : BoardPiece
        The player to generate a move for
    saved_state :
        Not Implemented

    Returns
    -------
    action : int
        An action to play generated from the minimax algorithm
    """
    depth = 8
    alpha = -100000000
    beta = 100000000
    best_score, action = mini_max_ab(board, player, depth, alpha, beta)

    return action, saved_state


def mini_max_ab(board, player, depth, alpha, beta):
    """
    Takes in a board configuration, player, and tree depth as input, then performs a tree-search of the game
    space using a minimax algorithm with alpha-beta pruning. Outputs the best score and the corresponding
    best move for the given depth.

    Parameters
    ----------
    board : np.ndarray
        Configuration of the game board
    player : BoardPiece
        Maximising/minimising player
    depth : int
        Maximum depth of the tree-search algorithm
    alpha : int
        Minimum score of the maximising player
    beta : int
        Maximum score of the minimising player

    Returns
    -------
    best_score : int
        The best possible score attainable for the given tree-search depth
    best_move : int
        The move which brings the system towards the best score
    """
    # Check if the board is a draw, which we heavily penalise
    # Otherwise return the score of the board
    end_state = check_end_state(board, player)
    if end_state == GameState.IS_DRAW:
        if player == PLAYER1:
            return -100000000, -1
        else:
            return 100000000, -1
    elif depth == 0:
        return heuristic(board), -1

    # Initialise best scores for each player
    # Also define functions which check if best score should be updated
    if player == PLAYER1:
        best_score = -10000000
        replace = lambda x: x > best_score
    elif player == PLAYER2:
        best_score = 10000000
        replace = lambda x: x < best_score

    # Initialise best move
    best_move = -1

    # Create child boards with all possible moves
    children = []
    for i in range(7):
        if board[5, i] == 0:
            child = np.copy(board)
            child = apply_player_action(child, i, player)
            children.append((i, child))

    # Switch player
    if player == PLAYER1:
        player = PLAYER2
    elif player == PLAYER2:
        player = PLAYER1

    # Get scores of child boards
    for child in children:
        move, child_board = child
        interim = mini_max_ab(child_board, player, depth - 1, alpha, beta)[0]

        # Replace best score and best move if a move leads to a 'better' score for the player
        if replace(interim):
            best_score = interim
            best_move = move

        # Perform alpha-beta pruning
        if player == PLAYER1:
            alpha = max(alpha, interim)
        else:
            beta = min(beta, interim)
        if alpha >= beta:
            break

    return best_score, best_move
