"""Графический интерфейс для симуляции 'Жизнь' с использованием Pygame."""

# pylint: disable=no-member

import pygame

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Класс для отображения игры 'Жизнь' в графическом окне."""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.paused = False

    def draw_lines(self) -> None:
        black = pygame.Color("black")
        line_thickness = 1
        for x_pos in range(0, self.width + 1, self.cell_size):
            pygame.draw.line(self.screen, black, (x_pos, 0), (x_pos, self.height), line_thickness)
        for y_pos in range(0, self.height + 1, self.cell_size):
            pygame.draw.line(self.screen, black, (0, y_pos), (self.width, y_pos), line_thickness)

    def draw_grid(self) -> None:
        for r in range(self.life.rows):
            for c in range(self.life.cols):
                cell_alive = self.life.curr_generation[r][c]
                fill_color = pygame.Color("green") if cell_alive else pygame.Color("white")
                rect_x = c * self.cell_size
                rect_y = r * self.cell_size
                pygame.draw.rect(self.screen, fill_color, (rect_x, rect_y, self.cell_size, self.cell_size))

    def run(self) -> None:
        clock = pygame.time.Clock()
        active = True

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        print(f"Пауза: {'включена' if self.paused else 'выключена'}")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.paused and event.button == 1:
                        mouse_x, mouse_y = event.pos
                        col_index = mouse_x // self.cell_size
                        row_index = mouse_y // self.cell_size
                        if 0 <= row_index < self.life.rows and 0 <= col_index < self.life.cols:
                            current_state = self.life.curr_generation[row_index][col_index]
                            self.life.curr_generation[row_index][col_index] = 1 - current_state
                            action = "оживили" if current_state == 0 else "убили"
                            print(f"{action.capitalize()} клетку ({row_index}, {col_index})")

            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()

            if not self.paused:
                self.life.step()
                if self.life.is_max_generations_exceeded:
                    print(f"Игра завершена: достигнуто максимальное число поколений ({self.life.max_generations})")
                    active = False
                elif not self.life.is_changing:
                    print("Игра завершена: конфигурация стабилизировалась.")
                    active = False

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
        print("Симуляция остановлена.")


if __name__ == "__main__":
    initial_game = GameOfLife(size=(50, 50))
    visual_interface = GUI(initial_game)
    visual_interface.run()
