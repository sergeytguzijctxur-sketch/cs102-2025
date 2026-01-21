import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = (width, height)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = width // cell_size
        self.cell_height = height // cell_size
        self.speed = speed
        self.rows = self.cell_height
        self.cols = self.cell_width

    def draw_lines(self) -> None:
        black = pygame.Color("black")
        for x_coord in range(0, self.width + 1, self.cell_size):
            pygame.draw.line(self.screen, black, (x_coord, 0), (x_coord, self.height))
        for y_coord in range(0, self.height + 1, self.cell_size):
            pygame.draw.line(self.screen, black, (0, y_coord), (self.width, y_coord))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_lines()
            self.draw_grid()
            self.grid = self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        empty_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        if randomize:
            for r in range(self.rows):
                for c in range(self.cols):
                    empty_grid[r][c] = random.randint(0, 1)
        return empty_grid

    def draw_grid(self) -> None:
        for row_idx, row in enumerate(self.grid):
            for col_idx, is_alive in enumerate(row):
                cell_color = pygame.Color("green") if is_alive else pygame.Color("white")
                rect_area = pygame.Rect(
                    col_idx * self.cell_size, row_idx * self.cell_size, self.cell_size, self.cell_size
                )
                pygame.draw.rect(self.screen, cell_color, rect_area)

    def get_neighbours(self, cell: Cell) -> Cells:
        r, c = cell
        neighbor_list = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbor_list.append(self.grid[nr][nc])

        Returns
        ----------
        out : Cells
            Список соседних клеток, в котором каждая позиция – 0 или 1.
        """
        pass

    def get_next_generation(self) -> Grid:
        next_gen = self.create_grid(randomize=False)

        for i in range(self.rows):
            for j in range(self.cols):
                live_neighbors = sum(self.get_neighbours((i, j)))
                current = self.grid[i][j]

                if current == 1:
                    next_gen[i][j] = 1 if live_neighbors in (2, 3) else 0
                else:
                    next_gen[i][j] = 1 if live_neighbors == 3 else 0

        return next_gen
