from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    r, c = coord
    r_target, c_target = r, c
    rand_dir = choice(("up", "right"))
    num_cols = len(grid[0])
    if rand_dir == "up" and r - 2 >= 0:
        r_target, c_target = r - 1, c
    else:
        rand_dir = "right"

    if rand_dir == "right" and c + 1 < num_cols - 1:
        r_target, c_target = r, c + 1
    elif r - 2 >= 0:
        r_target, c_target = r - 1, c
    grid[r_target][c_target] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    open_cells = []
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if i % 2 == 1 and j % 2 == 1:
                grid[i][j] = " "
                open_cells.append((i, j))

    for cell in open_cells:
        i, j = cell
        grid = remove_wall(grid, (i, j))

    if random_exit:
        in_row, out_row = randint(0, rows - 1), randint(0, rows - 1)
        in_col = randint(0, cols - 1) if in_row in (0, rows - 1) else choice((0, cols - 1))
        out_col = randint(0, cols - 1) if out_row in (0, rows - 1) else choice((0, cols - 1))
    else:
        in_row, in_col = 0, cols - 2
        out_row, out_col = rows - 1, 1

    grid[in_row][in_col], grid[out_row][out_col] = "X", "X"
    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits_list = []
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if grid[i][j] == "X":
                exits_list.append((i, j))
    return exits_list


def make_step(grid: List[List[Union[str, int]]], step_val: int) -> List[List[Union[str, int]]]:
    num_rows = len(grid)
    num_cols = len(grid[0])
    for i, row in enumerate(grid):
        for j, _ in enumerate(row):
            if grid[i][j] == step_val:
                if i + 1 < num_rows and grid[i + 1][j] == 0:
                    grid[i + 1][j] = step_val + 1
                if i - 1 >= 0 and grid[i - 1][j] == 0:
                    grid[i - 1][j] = step_val + 1
                if j + 1 < num_cols and grid[i][j + 1] == 0:
                    grid[i][j + 1] = step_val + 1
                if j - 1 >= 0 and grid[i][j - 1] == 0:
                    grid[i][j - 1] = step_val + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    def neighbors(grid, pos, val):
        num_rows = len(grid)
        num_cols = len(grid[0])
        i, j = pos
        if i + 1 < num_rows and grid[i + 1][j] == val - 1:
            return (i + 1, j)
        if i - 1 >= 0 and grid[i - 1][j] == val - 1:
            return (i - 1, j)
        if j + 1 < num_cols and grid[i][j + 1] == val - 1:
            return (i, j + 1)
        if j - 1 >= 0 and grid[i][j - 1] == val - 1:
            return (i, j - 1)

    path_seq = []
    cur_pos = exit_coord
    max_step = grid[cur_pos[0]][cur_pos[1]]
    path_seq.append(exit_coord)
    while int(grid[cur_pos[0]][cur_pos[1]]) > 1:
        neighbor_pos = neighbors(grid, cur_pos, grid[cur_pos[0]][cur_pos[1]])
        path_seq.append(neighbor_pos)
        cur_pos = neighbor_pos
    if len(path_seq) != max_step:
        err_i, err_j = path_seq[1]
        grid[err_i][err_j] = 0
        return shortest_path(grid, exit_coord)
    return path_seq


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    num_rows = len(grid)
    num_cols = len(grid[0])
    i, j = coord
    if (
        i == 0
        and j == 0
        or i == 0
        and j == num_cols - 1
        or i == num_rows - 1
        and j == 0
        or i == num_rows - 1
        and j == num_cols - 1
    ):
        return True
    elif (
        i == 0
        and grid[i + 1][j] != " "
        or i == num_rows - 1
        and grid[i - 1][j] != " "
        or j == 0
        and grid[i][j + 1] != " "
        or j == num_cols - 1
        and grid[i][j - 1] != " "
    ):
        return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    exits_found = get_exits(grid)
    if len(exits_found) < 1:
        return grid, None
    if len(exits_found) == 1:
        return grid, exits_found[0]
    if encircled_exit(grid, exits_found[0]) or encircled_exit(grid, exits_found[1]):
        return grid, None
    grid_dup = deepcopy(grid)
    for i, row in enumerate(grid_dup):
        for j, _ in enumerate(row):
            if grid_dup[i][j] == " " or grid_dup[i][j] == "X":
                grid_dup[i][j] = 0
    i_start, j_start = exits_found[0]
    grid_dup[i_start][j_start] = 1
    k_val = 1
    i_end, j_end = exits_found[1]
    while True:
        almost_done = make_step(grid_dup, k_val)
        k_val += 1
        if int(grid_dup[i_end][j_end]) > 0:
            break
    route = shortest_path(grid_dup, exits_found[1])
    return grid_dup, route


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    MAZE_GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(MAZE_GRID))
    _, FOUND_PATH = solve_maze(MAZE_GRID)
    FINAL_MAZE = add_path_to_grid(MAZE_GRID, FOUND_PATH)
    print(pd.DataFrame(FINAL_MAZE))
