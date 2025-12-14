from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
        grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def bin_tree_maze(
        rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    if rows < 5 or cols < 5:
        rows, cols = max(5, rows), max(5, cols)

    grid = create_grid(rows, cols)
    empty_cells = []

    for x in range(1, rows - 1, 2):
        for y in range(1, cols - 1, 2):
            grid[x][y] = " "
            empty_cells.append((x, y))

    for x, y in empty_cells:
        directions = []

        if x - 1 > 0:
            directions.append((-1, 0))
        if y + 1 < cols - 1:
            directions.append((0, 1))

        if directions:
            dx, dy = choice(directions)
            grid = remove_wall(grid, (x + dx, y + dy))

    exits = []
    while len(exits) < 2:
        if random_exit:
            side = choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x, y = 0, randint(0, cols - 1)
            elif side == 'bottom':
                x, y = rows - 1, randint(0, cols - 1)
            elif side == 'left':
                x, y = randint(0, rows - 1), 0
            else:
                x, y = randint(0, rows - 1), cols - 1
        else:
            if len(exits) == 0:
                x, y = 0, cols - 2
            else:
                x, y = rows - 1, 1

        if (x, y) not in exits:
            grid[x][y] = "X"
            exits.append((x, y))

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    rows, cols = len(grid), len(grid[0])
    new_grid = deepcopy(grid)

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if grid[nx][ny] in [" ", "X"]:
                            new_grid[nx][ny] = k + 1

    return new_grid


def shortest_path(
        grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    if not exit_coord:
        return None

    rows, cols = len(grid), len(grid[0])
    exits = get_exits(grid)

    if len(exits) != 2:
        return None

    start = [e for e in exits if e != exit_coord][0]

    wave_grid = deepcopy(grid)
    for x in range(rows):
        for y in range(cols):
            if isinstance(wave_grid[x][y], int):
                wave_grid[x][y] = " "

    wave_grid[exit_coord[0]][exit_coord[1]] = 1

    step = 1
    while True:
        wave_grid = make_step(wave_grid, step)
        step += 1

        start_val = wave_grid[start[0]][start[1]]
        if isinstance(start_val, int) and start_val > 1:
            break

        all_done = True
        for x in range(rows):
            for y in range(cols):
                if wave_grid[x][y] == step:
                    all_done = False
                    break
            if not all_done:
                break

        if all_done:
            break

    if not isinstance(wave_grid[start[0]][start[1]], int):
        return None

    path = [start]
    current = start

    while current != exit_coord:
        x, y = current
        current_val = wave_grid[x][y]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if isinstance(wave_grid[nx][ny], int) and wave_grid[nx][ny] == current_val - 1:
                    path.append((nx, ny))
                    current = (nx, ny)
                    break

    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    rows, cols = len(grid), len(grid[0])

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

    for exit_coord in exits:
        if not encircled_exit(grid, exit_coord):
            path = shortest_path(grid, exit_coord)
            if path and isinstance(path, list) and len(path) > 0:
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
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            result_grid[x][y] = "X"
    elif isinstance(path, list):
        for i, (x, y) in enumerate(path):
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
                result_grid[x][y] = "X"

    return result_grid


def create_solvable_maze(rows: int = 15, cols: int = 15, max_attempts: int = 10) -> List[List[Union[str, int]]]:
    """Создает лабиринт с гарантированным путем от входа к выходу"""
    for attempt in range(max_attempts):
        grid = bin_tree_maze(rows, cols, random_exit=True)
        _, path = solve_maze(grid)
        if path and isinstance(path, list) and len(path) > 1:
            return grid

    grid = create_grid(rows, cols)

    for y in range(1, cols - 1):
        grid[rows // 2][y] = " "

    grid[rows // 2][0] = "X"
    grid[rows // 2][cols - 1] = "X"

    return grid


if __name__ == "__main__":
    import pandas as pd

    GRID = create_solvable_maze(15, 15)
    print("Generated maze:")
    print(pd.DataFrame(GRID))

    _, PATH = solve_maze(GRID)
    print("\nPath:", PATH)

    if PATH:
        MAZE = add_path_to_grid(GRID, PATH)
        print("\nMaze with path:")
        print(pd.DataFrame(MAZE))
    else:
        print("\nNo path found!")