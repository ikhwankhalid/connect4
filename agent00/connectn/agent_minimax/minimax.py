from connectn.common import PLAYER1, PLAYER2, NO_PLAYER, GameState, BoardPiece
from connectn.common import connected_four
import numpy as np


def position_scoring(board: np.ndarray, player: BoardPiece) -> int:
    """
        Should evaluate the board and return scores for possible moves
        TODO: Column scoring
    """
    score = 0
    for r in board.shape[0]:
        r_window = [i for i in board[r, :]]
        for c in board.shape[1] - 3:
            c_window = r_window[c:c + 4]
            if c_window.count(player) == 4:
                score += 1000
            elif c_window.count(player) == 3 and c_window.count(NO_PLAYER) == 1:
                score += 100
            elif c_window.count(player) == 2 and c_window.count(NO_PLAYER) == 2:
                score += 10
            elif c_window.count(player) == 1 and c_window.count(NO_PLAYER) == 3:
                score += 1
    return score


def best_move(board: np.ndarray, player: BoardPiece):
    """
        Should find the best column to play by applying actions then
        computing the new score
    """
    pass


def minimax(board, depth, player: str):
    """
        Should return the best possible score via tree search
        at some depth performed on the board
    """
    if player == PLAYER1:
        human = PLAYER2
    else:
        human = PLAYER1
    if depth == 0 or GameState.STILL_PLAYING:
        #  If winning move for the AI, return a large score,
        #  if winning move for the opponent, return a large negative score
        if GameState.STILL_PLAYING:
            if connected_four(board, player):
                return 1000000000
            elif connected_four(board, human):
                return -1000000000
            else:
                return 0  #
        else:
            return scoring(board, player)

    '''  
    TODO: 
    if maximizingPlayer then
        value := −∞
    for each child of node do
        value := max(value, minimax(child, depth − 1, FALSE))
        return value

    else (*minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value'''
