from PIL import Image, ImageDraw
from os import getcwd, sep
from random import choice
import math

CELL, WALL = 0, 1
VISITED = -1
PASSED = 2
WRONG = -2

moves = [
lambda x, y, dist: (x, y - dist), # left
lambda x, y, dist: (x + dist, y), # up
lambda x, y, dist: (x, y + dist), # right
lambda x, y, dist: (x - dist, y)  # down
] 

HEIGHT = 20 + 1
WIDTH =  20 + 1
cell_width = 25

ENTER = (1, 1)
EXIT = (HEIGHT - 2, WIDTH - 2)


def get_frame() -> list:
    ''' Returns start frame for generating maze '''
    return [[CELL if i % 2 and j % 2 and 1 < i + 1 < HEIGHT and 1 < j + 1 < WIDTH else WALL for j in range(WIDTH)] for i in range(HEIGHT)]


def unvisited_exist(maze: list) -> bool:
    ''' Return true if any unvisited cell exists '''
    return any(maze[i][j] is not VISITED for i in range(1, HEIGHT, 2) for j in range(1, WIDTH, 2))


def get_neighbours(x: int, y: int, maze: list, distance: int) -> list:
    ''' Returns list of tuples coordinates of unvisited neighboring cells '''
    neigbours = []
    for (i, j) in [move(x, y, distance) for move in moves]:
        if 0 < i < HEIGHT - 1 and 0 < j < WIDTH - 1 and maze[i][j] is CELL:
            neigbours.append((i, j))
    return neigbours


def get_unvisited(maze: list) -> list:
    ''' Returns list of tuples of unvisited coordinates '''
    return [(i, j) for i in range(1, HEIGHT, 2) for j in range(1, WIDTH, 2) if maze[i][j] is CELL]


def remove_wall(x1: int, y1: int, x2: int, y2: int, maze: list, filler):
    ''' Remowes wall between neigbour coordinates '''
    xDiff = x2 - x1
    yDiff = y2 - y1
    
    addX = xDiff // max(1, abs(xDiff))
    addY = yDiff // max(1, abs(yDiff))

    maze[x1 + addX][y1 + addY] = filler


def manhattan_distance(turn: tuple) -> int:
    ''' Manhattan distance metrics '''
    return abs(EXIT[0] - turn[0]) + abs(EXIT[1] - turn[1])


def best_turn(neighbours: list) -> tuple:
    ''' Retuens best turn by min. manhattan distance from next cell to the exit'''
    return sorted(neighbours, key=manhattan_distance, reverse=True).pop()


def generate() -> list:
    '''
    Gerenates maze with one enter and exit
    Works using DFS algorithm in O (width * height)
    '''
    
    maze = get_frame()
    x, y = 1, 1
    maze[x][y] = VISITED
    stack = []

    while unvisited_exist(maze):
        Neighbours = get_neighbours(x, y, maze, 2)

        if Neighbours and (x, y) != EXIT: # If we can move to next neighbor cell
            stack.append((x, y))
            next_cell = choice(Neighbours)
            remove_wall(x, y, *next_cell, maze, VISITED)
            x, y = next_cell
            maze[x][y] = VISITED
        elif stack: # Come back, if we are at a dead end
            x, y = stack.pop()
        else: # If we can`t turn back and don`t have unvisited neighbours
            x, y = choice(get_unvisited(maze))
            maze[x][y] = VISITED

    return [[CELL if maze[i][j] is VISITED else WALL for j in range(WIDTH)] for i in range(HEIGHT)]


def solve(maze: list) -> list:
    '''
    Finds a way out of the maze, if such exist
    Works using DFS algorithm in O (width * height)
    Optimized by using manhattan distance metrics
    '''
    x, y = ENTER
    maze[x][y] = PASSED
    stack = list()

    while (x, y) != EXIT:
        neighbours = get_neighbours(x, y, maze, 1)

        if neighbours: # Move to next neighbour
            stack.append((x, y))
            x, y = best_turn(neighbours)
            maze[x][y] = PASSED
        elif stack: # Come back, if we are at a dead end
            maze[x][y] = WRONG
            x, y = stack.pop()
        else: # Incorrect maze
            return None

    return maze


def draw(maze: list, filename: str) -> None:
    image = Image.new('RGB', (cell_width * WIDTH, cell_width * HEIGHT), "white")
    drawer = ImageDraw.Draw(image)

    for i in range(HEIGHT):
        for j in range(WIDTH):
            x, y = j * cell_width, i * cell_width
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


maze = generate()
draw(maze, 'maze')

way = solve(maze)
draw(way, 'way')
