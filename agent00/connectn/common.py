import numpy as np
from enum import Enum
from typing import Optional
from typing import Callable, Tuple


class SavedState:
    pass


BoardPiece = np.int8       # Data type for board entries
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)    # board[i, j] == PLAYER1 where player 1 has a piece
PLAYER2 = BoardPiece(2)    # board[i, j] == PLAYER2 where player 2 has a piece
PlayerAction = np.int8     # The column to be played


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialise_game_state() -> np.ndarray:
    """
        Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """
    return np.zeros((6, 7), dtype=BoardPiece)


def pretty_print_board(board: np.ndarray) -> str:
    """
        Returns `board` converted to a human readable string representation,
        to be used when playing or printing diagnostics to the console (stdout).
        TODO: Replace 1->X and 2->O in pretty print
    """
    board = np.flip(board, 0)  # Flip so that [0, 0] is the bottom left corner
    columns = np.arange(7)
    ret = np.vstack((board, columns))
    ret = np.array2string(ret)
    return ret


def string_to_board(pp_board: str) -> np.ndarray:
    """
        Takes the output of pretty_print_board and turns it back into an ndarray.
    """
    raise NotImplemented()


def apply_player_action(
        board: np.ndarray, action: PlayerAction, player: BoardPiece, copy: bool = False
) -> np.ndarray:
    """
        Sets board[i, action] = player, where i is the lowest open row. The modified
        board is returned. If copy is True, makes a copy of the board before modifying it.
    """
    if copy:
        ret = np.copy(board)
        for r in range(6):  # We have 6 rows on the game board
            if ret[r, action] == 0:
                ret[r, action] = player
                return ret
    else:
        for r in range(6):  # We have 6 rows on the game board
            if board[r, action] == 0:
                board[r, action] = player
                return board


def connected_four(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> bool:
    """
        Returns True if there are four adjacent pieces equal to `player` arranged
        in either a horizontal, vertical, or diagonal line. Returns False otherwise.
        If desired, the last action taken (i.e. last column played) can be provided
        for potential speed optimisation.
    """
    # Check for horizontal fours
    for c in np.arange(4):
        for r in np.arange(6):
            if board[r, c] == board[r, c + 1] == board[r, c + 2] == board[r, c + 3] == player:
                return True

    # Check for vertical fours
    for c in np.arange(7):
        for r in np.arange(3):
            if board[r, c] == board[r + 1, c] == board[r + 2, c] == board[r + 3, c] == player:
                return True

    # Check upward diagonals
    for c in np.arange(4):
        for r in np.arange(3):
            if board[r, c] == board[r + 1, c + 1] == board[r + 2, c + 2] == board[r + 3, c + 3] == player:
                return True

    # Check downward diagonals
    for c in np.arange(4):
        for r in np.arange(3, 6):
            if board[r, c] == board[r - 1, c - 1] == board[r - 2, c - 2] == board[r - 3, c - 3] == player:
                return True
    else:
        return False


def check_end_state(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> GameState:
    """
    Returns the current game state for the current `player`, i.e.  whether their last
    action has won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or if play still on-going (GameState.STILL_PLAYING)
    """
    if connected_four(board, player, last_action):
        return GameState(1)
    elif np.all(board) != 0:
        return GameState(-1)
    else:
        return GameState(0)


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    Tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]
