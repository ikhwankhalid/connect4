import numpy as np
from connectn.common import BoardPiece, PlayerAction, SavedState
from typing import Optional
from typing import Tuple


def generate_move_random(
        board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    """
    Choose a valid, non-full column randomly and return it as an action
    """
    valid_move = False
    while not valid_move:
        action = np.random.randint(0, 7)
        if board[5, action] == 0:
            valid_move = True
    return action, saved_state
