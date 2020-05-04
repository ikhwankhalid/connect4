import numpy as np
from connectn.common import initialise_game_state

board = initialise_game_state()

def test_initialise_game_state():
    """
            Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """

    ret = initialise_game_state()

    # If one of these assertions fail, it logs as a failed test
    assert isinstance(ret, np.ndarray)  # Since ret is asserted as ndarray, pycharm 'knows'
    assert ret.dtype == np.int8         # Check array entries are integers
    assert ret.shape == (6, 7)          # Check board is the correct shape
    assert np.all(ret == 0)             # An array of booleans can't be interpreted as a boolean, so use "all"


def test_pretty_print_board():
    """
            Should return `board` converted to a human readable string representation,
            to be used when playing or printing diagnostics to the console (stdout). The piece in
            board[0, 0] should appear in the lower-left. Here's an example output:
            |==============|
            |              |
            |              |
            |    X X       |
            |    O X X     |
            |  O X O O     |
            |  O O X X     |
            |==============|
            |0 1 2 3 4 5 6 |
    """
    from connectn.common import pretty_print_board

    ret = pretty_print_board(board)

    assert type(ret) == str             # Pretty printed board should be a string


'''
def test_string_to_board():
    from connectn.common import string_to_board

    ret = string_to_board(pp_board)

    assert ret.dtype = np.ndarray
'''


def test_apply_player_action():
    """
        Should return a valid game board, and so must pass the same tests as 'initialise game state'.
        A further caveat is that there shouldn't be an empty slot below a board piece, since
        all pieces fall to the lowest available slot when played
        TODO: Should randomise board state, player action
    """
    from connectn.common import apply_player_action
    from connectn.common import initialise_game_state

    playboard = initialise_game_state()
    action = np.random.randint(0,6)

    ret = apply_player_action(playboard, action, 1)

    # If one of these assertions fail, it logs as a failed test
    assert isinstance(ret, np.ndarray)  # Since ret is asserted as ndarray, pycharm 'knows'
    assert ret.dtype == np.int8         # Check array entries are integers
    assert ret.shape == (6, 7)          # Check board is the correct shape
    for c in np.arange(7):              # Check that no non-zero element has a zero element below it
        for r in np.arange(5):
            if playboard[r+1][c] != 0:
                assert playboard[r][c] != 0


def test_connected_four():
    """
        Returns True if there are four adjacent pieces equal to `player` arranged
        in either a horizontal, vertical, or diagonal line. Returns False otherwise.
        If desired, the last action taken (i.e. last column played) can be provided
        for potential speed optimisation.
        TODO: Have both winning and not winning boards being tested
    """
    from connectn.common import initialise_game_state
    from connectn.common import connected_four

    playboard = initialise_game_state()
    ret = connected_four(playboard, 1)

    assert type(ret) == bool    # Either 'winning move' or 'not a winning move'
