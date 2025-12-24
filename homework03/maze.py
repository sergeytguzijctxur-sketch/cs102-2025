from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    x, y = coord
    grid[x][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    if rows < 5 or cols < 5:
        raise ValueError("Лабиринт должен быть минимум 5x5")

    grid = create_grid(rows, cols)
    empty_cells: List[Tuple[int, int]] = []

    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        directions: List[Tuple[int, int]] = []

        if x - 2 >= 1:
            directions.append((-1, 0))
        if y + 2 < cols - 1:
            directions.append((0, 1))

        if directions:
            dx, dy = choice(directions)
            grid = remove_wall(grid, (x + dx, y + dy))

    if random_exit:
        side_in = choice(["top", "bottom", "left", "right"])
        if side_in == "top":
            x_in, y_in = 0, randint(1, cols - 2)
        elif side_in == "bottom":
            x_in, y_in = rows - 1, randint(1, cols - 2)
        elif side_in == "left":
            x_in, y_in = randint(1, rows - 2), 0
        else:
            x_in, y_in = randint(1, rows - 2), cols - 1

        side_out = choice([s for s in ["top", "bottom", "left", "right"] if s != side_in])
        if side_out == "top":
            x_out, y_out = 0, randint(1, cols - 2)
        elif side_out == "bottom":
            x_out, y_out = rows - 1, randint(1, cols - 2)
        elif side_out == "left":
            x_out, y_out = randint(1, rows - 2), 0
        else:
            x_out, y_out = randint(1, rows - 2), cols - 1
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits: List[Tuple[int, int]] = []
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "X":
                exits.append((i, j))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    rows = len(grid)
    cols = len(grid[0])
    new_grid = deepcopy(grid)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if grid[ni][nj] == " " or grid[ni][nj] == "X":
                            new_grid[ni][nj] = k + 1
                        elif grid[ni][nj] == 0:
                            new_grid[ni][nj] = k + 1

    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    if not exit_coord:
        return None

    if encircled_exit(grid, exit_coord):
        return exit_coord

    rows = len(grid)
    cols = len(grid[0])
    exit_x, exit_y = exit_coord

    wave_grid = deepcopy(grid)
    for i in range(rows):
        for j in range(cols):
            if isinstance(wave_grid[i][j], int):
                wave_grid[i][j] = " "

    wave_grid[exit_x][exit_y] = 1
    k = 1
    changed = True

    while changed:
        changed = False
        for i in range(rows):
            for j in range(cols):
                if isinstance(wave_grid[i][j], int) and wave_grid[i][j] == k:
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < rows and 0 <= nj < cols:
                            if wave_grid[ni][nj] == " ":
                                wave_grid[ni][nj] = k + 1
                                changed = True

        if changed:
            k += 1

    exits = get_exits(grid)
    if len(exits) < 2:
        return None

    start_exit = [e for e in exits if e != exit_coord][0]
    sx, sy = start_exit

    if not isinstance(wave_grid[sx][sy], int):
        return None

    path = [start_exit]
    current = start_exit

    while current != exit_coord:
        cx, cy = current
        current_value = wave_grid[cx][cy]
        if not isinstance(current_value, int):
            break

        found_next = False
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if isinstance(wave_grid[nx][ny], int) and wave_grid[nx][ny] == current_value - 1:
                    path.append((nx, ny))
                    current = (nx, ny)
                    found_next = True
                    break

        if not found_next:
            break

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == " ":
                return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    exits = get_exits(grid)

    if len(exits) != 2:
        return grid, None

    if any(encircled_exit(grid, exit_coord) for exit_coord in exits):
        return grid, None

    for exit_coord in exits:
        path = shortest_path(grid, exit_coord)
        if path and isinstance(path, list) and len(path) > 1:
            return grid, path

    return grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    if not path:
        return grid

    result_grid = deepcopy(grid)

    if isinstance(path, tuple):
        x, y = path
        result_grid[x][y] = "X"
    else:
        for i, (x, y) in enumerate(path):
            if i == 0 or i == len(path) - 1:
                result_grid[x][y] = "X"
            else:
                result_grid[x][y] = "•"

    return result_grid


if __name__ == "__main__":
    import pandas as pd  # type: ignore

    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
