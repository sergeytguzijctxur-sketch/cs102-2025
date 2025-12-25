"""GUI for displaying and solving a binary tree maze."""

import tkinter as tk
from copy import deepcopy
from tkinter import ttk
from typing import List, cast

from maze import bin_tree_maze, solve_maze


def draw_cell(canvas: tk.Canvas, x: int, y: int, color: str, size: int = 10) -> None:
    """Draw a single cell on the canvas."""
    x0 = x * size
    y0 = y * size
    x1 = x0 + size
    y1 = y0 + size
    canvas.create_rectangle(x0, y0, x1, y1, fill=color)


def draw_maze(canvas: tk.Canvas, grid: List[List[str]], size: int = 10) -> None:
    """Draw the entire maze grid on the canvas."""
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "white"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "purple"
            else:
                color = "gray"
            draw_cell(canvas, y, x, color, size)


def show_solution(canvas: tk.Canvas, grid: List[List[str]], n: int, m: int, cell_size: int) -> None:
    """Regenerate and display a solvable maze with solution path."""
    current_grid = deepcopy(grid)
    _, path = solve_maze(cast(List[List[str | int]], current_grid))

    while path is None:
        raw_maze = bin_tree_maze(n, m)
        grid = [[str(cell) for cell in row] for row in raw_maze]
        current_grid = deepcopy(grid)
        _, path = solve_maze(cast(List[List[str | int]], current_grid))

    if path is not None and isinstance(path, tuple):
        path = [path]

    maze_with_path = deepcopy(grid)
    if path:
        for i, j in path:
            maze_with_path[i][j] = "X"

    canvas.delete("all")
    draw_maze(canvas, maze_with_path, cell_size)


def main() -> None:
    """Main entry point for the maze GUI application."""
    N, M = 51, 77
    CELL_SIZE = 10

    raw_maze = bin_tree_maze(N, M)
    grid = [[str(cell) for cell in row] for row in raw_maze]

    window = tk.Tk()
    window.title("Maze")
    window.geometry(f"{M * CELL_SIZE + 100}x{N * CELL_SIZE + 100}")

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(canvas, grid, CELL_SIZE)

    ttk.Button(window, text="Solve", command=lambda: show_solution(canvas, grid, N, M, CELL_SIZE)).pack(pady=20)

    window.mainloop()


if __name__ == "__main__":
    main()
