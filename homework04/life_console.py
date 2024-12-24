import curses
from life import GameOfLife
from ui import UI
import time


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border(0)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        grid = self.life.curr_generation
        height, width = screen.getmaxyx()

        for i in range(min(len(grid), height - 2)):  # Учитываем границы
            for j in range(min(len(grid[i]), width - 2)):
                if grid[i][j] == 1:
                    screen.addch(i + 1, j + 1, '█')  # Живая клетка
                else:
                    screen.addch(i + 1, j + 1, ' ')  # Мертвая клетка

    def run(self) -> None:
        curses.initscr()
        curses.curs_set(0)  # Скрыть курсор
        screen = curses.newwin(20, 60, 0, 0)  # Создание нового окна с размером
        screen.timeout(100)  # Таймаут для ожидания ввода

        self.draw_borders(screen)

        running = True
        while running:
            self.draw_grid(screen)
            screen.refresh()

            self.life.step()  # Выполняем один шаг игры

            if self.life.is_max_generations_exceeded or not self.life.is_changing:
                running = False

            time.sleep(0.5)  # Задержка для замедления игры

        curses.endwin()
        print("Game Over")


if __name__ == "__main__":
    game = Console(life=GameOfLife((20, 60), randomize=True))
    game.run()
