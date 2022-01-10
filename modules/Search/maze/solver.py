from enum import Enum
from functools import reduce


def read_file(dir):
    reader = open(dir)
    text = reader.read()
    reader.close()
    return text


class Stack:
    def __init__(self, init_item):
        self.items = [init_item]

    def add(self, item):
        self.items.append(item)

    def is_not_empty(self):
        return len(self.items)

    def remove(self):
        if not len(self.items):
            return

        last_item = self.items[-1]
        self.items = self.items[:-1]
        return last_item


class Queue(Stack):
    def remove(self):
        if not len(self.items):
            return

        first_item = self.items[0]
        self.items = self.items[1:]
        return first_item


class Maze:
    class Symbol(Enum):
        WALL = "#"
        START = "A"
        END = "B"
        EMPTY = " "

    class InvalidError(RuntimeError):
        def __init__(self, message):
            self.message = message

    class NoSolutionError(RuntimeError):
        def __init__(self):
            self.message = "maze has no solution"

    class Node:
        def __init__(self, state, parent):
            self.state = state
            self.parent = parent

    def __init__(self, serialized_maze):
        lines = serialized_maze.splitlines()

        self.serialized_maze = serialized_maze
        self.max_row = len(lines) - 1
        self.max_col = len(lines[0]) - 1 if lines else None
        self.walls_coords = []
        self.start_coords = None
        self.end_coords = None
        self.solution = None

        if self.max_col is None or any(
            len(line) - 1 is not self.max_col for line in lines
        ):
            raise self.InvalidError("invalid maze dimensions")

        for row, line in enumerate(lines):
            for col, symbol in enumerate(line):
                coords = (row, col)

                if symbol == self.Symbol.WALL.value:
                    self.walls_coords.append(coords)
                elif symbol == self.Symbol.START.value:
                    self.start_coords = coords
                elif symbol == self.Symbol.END.value:
                    self.end_coords = coords
                elif symbol != self.Symbol.EMPTY.value:
                    raise self.InvalidError(f"invalid symbol '{symbol}'")

        if not self.start_coords:
            raise self.InvalidError("maze should contain start position")

        if not self.end_coords:
            raise self.InvalidError("maze should contain end position")

    def solve(self, Frontier):
        def is_goal(state):
            return state == self.end_coords

        def resolve_path(node):
            path = []

            while node.parent:
                path.insert(0, node.state)
                node = node.parent

            return path

        def expand(state):
            row, col = state

            return list(
                filter(
                    lambda state: not (
                        state[0] < 0
                        or state[0] > self.max_row
                        or state[1] < 0
                        or state[1] > self.max_col
                        or state in self.walls_coords
                    ),
                    [
                        (row - 1, col),  # up
                        (row + 1, col),  # down
                        (row, col + 1),  # right
                        (row, col - 1),  # left
                    ],
                )
            )

        frontier = Frontier(self.Node(self.start_coords, None))
        explored = set()

        while frontier.is_not_empty():
            node = frontier.remove()

            if is_goal(node.state):
                self.solution = {
                    "path": resolve_path(node.parent),
                    "explored": explored,
                }
                return self.solution

            explored.add(node.state)

            for child_node in map(
                lambda state: self.Node(state, node), expand(node.state)
            ):
                if child_node.state not in explored:
                    frontier.add(child_node)

        raise self.NoSolutionError()

    def serialize_solution(self):
        if not self.solution:
            return

        def mapToIdx(coords):
            row, col = coords
            return row * (self.max_col + 2) + col

        def insert_path_symbol(maze, coords):
            maze[mapToIdx(coords)] = "*"
            return maze

        def insert_explored_symbol(maze, coords):
            if coords != self.start_coords and coords not in self.solution["path"]:
                maze[mapToIdx(coords)] = "."
            return maze

        path_track = reduce(
            insert_path_symbol,
            self.solution["path"],
            list(
                map(
                    lambda char: "\u2588" if char == self.Symbol.WALL.value else char,
                    list(self.serialized_maze),
                )
            ),
        )

        explored_track = reduce(
            insert_explored_symbol, self.solution["explored"], path_track.copy()
        )

        return {
            "path_track": "".join(path_track),
            "explored_track": "".join(explored_track),
        }


try:
    serialized_maze = read_file("./maps/2.txt")
    maze = Maze(serialized_maze)
    solution = maze.solve(Stack)
    serialized_solution = maze.serialize_solution()

    print(f'Path Track:\n\n{serialized_solution["path_track"]}\n')
    print(f'Explored Track:\n\n{serialized_solution["explored_track"]}\n')
    print("Explored Count:", len(solution["explored"]))
except FileNotFoundError:
    print("file not found")
except Maze.InvalidError as e:
    print(e.message)
except Maze.NoSolutionError as e:
    print(e.message)
