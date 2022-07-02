from termcolor import colored

import sys
from functools import reduce

import backtracking


class Variable:
    def __init__(self, starting_row, starting_col, direction, length):
        self.starting_row = starting_row
        self.starting_col = starting_col
        self.direction = direction
        self.length = length

    def __repr__(self):
        return f"({self.starting_row}, {self.starting_col}, {self.direction}, {self.length})"  # noqa


""" Possible #TODOs (refer to course website for the theory behind the following):
- Implement AC3 for enforcing arc-consistency.
- Implement least constraining value heuristic.
- Implement minimum remaining value heuristic.
"""


class CrosswordCSP:
    def __init__(self, serialized_structure, words_list):
        self.serialized_structure = serialized_structure

        empty_squares = [
            (row, col)
            for row, line in enumerate(self.serialized_structure.splitlines())
            for col, char in enumerate(line)
            if char == "_"
        ]

        def accumulate_vars(is_square_in_var, direction):
            def accumulator(vars, square):
                var = next(
                    filter(
                        lambda var: is_square_in_var(var, square),
                        vars,
                    ),
                    None,
                )

                if var:
                    var.length += 1
                else:
                    vars.append(Variable(square[0], square[1], direction, 1))

                return vars

            return accumulator

        self.vars = [
            var
            for var in [
                *reduce(
                    accumulate_vars(
                        lambda var, square: (
                            square[0] == var.starting_row
                            and square[1] == var.starting_col + var.length
                        ),
                        "across",
                    ),
                    empty_squares,
                    [],
                ),
                *reduce(
                    accumulate_vars(
                        lambda var, square: (
                            square[1] == var.starting_col
                            and square[0] == var.starting_row + var.length
                        ),
                        "down",
                    ),
                    sorted(empty_squares, key=lambda square: square[1]),
                    [],
                ),
            ]
            if var.length > 1
        ]

        # Enforcing node-consistency here
        self.vars_domains = {
            var: [word for word in words_list if len(word) == var.length]
            for var in self.vars
        }

    def get_var_domain(self, var):
        return self.vars_domains[var]

    def is_assignment_consistent(self, var, value, assignments):
        return all(
            value[overlap_indexes[0]] == assignments[neighbor][overlap_indexes[1]]
            for neighbor, overlap_indexes in self.get_var_neighbors(var)
            if neighbor in assignments
        )

    def get_var_squares(self, var):
        var_direction_is_down = var.direction == "down"
        return [
            (
                var.starting_row + var_direction_is_down * i,
                var.starting_col + (not var_direction_is_down) * i,
            )
            for i in range(var.length)
        ]

    def get_var_neighbors(self, var):
        var_squares = self.get_var_squares(var)
        neighbors = []

        for candidate_neighbor_var in self.vars:
            if candidate_neighbor_var != var:
                candidate_neighbor_var_squares = self.get_var_squares(
                    candidate_neighbor_var
                )
                [intersection_square] = set(
                    candidate_neighbor_var_squares
                ).intersection(var_squares) or [None]
                if intersection_square:
                    neighbors.append(
                        (
                            candidate_neighbor_var,
                            (
                                var_squares.index(intersection_square),
                                candidate_neighbor_var_squares.index(
                                    intersection_square
                                ),
                            ),
                        )
                    )

        return neighbors

    def draw(self, assignments):
        structure = [
            [char for char in line] for line in self.serialized_structure.splitlines()
        ]

        for var, value in assignments.items():
            var_squares = self.get_var_squares(var)

            for value_index, square in enumerate(var_squares):
                structure[square[0]][square[1]] = value[value_index]

        print(
            "\n".join(
                [
                    "".join(
                        [
                            colored(" ", None, "on_grey")
                            if char == "#"
                            else colored(
                                char,
                                "grey",
                                "on_white",
                            )
                            for char in row
                        ]
                    )
                    for row in structure
                ]
            )
        )


if len(sys.argv) != 3:
    sys.exit("Usage: python crossword.py structure words")

[_, structure_file_path, words_file_path] = sys.argv

with open(structure_file_path) as structure_file:
    with open(words_file_path) as words_file:
        try:
            csp = CrosswordCSP(structure_file.read(), words_file.read().splitlines())
            assignments = backtracking.backtrack(csp)
            csp.draw(assignments)
        except backtracking.SolutionDNE as e:
            print(e)
