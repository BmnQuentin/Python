import numpy as np

my_grid = [[3, 0, 0, 0, 0, 0, 6, 7, 0],
           [4, 7, 0, 0, 0, 0, 0, 1, 2],
           [0, 0, 9, 0, 3, 0, 0, 0, 8],
           [0, 1, 0, 7, 0, 9, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 2, 0, 3, 0, 4, 0],
           [6, 0, 0, 0, 5, 0, 2, 0, 0],
           [5, 8, 0, 0, 0, 0, 0, 6, 3],
           [0, 3, 7, 0, 0, 0, 0, 0, 4]]


def is_valid(grid, number, x, y):
    if grid[y][x] != 0:
        return False
    for i in range(9):
        if grid[y][i] == number:
            return False
    for j in range(9):
        if grid[j][x] == number:
            return False
    block_x = int(x / 3)
    block_y = int(y / 3)
    for i in range(3):
        for j in range(3):
            if grid[j + block_y * 3][i + block_x * 3] == number:
                return False
    return True


def find_blanks(grid):
    for i in range(9):
        for j in range(9):
            if grid[j][i] == 0:
                return i, j
    return None


def sudoku_solver(grid):
    if not find_blanks(grid):
        return True
    else:
        i, j = find_blanks(grid)
        for n in range(9):
            if is_valid(grid, n+1, i, j):
                grid[j][i]= n+1
                if sudoku_solver(grid):
                    return True
                grid[j][i] = 0  # backtrack happens here
        return False


sudoku_solver(my_grid)

print(np.matrix(my_grid))
