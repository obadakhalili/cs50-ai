from math import inf


def minimax(state, maximizer_player, minimizer_player):
    def player_won(state):
        def strike_through(combo):
            x, y, z = combo
            return state[x] and state[x] == state[y] and state[y] == state[z]

        winning_combos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]

        return any(strike_through(combo) for combo in winning_combos)

    def no_empty_cells_left(state):
        return len([cell for cell in state if not cell]) == 0

    def possible_moves(state, player):
        def play_move(state, cellIdx):
            state[cellIdx] = player
            return state

        return [
            (play_move(state.copy(), idx), idx)
            for idx, cell in enumerate(state)
            if not cell
        ]

    alpha = -inf
    beta = inf

    def minimizer(state):
        nonlocal alpha

        if player_won(state):  # The agent has won
            return 1

        if no_empty_cells_left(state):
            return 0

        min_utility = inf

        for child_state, _ in possible_moves(state, minimizer_player):
            max_utility, _ = maximizer(child_state)

            if max_utility < alpha:
                return max_utility

            min_utility = min(min_utility, max_utility)

        alpha = min_utility

        return min_utility

    def maximizer(state):
        nonlocal beta

        move = None

        if player_won(state):  # The adversary has won
            return -1, move

        if no_empty_cells_left(state):  # It's a tie
            return 0, move

        max_utility = -inf

        for child_state, action in possible_moves(state, maximizer_player):
            min_utility = minimizer(child_state)

            if min_utility > beta:
                return min_utility, action

            if min_utility > max_utility:
                max_utility = min_utility
                move = action

        beta = max_utility

        return max_utility, move

    _, move = maximizer(state)
    return move


move = minimax(
    # fmt: off
    state=[
        "", "", "",
        "", "", "",
        "", "", ""
    ],
    # fmt: on
    maximizer_player="X",
    minimizer_player="O",
)

if move is not None:
    print(move, (move // 3, move % 3))
else:
    print("No move can be made")
