import random

random.seed(10)


def hill_climb(problem, min_value=True):
    current_state = problem.init_state

    get_best_state, has_reached_optimal = (
        (
            min,
            lambda current_state_cost, candidate_state_cost: (
                current_state_cost <= candidate_state_cost
            ),
        )
        if min_value
        else (
            max,
            lambda current_state_cost, candidate_state_cost: (
                current_state_cost >= candidate_state_cost
            ),
        )
    )

    while True:
        neighbors = problem.get_state_neighbors(current_state)
        neighbors_cost = [
            (neighbor, problem.get_state_cost(neighbor)) for neighbor in neighbors
        ]
        candidate_state, candidate_state_cost = get_best_state(
            neighbors_cost, key=lambda x: x[1]
        )
        current_state_cost = problem.get_state_cost(current_state)

        if has_reached_optimal(current_state_cost, candidate_state_cost):
            return current_state, current_state_cost

        current_state = candidate_state


class HospitalProblem:
    def __init__(self, space_width, space_height, hospitals_count):
        self.space_width = space_width
        self.space_height = space_height
        self.init_state = [
            (
                random.randrange(0, self.space_width),
                random.randrange(0, self.space_height),
            )
            for _ in range(hospitals_count)
        ]
        self._houses_locations = []

    def add_house(self, house_location):
        self._houses_locations.append(house_location)

    def draw(self, hospitals_locations):
        canvas = [["\u2588"] * self.space_width for _ in range(self.space_height)]

        for house_location in self._houses_locations:
            x, y = house_location
            canvas[y][x] = "\u2302"

        for hospital_location in hospitals_locations:
            x, y = hospital_location
            canvas[y][x] = "+"

        print("\n".join(["".join(row) for row in canvas]))

    def get_state_neighbors(self, hospitals_locations):
        neighbors_states = []

        for hospital_location in hospitals_locations:
            x, y = hospital_location
            for neighbor in (
                candidate_location
                for candidate_location in (
                    (x - 1, y),  # left
                    (x + 1, y),  # right
                    (x, y - 1),  # up
                    (x, y + 1),  # down
                )
                if candidate_location
                not in [*self._houses_locations, *hospitals_locations]
                and candidate_location[0] in range(self.space_width)
                and candidate_location[1] in range(self.space_height)
            ):
                neighbor_state = hospitals_locations.copy()
                neighbor_state.remove(hospital_location)
                neighbor_state.append(neighbor)

                neighbors_states.append(neighbor_state)

        return neighbors_states

    def get_state_cost(self, hospitals_locations):
        return sum(
            min(
                abs(house_x - hospital_x) + abs(house_y - hospital_y)
                for hospital_x, hospital_y in hospitals_locations
            )
            for house_x, house_y in self._houses_locations
        )


hospital_problem = HospitalProblem(25, 15, 3)

for _ in range(10):
    hospital_problem.add_house(
        (
            random.randrange(0, hospital_problem.space_width),
            random.randrange(0, hospital_problem.space_height),
        ),
    )

hospitals_locations, cost = hill_climb(hospital_problem)

hospital_problem.draw(hospitals_locations)
print(f"Cost: {cost}")
