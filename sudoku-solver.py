import numpy as np


def sudoku_solver(sudoku):
    '''
    Takes a single numpy array as input,
    checks board is valid,
    finds the empty spaces on the puzzle board,
    calls the sudoku solver,
    and then returns the appropriate output depending on the results of the solver.

    Parameters: 9x9 numpy array (unsolved Sudoku puzzle)
    Returns: 9x9 numpy array (solved Sudoku puzzle OR 9x9 array of -1)

    '''

    # initialise -1 array for output in case of no solution
    failure = np.full((9, 9), -1)

    # if invalid initial state then no need to call solver
    if check_invalid(sudoku):
        return failure

    # convert np array to list
    sudoku = sudoku.tolist()

    # find empty spaces - row, col tuple OR None if no spaces
    zeroes = find_spaces(sudoku)

    # call solver
    solution = solver(sudoku, zeroes)

    # if solver returns None - no solution for input board
    if solution is None:

        return failure

    # otherwise, convert returned board back to np array and return
    else:

        return np.array(solution)


def solver(sudoku, zeroes):
    '''
    Recursive method for solving sudoku.
    Generates an array of possible values for a given empty space on the board.
    Starts/continues DFS with first value in that array, fills in space on the board.
    Calls solver again with newly filled in board and space removed from zeroes array.
    If there are empty spaces, but no possible values for that space, backtrack to previous empty space, and try next value.
    If no more values then continue to backtrack.
    If at first space and no more possible values, return None > board is invalid.
    If no spaces left, board is finished, return finished board.


    Parameters: 9x9 numpy array, list[int] (unsolved Sudoku puzzle and list of empty spaces on the board)
    Returns: 9x9 numpy array, None(solved Sudoku puzzle OR None if invalid)

    '''

    # if there are still zero spaces on the board
    if zeroes:

        # take the next available space
        x, y = zeroes.pop(0)

        # store candidate values for zero space in list
        candidate_vals = generate_candidates(sudoku, x, y)

        # if generate_candidates returned None
        # board is invalid due to duplicates in adjacent spaces
        if candidate_vals == None:
            # clearing zeroes list will allow escape from recursion
            zeroes = []
            return

        for value in candidate_vals:

            sudoku[x][y] = value

            # this is the escape for the rescursion
            # solver will return None unless it has a finished solution
            # finished solution can then be returned here without setting the x,y to 0
            if solver(sudoku, zeroes) is not None:
                return sudoku

        # if no valid moves at position, set that position to zero
        sudoku[x][y] = 0

        # insert position into list of zeroes at beginning
        zeroes.insert(0, (x, y))

        # return steps back through recursion to previous zero position
        return

    # if there are no more zero positions then board must be complete so return board
    return sudoku


def find_spaces(sudoku):
    '''
    Finds the zeroes on the input sudoku puzzle.
    Scans through array and adds (x,y) coordinate to list where position is 0.

    Parameters: 9x9 numpy array
    Result: list(tuples) - Each tuple contains x,y position of 0's on the board.

   '''

    # initialise empty array
    zeroes = []

    for row_pos in range(9):

        for col_pos in range(9):

            if sudoku[row_pos][col_pos] == 0:
                # returns empty space in sudoku board
                zeroes.append((row_pos, col_pos))

    # if there was zeroes on the board, return coordinates
    if zeroes:

        return zeroes

    # shouldn't occur unless input is a solved board for some reason
    else:

        return None


def check_invalid(sudoku):
    '''
    Checks to ensure initial Sudoku board is not invalid due to duplicates in rows, cols, or boxes.

    Parameters: 9x9 numpy array - Current state of Sudoku puzzle.
    Returns: boolean (True for invalid board)
    '''

    # loop through rows and cols
    for idx in range(0, 9):

        row_vals = []
        col_vals = []

        # populate lists with values already in row and col
        row_vals = [sudoku[idx][i] for i in range(0, 9) if sudoku[idx][i] > 0]
        col_vals = [sudoku[i][idx] for i in range(0, 9) if sudoku[i][idx] > 0]

        # values on board with duplicates removed
        row_set = set(row_vals)
        col_set = set(col_vals)

        # if lens don't match then there is a duplicate
        if len(col_vals) != len(col_set) or len(row_vals) != len(row_set):
            return True

    # loop thorugh each box
    for row_idx in range(3):
        for col_idx in range(3):

            # initialise and clear box vals
            box_vals = []

            # loop thorugh 9 positions in box
            for i in range(3):
                for j in range(3):

                    if sudoku[(row_idx * 3) + i][(col_idx * 3) + j] > 0:
                        box_vals.append(sudoku[(row_idx * 3) + i][(col_idx * 3) + j])

            # set removes duplicates
            box_set = set(box_vals)

            if len(box_vals) != len(box_set):
                return True

    # if haven't returned by now then board is valid
    return False


def generate_candidates(sudoku, row, col):
    '''
    Generates candidate values for a space by eliminating numbers that appear in the same row, column, or box as the zero space.

    Parameters: 9x9 numpy array, int, int - Current state of Sudoku puzzle and row and col position of zero on board.
    Returns: list[int]
    '''

    # used for finding top left position of 3x3 box within 9x9 puzzle
    mod_row = row % 3
    mod_col = col % 3

    # populate lists with values already in adjacent rows and cols
    row_vals = [sudoku[row][i] for i in range(0, 9) if sudoku[row][i] > 0]
    col_vals = [sudoku[i][col] for i in range(0, 9) if sudoku[i][col] > 0]

    # populate lists with values already in box
    box_vals = []

    for i in range(3):
        for j in range(3):

            if sudoku[row + i - mod_row][col + j - mod_col] > 0:
                box_vals.append(sudoku[row + i - mod_row][col + j - mod_col])

    # create set containing row, col, box values
    # find and return complement of this set and set of numbers from 1-9
    final_set = set().union(box_vals, row_vals, col_vals)
    candidates = list(set(list(range(1, 10))) - final_set)
    return candidates

