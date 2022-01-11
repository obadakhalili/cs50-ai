import re
from os import path
from termcolor import colored


def parse_IMDb(data_dir):
    if not path.isdir(data_dir):
        return

    actors_info = {}
    movies_info = {}

    def parse_actors(actors_csv):
        for line in actors_csv:
            try:
                actor_id, actor_name, actor_yob = re.match(
                    r'(.*),"(.*)",(\d{4})', line
                ).groups()

                actors_info[actor_id] = {
                    "movies_ids": [],
                    "name": actor_name,
                    "yob": actor_yob,
                }
            except Exception:
                pass

    def parse_movies(movies_csv):
        for line in movies_csv:
            try:
                movie_id, movie_name, movie_year = re.match(
                    r'(.*),"(.*)",(\d{4})', line
                ).groups()

                movies_info[movie_id] = {
                    "actors_ids": [],
                    "name": movie_name,
                    "year": movie_year,
                }
            except Exception:
                pass

    def parse_starring_relationships(starring_relationships):
        for line in starring_relationships:
            try:
                actor_id, movie_id = line.split(",")

                if actor_id in actors_info:
                    actors_info[actor_id]["movies_ids"].append(movie_id)

                if movie_id in movies_info:
                    movies_info[movie_id]["actors_ids"].append(actor_id)
            except Exception:
                pass

    parsers = {
        "actors.csv": parse_actors,
        "movies.csv": parse_movies,
        "stars.csv": parse_starring_relationships,
    }

    try:
        for filename in parsers.keys():
            with open(f"{data_dir}/{filename}") as buffer:
                parsers[filename](buffer.read().splitlines()[1:])
    except Exception:
        return

    return actors_info, movies_info


class Queue:
    def __init__(self, init_item):
        self.items = [init_item]

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not len(self.items):
            return

        first_item = self.items[0]
        self.items = self.items[1:]

        return first_item

    def is_not_empty(self):
        return len(self.items)


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        pass

    def resolve_path(self):
        path = [self.state]
        parent = self.parent

        while parent:
            path.insert(0, parent.state)
            parent = parent.parent

        return path


def BFS(initial_state, final_state, expand_state):
    frontier = Queue(Node(initial_state))
    explored = set()

    while frontier.is_not_empty():
        current_node = frontier.dequeue()

        if current_node.state == final_state:
            return current_node.resolve_path()

        explored.add(current_node.state)

        for child_state in expand_state(current_node.state):
            if child_state not in explored:
                frontier.enqueue(Node(child_state, current_node))


if __name__ == "__main__":
    IMDb = parse_IMDb("./IMDb/small")

    if not IMDb:
        print("Failed to parse IMDb")
        exit(1)

    actors_info, movies_info = IMDb
    actors_path = BFS(
        # TODO: generate actors ids from their names as input
        "102",
        "144",
        lambda current_actor_id: [
            actor_id
            for actor_movie_id in actors_info.get(current_actor_id, {"movies_ids": []})[
                "movies_ids"
            ]
            for actor_id in movies_info.get(actor_movie_id, {"actors_ids": []})[
                "actors_ids"
            ]
        ],
    )

    if not actors_path:
        print("There is no path between the two actors")
        exit(0)

    for actor_a, actor_b in zip(actors_path, actors_path[1:]):
        print(
            f'* {colored(actors_info[actor_a]["name"], "yellow")} and {colored(actors_info[actor_b]["name"], "yellow")} starred in:'  # noqa
        )

        shared_movies = set(actors_info[actor_a]["movies_ids"]).intersection(
            set(actors_info[actor_b]["movies_ids"])
        )

        for movie_id in shared_movies:
            print(
                f'\t- {movies_info[movie_id]["name"]}. {colored(movies_info[movie_id]["year"], "green")}'  # noqa
            )
