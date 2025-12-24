import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, _ = pos
    return grid[row]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    _, col = pos
    return [grid[row][col] for row in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    row, col = pos
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3

    result = []
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            result.append(grid[i][j])

    return result


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row_vals = set(get_row(grid, pos))
    col_vals = set(get_col(grid, pos))
    block_vals = set(get_block(grid, pos))

    used = row_vals | col_vals | block_vals
    used.discard(".")

    return set("123456789") - used


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty_pos = find_empty_positions(grid)

    if not empty_pos:
        return grid

    row, col = empty_pos
    possible_values = find_possible_values(grid, (row, col))

    for value in possible_values:
        grid[row][col] = value
        solution = solve(grid)
        if solution:
            return solution
        grid[row][col] = "."

    return None


def check_solution(grid: tp.List[tp.List[str]]) -> bool:
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == ".":
                print("Solution is false (empty cell found)")
                return False

    for row in range(len(grid)):
        row_values = set()
        for col in range(len(grid[0])):
            value = grid[row][col]
            if value in row_values:
                print("Solution is false (duplicate in row)")
                return False
            row_values.add(value)

    for col in range(len(grid[0])):
        col_values = set()
        for row in range(len(grid)):
            value = grid[row][col]
            if value in col_values:
                print("Solution is false (duplicate in column)")
                return False
            col_values.add(value)

    for block_row in range(0, 9, 3):
        for block_col in range(0, 9, 3):
            block_values = set()
            for i in range(3):
                for j in range(3):
                    value = grid[block_row + i][block_col + j]
                    if value in block_values:
                        print("Solution is false (duplicate in block)")
                        return False
                    block_values.add(value)

    print("Solution is correct")
    return True


import random


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [["." for _ in range(9)] for _ in range(9)]

    solved = solve(grid)
    if not solved:
        return grid

    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)

    cells_to_remove = 81 - min(N, 81)

    for pos in positions[:cells_to_remove]:
        solved[pos[0]][pos[1]] = "."

    return solved


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
