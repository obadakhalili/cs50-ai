from random import randrange


class GameOver(Exception):
    pass


class Game:
    def __init__(self, width=10, height=10, mines_count=10):
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
        if cell in self.mines:
            raise GameOver()

        self.unrevealed_safes_count -= 1

        if self.unrevealed_safes_count:
            neighbours = self.neighbours(cell)
            return (neighbours, len(set(neighbours).intersection(self.mines)))


class AI:
    def __init__(self, width, height, safes=None, mines=None):
        self.width = width
        self.height = height
        self.safes = safes or set()
        self.mines = mines or set()
        self.revealed = []
        self.maybes = []

    def extend_knowledge(self, cell, neighbours, neighbouring_mines_count):
        def extend_safes(safes, is_not_played=True):
            if is_not_played:
                self.safes.update(safes)

            for maybe in self.maybes:
                for safe in safes:
                    if safe in maybe[0]:
                        maybe[0].remove(safe)
                        if len(maybe[0]) == maybe[1]:
                            self.maybes.remove(maybe)
                            extend_mines(maybe[0])

        def extend_mines(mines):
            self.mines.update(mines)
            for maybe in self.maybes:
                for mine in mines:
                    if mine in maybe[0]:
                        maybe[0].remove(mine)
                        maybe[1] -= 1
                        if maybe[1] == 0:
                            self.maybes.remove(maybe)
                            extend_safes(maybe[0])

        self.revealed.append(cell)
        extend_safes([cell], is_not_played=False)

        if neighbouring_mines_count == 0:
            extend_safes(neighbours.difference(self.safes.union(self.revealed)))
        elif neighbouring_mines_count == len(neighbours):
            extend_mines(neighbours)
        else:
            for maybe in self.maybes:
                if neighbours.issubset(maybe[0]):
                    maybe[0] = maybe[0].difference(neighbours)
                    maybe[1] -= neighbouring_mines_count

                    if maybe[1] == 0:
                        self.maybes.remove(maybe)
                        extend_safes(maybe[0])
                    elif maybe[1] == len(maybe[0]):
                        extend_mines(maybe[0])
                elif maybe[0].issubset(neighbours):
                    neighbours = neighbours.difference(maybe[0])
                    neighbouring_mines_count -= maybe[1]

                    if neighbouring_mines_count == 0:
                        extend_safes(
                            neighbours.difference(self.safes.union(self.revealed))
                        )
                        return
                    elif neighbouring_mines_count == len(neighbours):
                        extend_mines(neighbours)
                        return

            neighbouring_mines_count -= len(neighbours.intersection(self.mines))
            maybes_cells = neighbours.difference(
                self.safes.union(self.mines).union(self.revealed)
            )

            if neighbouring_mines_count == 0:
                extend_safes(maybes_cells)
            elif neighbouring_mines_count == len(maybes_cells):
                extend_mines(maybes_cells)
            else:
                self.maybes.append([maybes_cells, neighbouring_mines_count])

    def play(self, reveal_cell):
        if self.safes:
            safe = self.safes.pop()
            move_result = reveal_cell(safe)

            if move_result:
                self.extend_knowledge(safe, *move_result)
                return move_result
            else:
                return

        maybes_cells = {cell for maybe in self.maybes for cell in maybe[0]}

        for row in range(self.height):
            for col in range(self.width):
                arbitrary_cell = (row, col)
                if not (
                    arbitrary_cell in self.revealed
                    or arbitrary_cell in self.mines
                    or arbitrary_cell in maybes_cells
                ):
                    move_result = reveal_cell(arbitrary_cell)

                    if move_result:
                        self.extend_knowledge(arbitrary_cell, *move_result)
                        return move_result
                    else:
                        return

        maybe_cell_to_mine_probability_mapper = [
            (list(maybe[0])[0], maybe[1] / len(maybe[0])) for maybe in self.maybes
        ]
        maybe_cell_to_mine_probability_mapper.sort(key=lambda x: x[1])
        maybe_cell_to_mine_probability_mapper = dict(
            maybe_cell_to_mine_probability_mapper
        )

        best_maybe_cell = min(
            maybe_cell_to_mine_probability_mapper,
            key=lambda cell: maybe_cell_to_mine_probability_mapper[cell],
        )
        move_result = reveal_cell(best_maybe_cell)

        if move_result:
            self.extend_knowledge(best_maybe_cell, *move_result)
            return move_result


if __name__ == "__main__":
    games_count = 1
    games_won = 0

    """ Win probability found by playing 100_000 games:
    * Difficulty beginner (10x10 board, 10 mines): 0.78064
    * Difficulty intermediate (16x16 board, 40 mines): 0.39985
    * Difficulty expert (30x16 board, 99 mines): 0.02333
    """

    for _ in range(games_count):
        try:
            game = Game()
            ai = AI(game.width, game.height)

            def reveal_cell(cell):
                print("Played:", cell)
                return game.play_move(cell)

            while True:
                last_move_result = ai.play(reveal_cell=reveal_cell)

                if not last_move_result:
                    print("AI won")
                    games_won += 1
                    break
        except GameOver:
            print("AI lost")
            pass

    print(f"Won {games_won}/{games_count} games ({games_won / games_count * 100}%)")
