"""
Графический интерфейс для игры "Жизнь" Конвея на Pygame.
Предоставляет визуализацию, интерактивное управление и различные режимы отображения.
"""

import random
from pathlib import Path

import pygame
from pygame import KEYDOWN, MOUSEBUTTONDOWN, QUIT, K_l, K_p, K_q, K_r, K_s

from life import GameOfLife
from ui import UI


class GUI(UI):  # pylint: disable=too-many-instance-attributes
    """
    Графический интерфейс для игры "Жизнь".

    Атрибуты:
        cell_size: Размер ячейки в пикселях
        width: Ширина экрана в пикселях
        height: Высота экрана в пикселях
        screen: Поверхность отображения Pygame
        speed: Скорость игры (кадров в секунду)
        paused: Приостановлена ли симуляция
        random_color: Использовать случайные цвета
    """

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size

        self.width = self.cell_size * self.life.rows
        self.height = self.cell_size * self.life.cols
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        self.cell_width = life.rows
        self.cell_height = life.cols

        self.speed = speed
        self.paused = False
        self.random_color = False

    def draw_lines(self) -> None:
        """Отрисовка сетки на экране."""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self, color="purple") -> None:
        """
        Отрисовка игрового поля.

        Args:
            color: Цвет живых клеток (по умолчанию фиолетовый)
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                x = col * self.cell_size
                y = row * self.cell_size
                if self.life.curr_generation[row][col] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color(color),
                        (x, y, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (x, y, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:  # pylint: disable=too-many-branches
        """Основной цикл игры и обработка событий."""
        pygame.init()  # pylint: disable=no-member
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        running = False
                    elif event.key == K_p:
                        self.paused = not self.paused
                    elif event.key == K_s:
                        self.life.save(Path("save.txt"))
                    elif event.key == K_l:
                        self.life = GameOfLife.from_file(Path("save.txt"))
                    elif event.key == K_r:
                        self.random_color = not self.random_color
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 and self.paused:
                        x, y = event.pos
                        row = y // self.cell_size
                        col = x // self.cell_size
                        self.life.curr_generation[row][col] = 1 - self.life.curr_generation[row][col]

            self.draw_lines()

            if self.random_color:
                self.draw_grid(
                    color=(
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                )
            else:
                self.draw_grid()

            if not self.paused:
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    game = GameOfLife(size=(100, 100))
    gui = GUI(game)
    gui.run()
