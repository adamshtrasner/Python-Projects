############################################################
#                                                          #
# Nonogram Game - Python implementation using backtracking #
#                                                          #
############################################################

def create_board(rows_amount, cols_amount):
    """
    :param rows_amount: the amount of the rows according to the number of the row's constraints
    :param cols_amount: the amount of the columns according to the number of the column's constraints.
    :return: a (rows_amount)X(cols_amount) board (list of lists)
    """
    board = []
    for i in range(rows_amount):
        row = [-1]*cols_amount
        board.append(row)
    return board


def get_row_variations_helper(row, blocks, r, b, counter, var_lst):
    """
    The program fills squares or leaves them empty and appends
    the rows to a list according to the given blocks.
    :param row: a list of 0,1,-1
    :param blocks: constraints list
    :param r: pointer for the row list
    :param b: pointer for the blocks list
    :param counter: counting the filled squares according to a block
    :param var_lst: the variations list
    returns none.
    """
    if b == len(blocks):
        if row.count(1) == sum(blocks):
            while r != len(row):
                if row[r] == -1:
                    row[r] = 0
                r += 1
            var_lst.append(row)
        return

    if row.count(-1) == 0:
        # Base case: when there are no unknown squares.
        if row.count(1) == sum(blocks):
            # the number of filled squares equals the number of the blocks.
            var_lst.append(row)
        return

    if row.count(0) > len(row) - sum(blocks):
        # Base case: the number of empty spaces is invalid.
        return

    if row.count(1) > sum(blocks):
        # Base case: the number of filled squares is bigger than the number of the blocks.
        return

    if counter == blocks[b]:
        row[r] = 0
        get_row_variations_helper(row, blocks, r+1, b+1, 0, var_lst)
        return

    if row.count(1) == sum(blocks) and row.count(-1) == 0:
        while r != len(row):
            if row[r] == -1:
                row[r] = 0
            r += 1
        var_lst.append(row)
        return

    if row[r] == 0:
        if counter != 0:
            if counter == blocks[b]:
                get_row_variations_helper(row, blocks, r+1, b+1, 0, var_lst)
            else:
                return
        else:
            get_row_variations_helper(row, blocks, r+1, b, 0, var_lst)
    elif row[r] == 1:
        get_row_variations_helper(row, blocks, r+1, b, counter+1, var_lst)
    elif row[r] == -1:
        new_row = row[:]
        if counter == blocks[b] or counter == 0:
            row[r] = 0
            get_row_variations_helper(row, blocks, r+1, b, 0, var_lst)
        new_row[r] = 1
        get_row_variations_helper(new_row, blocks, r+1, b, counter+1, var_lst)
    return

def get_row_variations(row, blocks):
    """
    :param row: a list of 0,1,-1
    :param blocks: constraints list
    :return: a list of possible valid rows
    """
    var_lst = []
    new_row = row[:]
    get_row_variations_helper(new_row, blocks, 0, 0, 0, var_lst)
    return var_lst


def get_intersection_row(rows):
    """
    :param rows: the rows of the nonogram board
    :return: a row that is the intersection of all rows
    """
    inter_row = []
    for i in range(len(rows[0])):
        flag = True
        for j in range(len(rows) - 1):
            if rows[j][i] != rows[j+1][i]:
                # if the square in the 'j' position is not the same in each row,
                # then the 'j' position in the intersection row is unknown.
                flag = False
                break
        if flag:
            inter_row.append(rows[0][i])
        else:
            inter_row.append(-1)
    return inter_row

def column(board, pos):
    """
    :param board: the nonogram board. list of lists.
    :param pos: pointer
    :return: the column of the board according to a position(pos) given
    """
    col = []
    for i in range(len(board)):
        col.append(board[i][pos])
    return col


def conclude_from_constraints(board, constraints):
    """
    The program concludes the solution of each row according to the intersection rows.
    :param board: the nonogram rows. list of lists.
    :param constraints: a constraints list.
    """
    for i in range(len(board)):
        row = board[i][:]
        if row.count(-1) == 0:
            # if the row is completed, there's no use in checking it.
            pass
        else:
            board[i] = get_intersection_row(get_row_variations(row, constraints[0][i]))




def conclude_column(board, constraints):
    """
    The program concludes the solution of each column according to the intersection rows.
    :param board: the nonogram rows. list of lists.
    :param constraints: a constraints list.
    """
    for k in range(len(board[0])):
        col = column(board, k)
        if col.count(-1) == 0:
            # if the column is completed there's no use in checking it.
            pass
        else:
            new_col = get_intersection_row(get_row_variations(col, constraints[1][k]))
            for j in range(len(board)):
                board[j][k] = new_col[j]



def solved_board(board):
    """
    :param board: the nonogram rows. list of lists.
    :return: returns True if the board is solved(no "unknown" squares),
    and False otherwise.
    """
    for i in range(len(board)):
        if board[i].count(-1) != 0:
            return False
    return True




def solve_easy_nonogram(constraints):
    """
    :param constraints: a constraints list.
    :return: returns a solved board or half solved board if the solution
    cannot be concluded anymore.
    """
    board = create_board(len(constraints[0]), len(constraints[1]))
    board_helper = board[:]
    conclude_from_constraints(board, constraints)
    conclude_column(board, constraints)
    while board != board_helper:
        if solved_board(board):
            return board
        board_helper = board[:]
        conclude_from_constraints(board, constraints)
        conclude_column(board, constraints)
    return board


def solve_nonogram_helper(board, constraints, pos, boards_list):
    """
    The program finds rows in the board that are unsolved.
    It then checks for a solution of the board with every row's variation
    and backtracks accordingly.
    :param board: the nonogram board. list of lists.
    :param constraints: a constraints list
    :param pos: pointer
    :param boards_list: a list of lists. each list is an optional solution of the given board.
    """
    if solved_board(board):
        # Base case: if the board is solved(no "unknown" squares)
        boards_list.append(board)
        return
    if board[pos].count(-1) == 0:
        # if the row is solved
        solve_nonogram_helper(board, constraints, pos+1, boards_list)
    else:
        # if the row isn't solved
        variations = get_row_variations(board[pos], constraints[0][pos])
        board_helper = board[:]
        for i in range(len(variations)):
            board[pos] = variations[i]
            conclude_from_constraints(board, constraints)
            conclude_column(board, constraints)
            solve_nonogram_helper(board, constraints, pos+1, boards_list)
            board = board_helper[:]
    return

def solve_nonogram(constraints):
    """
    :param constraints: a constraints list.
    :return: a list of optional solutions of the nonogram board according
    to its constraints.
    """
    board = solve_easy_nonogram(constraints)
    boards_list = []
    solve_nonogram_helper(board, constraints, 0, boards_list)
    return boards_list

