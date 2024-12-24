import random
import typing as tp

import pygame
from pygame.examples import grid
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]

grid: Grid = []


class GameOfLife:
    def __init__(
            self, width: int = 640, height: int = 480, cell_size: int = 20, speed: int = 10
    ) -> None:
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
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        global grid

        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")

        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        grid = self.create_grid(randomize=True)
        self.draw_grid()

        running = True
        self.draw_lines()

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Выполнение одного шага игры (обновление состояния ячеек)
            grid = self.get_next_generation()

            # Отрисовка списка клеток
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        _grid = []
        for i in range(self.cell_width):
            a = []
            for j in range(self.cell_height):
                if randomize:
                    a.append(random.randint(0, 1))
                else:
                    a.append(0)

            _grid.append(a)

        return _grid
        pass

    def draw_grid(self) -> None:
        global grid

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(self.screen, pygame.Color("purple"),
                             (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("white"),
                             (i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size))

        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbors = []

        for dx in [-1, 0, 1]:  # Смещения по x
            for dy in [-1, 0, 1]:  # Смещения по y
                if dx == 0 and dy == 0:
                    continue  # Пропустить саму клетку
                new_x = cell[0] + dx
                new_y = cell[1] + dy
                if 0 <= new_x < self.cell_width and 0 <= new_y < self.cell_height:
                    neighbors.append(grid[new_x][new_y])

        return neighbors

    def get_next_generation(self) -> Grid:
        global grid

        _grid = self.create_grid()

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                countOfNeighbours = sum(self.get_neighbours((i, j)))
                if grid[i][j] == 1:  # Если клетка живая
                    if countOfNeighbours == 2 or countOfNeighbours == 3:
                        _grid[i][j] = 1  # Клетка остается живой
                    else:
                        _grid[i][j] = 0  # Клетка умирает
                else:  # Если клетка мертвая
                    if countOfNeighbours == 3:
                        _grid[i][j] = 1  # Клетка становится живой

        return _grid


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
