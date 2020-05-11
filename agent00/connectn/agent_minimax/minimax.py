from connectn.common import PLAYER1, PLAYER2, GameState, BoardPiece
from connectn.common import connected_four
import numpy as np


def scoring(board: np.ndarray, player: BoardPiece) -> int:
    """
        Should evaluate the board and return scores for playing
        empty positions
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