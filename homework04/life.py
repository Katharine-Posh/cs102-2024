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
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        _grid = []
        for i in range(self.rows):
            a = []
            for j in range(self.cols):
                if randomize:
                    a.append(random.randint(0, 1))
                else:
                    a.append(0)

            _grid.append(a)

        return _grid

    def get_neighbours(self, cell: Cell) -> Cells:
        grid = self.curr_generation
        neighbours = []

        for dx in [-1, 0, 1]:  # Смещения по x
            for dy in [-1, 0, 1]:  # Смещения по y
                if dx == 0 and dy == 0:
                    continue  # Пропустить саму клетку
                r, c = cell[0] + dx, cell[1] + dy
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbours.append(self.curr_generation[r][c])

        return neighbours

    def get_next_generation(self) -> Grid:
        self.prev_generation = self.curr_generation

        grid = self.curr_generation
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
        pass

    def step(self) -> None:
        self.curr_generation = self.get_next_generation()
        self.generations += 1


    @property
    def is_max_generations_exceeded(self) -> bool:
        if self.generations >= self.max_generations:
            return True


    @property
    def is_changing(self) -> bool:
        if self.curr_generation != self.prev_generation:
            return True
        else:
            return False


    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r", encoding="utf-8") as save_file:
            lines = save_file.readlines()
            pattern = [[int(cell) for cell in line.strip()] for line in lines if line.strip()]

            game = GameOfLife((len(pattern), len(pattern[0])), randomize=False)
            game.curr_generation = pattern
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w+", encoding="utf-8") as save_file:
            save_file.writelines("".join(map(lambda e: str(int(e)), line)) + "\n" for line in self.curr_generation)
