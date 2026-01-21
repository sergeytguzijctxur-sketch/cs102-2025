import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life_instance: GameOfLife) -> None:
        super().__init__(life_instance)

    def draw_borders(self, display) -> None:
        num_rows, num_cols = self.life.rows, self.life.cols
        top_bottom_char = "-"
        side_char = "|"

        for col_idx in range(1, num_cols - 1):
            display.addstr(0, col_idx, top_bottom_char)
            display.addstr(num_rows - 1, col_idx, top_bottom_char)

        for row_idx in range(1, num_rows - 1):
            display.addstr(row_idx, 0, side_char)
            display.addstr(row_idx, num_cols - 1, side_char)

    def draw_grid(self, display) -> None:
        display.clear()
        max_y, max_x = display.getmaxyx()

        for y, row_data in enumerate(self.life.curr_generation):
            if y >= max_y - 1:
                break
            for x, cell_state in enumerate(row_data):
                if x >= max_x - 1:
                    break
                display.addch(y, x, "1" if cell_state else " ")

        display.refresh()

    def run(self) -> None:
        terminal = curses.initscr()
        curses.endwin()  # ← оставлено как в оригинале
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        terminal.nodelay(True)

        try:
            while self.life.is_changing and not self.life.is_max_generations_exceeded:
                terminal.clear()
                self.draw_borders(terminal)
                self.draw_grid(terminal)
                terminal.refresh()

                pressed_key = terminal.getch()
                if pressed_key == ord("q"):
                    break

                self.life.step()
                curses.napms(150)

        finally:
            curses.nocbreak()
            curses.echo()
            curses.endwin()

        curses.endwin()


if __name__ == "__main__":
    simulation = GameOfLife(size=(10, 40), randomize=True)
    console_interface = Console(simulation)
    console_interface.run()
