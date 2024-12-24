"""Создание прототипа игры"""

import random
import typing as tp

import pygame
from pygame.locals import QUIT

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 20, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""

        pygame.init()  # pylint: disable=no-member
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        self.screen.fill(pygame.Color("white"))

        # Cоздание списка клеток
        self.grid = self.create_grid(True)
        self.draw_grid()

        running = True
        self.draw_lines()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()

            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()  # pylint: disable=no-member

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        _grid = []
        for _ in range(self.cell_width):
            a = []
            for _ in range(self.cell_height):
                if randomize:
                    a.append(random.randint(0, 1))
                else:
                    a.append(0)

            _grid.append(a)

        return _grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i, row in enumerate(self.grid):
            for j, value in enumerate(row):
                if value == 1:
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

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        neighbors = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                new_x = cell[0] + dx
                new_y = cell[1] + dy
                if 0 <= new_x < self.cell_width and 0 <= new_y < self.cell_height:
                    neighbors.append(self.grid[new_x][new_y])

        return neighbors

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        _grid = self.create_grid()

        for i in range(len(_grid)):
            for j in range(len(_grid[i])):
                count_of_neighbours = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 1:
                    if count_of_neighbours in (2, 3):
                        _grid[i][j] = 1
                    else:
                        _grid[i][j] = 0
                else:
                    if count_of_neighbours == 3:
                        _grid[i][j] = 1

        return _grid


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
