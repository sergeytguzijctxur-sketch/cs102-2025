import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        base_grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for r_idx in range(self.rows):
                for c_idx in range(self.cols):
                    base_grid[r_idx][c_idx] = random.randint(0, 1)
        return base_grid

    def get_neighbours(self, cell: Cell) -> Cells:
        current_row, current_col = cell
        neighbor_values = []

        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                neighbor_row = current_row + dr
                neighbor_col = current_col + dc

                if 0 <= neighbor_row < self.rows and 0 <= neighbor_col < self.cols:
                    neighbor_values.append(self.curr_generation[neighbor_row][neighbor_col])

        return neighbor_values

    def get_next_generation(self) -> Grid:
        next_gen = self.create_grid(randomize=False)

        for r in range(self.rows):
            for c in range(self.cols):
                live_count = sum(self.get_neighbours((r, c)))

                if self.curr_generation[r][c] == 1:
                    next_gen[r][c] = 1 if live_count in (2, 3) else 0
                else:
                    next_gen[r][c] = 1 if live_count == 3 else 0

        return next_gen

    def step(self) -> None:
        self.prev_generation = [row[:] for row in self.curr_generation]
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.max_generations is None:
            raise ValueError("Maximum generations limit is not set")
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filepath: pathlib.Path) -> "GameOfLife":
        grid_data = []
        with open(filepath, "r") as file_handle:
            for line in file_handle:
                cleaned_line = line.strip()
                if cleaned_line:
                    grid_data.append([int(ch) for ch in cleaned_line.split()])
        height, width = len(grid_data), len(grid_data[0]) if grid_data else 0
        instance = GameOfLife((height, width), randomize=False)
        instance.curr_generation = grid_data
        return instance

    def save(self, filepath: pathlib.Path) -> None:
        with open(filepath, "w") as output_file:
            for row in self.curr_generation:
                output_file.write(" ".join(str(cell) for cell in row) + "\n")
