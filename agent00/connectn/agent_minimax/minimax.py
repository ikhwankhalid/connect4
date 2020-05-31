from connectn.common import PLAYER1, PLAYER2, NO_PLAYER, GameState, BoardPiece, PlayerAction, SavedState
from connectn.common import connected_four, apply_player_action
from typing import Optional
from typing import Tuple
import numpy as np

depth = 5


def heuristic(board: np.ndarray, player: BoardPiece) -> int:
    """
        Returns a heuristic for a given position on the game board
    """
    score = 0

    # Determine if agent is player1 or player2
    if player == PLAYER1:
        opp = PLAYER2
    else:
        opp = PLAYER1

    for r in range(0, board.shape[0]):
        for c in range(board.shape[1]):
            # Check horizontal scores
            try:
                # Add player scores
                if board[r][c] == board[r + 1][c] == player:
                    score += 10
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == player:
                    score += 100
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == player:
                    score += 100000

                # Subtract opponent scores
                if board[r][c] == board[r + 1][c] == opp:
                    score -= 10
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == opp:
                    score -= 1000
                if board[r][c] == board[r + 1][c] == board[r + 2][c] == board[r + 3][c] == opp:
                    score -= 1000000
            except IndexError:
                pass

            # Check vertical scores
            try:
                # Add player scores
                if board[r][c] == board[r][c + 1] == player:
                    score += 10
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == player:
                    score += 100
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r + 3][c + 3] == player:
                    score += 100000

                # Subtract opponent scores
                if board[r][c] == board[r][c + 1] == opp:
                    score -= 10
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == opp:
                    score -= 1000
                if board[r][c] == board[r][c + 1] == board[r][c + 2] == board[r + 3][c + 3] == opp:
                    score -= 1000000
            except IndexError:
                pass

            # Check upward diagonals
            try:
                # Add player scores
                if not c + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == player:
                    score += 10
                if not c + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][
                    c + 2] == player:
                    score += 100
                if not c + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] \
                        == board[r + 3][c + 3] == player:
                    score += 100000

                # Subtract opponent scores
                if not c + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == opp:
                    score -= 10
                if not c + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] == opp:
                    score -= 1000
                if not c + 3 > board.shape[1] and board[r][c] == board[r + 1][c + 1] == board[r + 2][c + 2] \
                        == board[r + 3][c + 3] == opp:
                    score -= 1000000
            except IndexError:
                pass

            # Check downward diagonals
            try:
                # Add player scores
                if not c - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == player:
                    score += 10
                if not c - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][
                    c - 2] == player:
                    score += 100
                if not c - 3 > board.shape[1] and board[r][c] == board[r + 1][c - 1] == board[r - 2][c - 2] \
                        == board[r - 3][c - 3] == player:
                    score += 100000

                # Subtract opponent scores
                if not c - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == opp:
                    score -= 10
                if not c - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][c - 2] == opp:
                    score -= 1000
                if not c - 3 > board.shape[1] and board[r][c] == board[r - 1][c - 1] == board[r - 2][c - 2] \
                        == board[r - 3][c - 3] == opp:
                    score -= 1000000
            except IndexError:
                pass

    return score


def generate_move_mm(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    best_score, action = mini_max(board, player, 2)

    return action, saved_state


def mini_max(board, player, depth):
    if not GameState.STILL_PLAYING:
        return -10000000 if player else 10000000, -1
    elif depth == 0:
        return heuristic(board, player), -1

    if player:
        best_score = -10000000
        replace = lambda x: x > best_score
    else:
        best_score = 10000000
        replace = lambda x: x < best_score

    best_move = -1

    children = []
    for i in range(board.shape[1]):
        if board[board.shape[0]-1, i] < board.shape[0]-1:
            child = np.copy(board)
            apply_player_action(child, i, player)
            children.append((i, child))

    for child in children:
        move, child_board = child
        interim = mini_max(child_board, player, depth-1)[0]
        if replace(interim):
            best_score = interim
            best_move = move

    return best_score, best_move
