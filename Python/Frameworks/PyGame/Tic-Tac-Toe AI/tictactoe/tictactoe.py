"""
Tic Tac Toe Player
"""

import math

# Constants for players and board state
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count the number of X's and O's on the board
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # If X is to play, return X, else return O
    return X if x_count == o_count else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    candidates = [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]
    return candidates


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = [row[:] for row in board]
    i, j = action
    if new_board[i][j] is not EMPTY:
        raise Exception("Please play a clean game!")
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check rows, columns, and diagonals for a winner
    for i in range(3):
        # Check rows and columns
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    return None  # Return None if no winner


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there's a winner or no empty cells left, the game is over
    if winner(board) or all(all(cell is not EMPTY for cell in row) for row in board):
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board using the minimax algorithm.
    """
    if terminal(board):
        return None

    if player(board) == X:
        value = -math.inf
        for action in actions(board):
            min_val = min_value(result(board, action))
            if min_val > value:
                value = min_val
                best_action = action
    else:
        value = math.inf
        for action in actions(board):
            max_val = max_value(result(board, action))
            if max_val < value:
                value = max_val
                best_action = action
    return best_action

def max_value(board):
    if terminal(board):
        return utility(board)
    value = -math.inf
    for action in actions(board):
        value = max(value, min_value(result(board, action)))
    return value

def min_value(board):
    if terminal(board):
        return utility(board)
    value = math.inf
    for action in actions(board):
        value = min(value, max_value(result(board, action)))
    return value
