from PIL import Image, ImageDraw
from os import getcwd, sep
from random import choice
import math

CELL = 0
WALL = 1
VISITED = -1
PASSED = 2
WRONG = -2

moves = [lambda x, y, dist: (x, y - dist), # left
		 lambda x, y, dist: (x + dist, y), # up
		 lambda x, y, dist: (x, y + dist), # right
		 lambda x, y, dist: (x - dist, y)  # down
		] 

HEIGHT = 121
WIDTH = 251
cell_width = 10

ENTER = (1, 1)
EXIT = (HEIGHT - 2, WIDTH - 2)


def get_frame() -> list:
	return [[CELL if i % 2 and j % 2 and 1 < i + 1 < HEIGHT and 1 < j + 1 < WIDTH else WALL for j in range(WIDTH)] for i in range(HEIGHT)]


def unvisited_exist(maze: list) -> bool:
	return any(maze[i][j] is not VISITED for i in range(1, HEIGHT, 2) for j in range(1, WIDTH, 2))


def get_neighbours(x: int, y: int, maze: list, distance: int) -> list:
	neigbours = []
	for move in moves:
		neigbour = move(x, y, distance)
		i, j = neigbour
		if 0 < i < HEIGHT - 1 and 0 < j < WIDTH - 1 and maze[i][j] is CELL:
			neigbours.append(neigbour)
	return neigbours


def get_unvisited(maze: list) -> list:
	return [(i, j) for i in range(1, HEIGHT, 2) for j in range(1, WIDTH, 2) if maze[i][j] is CELL]


def remove_wall(x1: int, y1: int, x2: int, y2: int, maze: list, filler):
    xDiff = x2 - x1
    yDiff = y2 - y1
    
    addX = xDiff // max(1, abs(xDiff))
    addY = yDiff // max(1, abs(yDiff))

    maze[x1 + addX][y1 + addY] = filler;


def manhattan_distance(turn: tuple) -> int:
	return abs(EXIT[0] - turn[0]) + abs(EXIT[1] - turn[1])


def best_turn(neighbours: list) -> tuple:
	return sorted(neighbours, key=manhattan_distance, reverse=True).pop()


def DFS_create() -> list:
	maze = get_frame()
	x, y = 1, 1
	maze[x][y] = VISITED
	stack = []

	while unvisited_exist(maze):
		Neighbours = get_neighbours(x, y, maze, 2)

		if Neighbours and (x, y) != EXIT:
			stack.append((x, y))
			next = choice(Neighbours)
			remove_wall(x, y, *next, maze, VISITED)
			x, y = next
			maze[x][y] = VISITED
		elif stack:
			x, y = stack.pop()
		else:
			x, y = choice(get_unvisited(maze))
			maze[x][y] = VISITED

	return [[CELL if maze[i][j] is VISITED else WALL for j in range(WIDTH)] for i in range(HEIGHT)]


def DFS_solve(maze: list) -> list:
	'''
	Находит выход из лабиринта, если такой существует
	Работает на осонове обхода в глубину за O(width / 2, height / 2)
	Для оптимизации применияется евристика манхетанского расстояния
	'''
	x, y = ENTER
	maze[x][y] = PASSED
	stack = []

	while (x, y) != EXIT:
		neighbours = get_neighbours(x, y, maze, 1)

		if neighbours:
			stack.append((x, y))
			x, y = best_turn(neighbours)
			maze[x][y] = PASSED
		elif stack:
			maze[x][y] = WRONG
			x, y = stack.pop()
		else:
			return None

	return maze


def draw(maze: list, filename: str) -> None:
	image = Image.new('RGB', (cell_width * WIDTH, cell_width * HEIGHT), "white")
	drawer = ImageDraw.Draw(image)

	for i in range(HEIGHT):
		for j in range(WIDTH):
			# Коодинаты левого верхнего угла текущей клетки
			x, y = j * cell_width, i * cell_width
			# Коодинаты правого нижнего угла текущей клетки
			z, t = x + cell_width, y + cell_width
			cell_coords = [x, y, z, t]

			if (i, j + 1) == ENTER or (i, j - 1) == EXIT:
				drawer.rectangle(cell_coords, fill="green")
			elif maze[i][j] is PASSED:
				drawer.rectangle(cell_coords, fill="red")
			elif maze[i][j] is WRONG:
				drawer.rectangle(cell_coords, fill="blue")
			elif maze[i][j] is WALL:
				drawer.rectangle(cell_coords, fill="black")
	
	image.show()
	image.save(filename + ".png")


maze = DFS_create()
draw(maze, 'maze')

way = DFS_solve(maze)
draw(way, 'way')
