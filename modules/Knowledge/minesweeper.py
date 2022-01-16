from random import randrange


class Game:
    def __init__(self, width=8, height=8, mines_count=10):
        if mines_count > width * height:
            raise ValueError(
                "`mines_count` can't be more than the total number of cells"
            )

        self.mines = []

        while len(self.mines) < mines_count:
            mine = (randrange(0, height), randrange(0, width))
            if mine not in self.mines:
                self.mines.append(mine)

        self.unrevealed_safes_count = width * height - len(self.mines)
        self.width = width
        self.height = height

    def neighbours(self, cell):
        row, col = cell

        return set(
            filter(
                lambda state: not (
                    state[0] < 0
                    or state[0] >= self.height
                    or state[1] < 0
                    or state[1] >= self.width
                ),
                [
                    (row - 1, col),  # up
                    (row, col + 1),  # right
                    (row + 1, col),  # down
                    (row, col - 1),  # left
                    (row - 1, col - 1),  # up left
                    (row - 1, col + 1),  # up right
                    (row + 1, col - 1),  # down left
                    (row + 1, col + 1),  # down right
                ],
            )
        )

    def play_move(self, cell):
        # if input("Is mine? (y/n) ") == "y":
        if cell in self.mines:
            raise ValueError("cell is a mine")

        self.unrevealed_safes_count -= 1

        if self.unrevealed_safes_count:
            neighbours = self.neighbours(cell)
            # return (neighbours, len(set(neighbours).intersection([(1, 2), (2, 1)])))
            return (neighbours, len(set(neighbours).intersection(self.mines)))


class AI:
    def __init__(self, width, height, safes=[], mines=[]):
        self.width = width
        self.height = height
        self.safes = safes
        self.mines = mines
        self.revealed = []
        self.maybes = []

    def extend_knowledge(self, cell, neighbours, neighbouring_mines_count):
        def extend_safes(safes):
            self.safes.extend(safes)
            for maybe in self.maybes:
                for safe in safes:
                    if safe in maybe[0]:
                        maybe[0].remove(safe)
                        if len(maybe[0]) == maybe[1]:
                            self.maybes.remove(maybe)
                            extend_mines(maybe[0])

        def extend_mines(mines):
            self.mines.extend(mines)
            for idx, maybe in enumerate(self.maybes):
                for mine in mines:
                    if mine in maybe[0]:
                        maybe[0].remove(mine)
                        self.maybes[idx] = [maybe[0], maybe[1] - 1]
                        if maybe[1] == 0:
                            self.maybes.remove(maybe)
                            extend_safes(maybe[0])

        self.revealed.append(cell)

        if neighbouring_mines_count == 0:
            extend_safes(neighbours)
        elif neighbouring_mines_count == len(neighbours):
            extend_mines(neighbours)
        else:
            for maybe in self.maybes:
                if neighbours.issubset(maybe[0]):
                    maybe[0] = maybe[0].difference(neighbours)
                    maybe[1] = maybe[1] - neighbouring_mines_count

            self.maybes.append(
                [
                    neighbours.difference(set(self.safes).union(self.mines)),
                    neighbouring_mines_count,
                ]
            )

    def play(self, reveal_cell):
        if self.safes:
            safe = self.safes.pop()
            return self.extend_knowledge(safe, *reveal_cell(safe))

        maybes_cells = {cell for maybe in self.maybes for cell in maybe[0]}

        for row in range(self.height):
            for col in range(self.width):
                arbitrary_cell = (row, col)
                if not (
                    arbitrary_cell in self.revealed
                    or arbitrary_cell in self.mines
                    or arbitrary_cell in maybes_cells
                ):
                    return self.extend_knowledge(arbitrary_cell, *reveal_cell(arbitrary_cell))

        maybe_cell_to_mine_probability_mapper = {
            list(maybe[0])[1]: len(maybe[0]) / maybe[1] for maybe in self.maybes
        }

        if maybe_cell_to_mine_probability_mapper:
            maybe_cell = min(
                maybe_cell_to_mine_probability_mapper,
                key=lambda cell: maybe_cell_to_mine_probability_mapper[cell],
            )
            return self.extend_knowledge(maybe_cell, *reveal_cell(maybe_cell))


if __name__ == "__main__":
    try:
        game = Game(3, 3, 2)
        ai = AI(game.width, game.height)

        def reveal_cell(cell):
            print(f"Played: {cell}")

            move_result = game.play_move(cell)

            if move_result:
                return move_result

            print("AI won")
            exit(0)

        while True:
            ai.play(reveal_cell)
    except ValueError as e:
        print(e)
