import random
import tkinter as tk
from collections import deque
from tkinter import messagebox, ttk
from typing import List, Optional, Tuple


def generate_maze(n: int, m: int) -> List[List[str]]:
    """
    Генерирует идеальный лабиринт размером n x m с использованием DFS.
    Вход — (0, 1), выход — (n-1, m-2).
    Стены обозначаются '■', проходы — ' '.
    """
    if n % 2 == 0:
        n -= 1
    if m % 2 == 0:
        m -= 1

    grid = [["■" for _ in range(m)] for _ in range(n)]

    stack = [(1, 1)]
    grid[1][1] = " "

    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]

    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < n - 1 and 0 < ny < m - 1 and grid[nx][ny] == "■":
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            grid[(x + nx) // 2][(y + ny) // 2] = " "
            grid[nx][ny] = " "
            stack.append((nx, ny))
        else:
            stack.pop()

    grid[0][1] = " "
    grid[n - 1][m - 2] = " "

    return grid


def solve_maze(grid: List[List[str]]) -> Tuple[List[List[str]], List[Tuple[int, int]]]:
    """
    Возвращает (grid, path), где path — список координат от входа к выходу.
    Вход предполагается в (0,1), выход — (n-1, m-2).
    """
    n, m = len(grid), len(grid[0])
    start = (0, 1)
    end = (n - 1, m - 2)

    visited = [[False] * m for _ in range(n)]
    parent: dict[Tuple[int, int], Tuple[int, int]] = {}
    queue = deque([start])
    visited[start[0]][start[1]] = True

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            path = []
            while (x, y) != start:
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append(start)
            path.reverse()
            return grid, path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and grid[nx][ny] == " ":
                visited[nx][ny] = True
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return grid, []


def add_path_to_grid(grid: List[List[str]], path: List[Tuple[int, int]]) -> List[List[str]]:
    new_grid = [row[:] for row in grid]  # копия
    for x, y in path:
        if new_grid[x][y] not in ["■"]:  # не перезаписываем стены
            new_grid[x][y] = "X"
    return new_grid


def draw_cell(x, y, color, size: int = 10):
    x *= size
    y *= size
    x1 = x + size
    y1 = y + size
    canvas.create_rectangle(x, y, x1, y1, fill=color)


def draw_maze(grid: List[List[str]], size: int = 10):
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == " ":
                color = "White"
            elif cell == "■":
                color = "black"
            elif cell == "X":
                color = "blue"
            draw_cell(y, x, color, size)


def show_solution():
    maze, path = solve_maze(GRID)
    maze = add_path_to_grid(GRID, path)
    if path:
        draw_maze(maze, CELL_SIZE)
    else:
        tk.messagebox.showinfo("Message", "No solutions")


if __name__ == "__main__":
    global GRID, CELL_SIZE
    N, M = 51, 77

    CELL_SIZE = 10
    GRID = generate_maze(N, M)

    window = tk.Tk()
    window.title("Maze")
    window.geometry("%dx%d" % (M * CELL_SIZE + 100, N * CELL_SIZE + 100))

    canvas = tk.Canvas(window, width=M * CELL_SIZE, height=N * CELL_SIZE)
    canvas.pack()

    draw_maze(GRID, CELL_SIZE)
    ttk.Button(window, text="Solve", command=show_solution).pack(pady=20)

    window.mainloop()
