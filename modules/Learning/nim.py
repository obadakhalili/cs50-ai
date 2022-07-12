import itertools
import random
import termcolor


class NimInvalidMove(RuntimeError):
    def __init__(self):
        super().__init__()


class hash_list(list):
    def __init__(self, lst):
        super().__init__(lst)

    def copy(self):
        return hash_list([el for el in self])

    def __hash__(self):
        return hash(el for el in self)


class Nim:
    def __init__(self, init_piles):
        self.piles = hash_list(init_piles)

    def make_move(self, move):
        pile, objects = move

        if (
            pile not in range(len(self.piles))
            or objects > self.piles[pile]
            or objects < 0
        ):
            raise NimInvalidMove()

        self.piles[pile] -= objects

    def get_all_states(self):
        piles_states = [list(range(objects + 1)) for objects in self.piles]
        all_game_states = [
            hash_list(state)
            for state in itertools.product(*piles_states)
            if sum(state) > 1
        ]
        return all_game_states

    def get_state_actions(self, piles):
        return [
            action
            for pile, objects in enumerate(piles)
            if objects > 0
            for action in itertools.product([pile], range(1, objects + 1))
        ]

    def get_next_state(self, piles, move):
        pile, objects = move
        next_piles_state = piles.copy()
        next_piles_state[pile] -= objects

        return next_piles_state

    def is_game_over(self, piles):
        return sum(objects for objects in piles) <= 1

    def get_state_reward(self, piles):
        def is_winner_move(piles, move):
            pile, objects = move
            piles[pile] -= objects
            return self.is_game_over(piles)

        if self.is_game_over(piles):
            return 1
        elif any(
            is_winner_move(piles.copy(), move) for move in self.get_state_actions(piles)
        ):
            return -1

        return 0

    def play(self, agent=None):
        players_names = [
            input("Enter first player name: "),
            input(f"Enter {'agent' if agent else 'second player'} name: "),
        ]
        player_turn = int(
            input(
                f"Enter the code for the player which will go first, {players_names[0]} (0) or {players_names[1]} (1): "
            )
        )

        while not self.is_game_over(self.piles):
            for pile, objects in enumerate(reversed(self.piles)):
                print(
                    f"Pile {len(self.piles) - pile - 1}: {objects}    {termcolor.colored(objects * '*', 'blue')}"
                )

            next_move = (
                agent(self.piles)
                if agent and player_turn == 1
                else tuple(
                    int(value)
                    for value in input(f"{players_names[player_turn]}'s turn: ").split(
                        ", "
                    )
                )
            )

            print(f"Player {players_names[player_turn]} played {next_move}")

            try:
                self.make_move(next_move)
                player_turn = 0 if player_turn else 1
            except NimInvalidMove:
                print(f"Invalid move {next_move}. Try again")

        print(f"{players_names[0 if player_turn else 1]} won")


def q_learning(world, episodes_count, epsilon=0.2, alpha=0.5, gamma=0.5):
    Q = {
        state: {action: 0 for action in world.get_state_actions(state)}
        for state in world.get_all_states()
    }

    get_best_action = lambda state: max(Q[state], key=Q[state].get)

    for _ in range(episodes_count):
        current_state = random.choice(list(Q.keys()))

        while True:
            action = (
                random.choice(list(Q[current_state].keys()))
                if random.random() < epsilon
                else get_best_action(current_state)
            )
            next_state = world.get_next_state(current_state, action)
            next_state_reward = world.get_state_reward(next_state)
            is_terminal_state = next_state_reward != 0

            Q[current_state][action] = Q[current_state][action] + alpha * (
                (
                    next_state_reward
                    + (not is_terminal_state and gamma * max(Q[next_state].values()))
                )
                - Q[current_state][action]
            )

            if is_terminal_state:
                break

            current_state = next_state

    return get_best_action


nim = Nim([7, 5, 3, 1])
nim_agent = q_learning(nim, 10000)

nim.play(nim_agent)
