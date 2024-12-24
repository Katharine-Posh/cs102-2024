"""Версия игры с графическим интерфейсом"""

from pathlib import Path

import pygame
import pygame.locals

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Общая логика работы игры с графическим интерфейсом"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 5) -> None:
        super().__init__(life)
        self.cell_size = cell_size

        self.screen_size = life.cols * cell_size, life.rows * cell_size
        self.screen = pygame.display.set_mode(self.screen_size)

        self.speed = speed

    def draw_lines(self) -> None:
        """Создание линий - клетчатого поля"""
        for x in range(0, self.life.cols * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.life.rows * self.cell_size))
        for y in range(0, self.life.rows * self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.life.cols * self.cell_size, y))

    def draw_grid(self) -> None:
        """ "Закрашивание" клеток в соответствии с их состоянием (живая или нет)"""
        grid = self.life.curr_generation

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("purple"),
                        (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size),
                    )

    def run(self) -> None:
        pygame.init()  # pylint: disable=no-member
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.life.curr_generation = self.life.create_grid(randomize=True)

        running = True
        has_changes = True
        paused = False

        while running and has_changes:
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:  # pylint: disable=no-member
                    running = False
                if event.type == pygame.locals.KEYDOWN:  # pylint: disable=no-member
                    if event.key == pygame.locals.K_SPACE:  # pylint: disable=no-member
                        paused ^= True
                        print("Pause toggled")
                if event.type == pygame.locals.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                    if event.button == 1 and paused:
                        y, x = event.pos
                        x //= self.cell_size
                        y //= self.cell_size
                        self.life.curr_generation[y][x] ^= True
                        self.draw_grid()
                        self.draw_lines()
                        pygame.display.flip()

            if paused:
                continue

            self.life.step()
            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()
            # Выполнение одного шага игры (обновление состояния ячеек)

            # Проверка обновления ячеек
            has_changes = self.life.is_changing

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()  # pylint: disable=no-member
        print("Game Over")


if __name__ == "__main__":
    game = GUI(life=GameOfLife((50, 50)), speed=50, cell_size=15)
    game.run()
    game.life.save(Path("result.txt"))

    # Загрузка из файла

    # game = GameOfLife.from_file(Path('glider.txt'))
    # print(game.curr_generation)
    # for _ in range(4):
    #     game.step()
    # print(game.curr_generation)
