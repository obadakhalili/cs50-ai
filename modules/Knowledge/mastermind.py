from logic import Self, Not, And, Or, XOr, Implification, model_checking


def format_color_at_position(color, position):
    return f"{color} at {position}"


if __name__ == "__main__":
    try:
        colors = ["Red", "Green", "Blue", "Yellow"]

        KB = And()

        for color_i in colors:
            one_position_per_color = XOr()

            for position in range(len(colors)):
                one_position_per_color.add(format_color_at_position(color_i, position))

                one_color_per_position = Implification(
                    format_color_at_position(color_i, position)
                )
                colors_not_in_position = And()

                for color_j in colors:
                    if color_i != color_j:
                        colors_not_in_position.add(
                            Not(format_color_at_position(color_j, position))
                        )

                KB.add(one_color_per_position.add(colors_not_in_position))

            KB.add(one_position_per_color)

        """
        Imagine that my initial guess was: Red, Blue, Green, Yellow.
        And that I got 2 of the positions correct.
        """
        first_guess = ["Red", "Blue", "Green", "Yellow"]
        possible_correct_combinations = Or()

        for position_i, color_i in enumerate(first_guess):
            for position_j, color_j in enumerate(first_guess):
                if color_i != color_j:
                    possible_correct_combination = And(
                        format_color_at_position(color_i, position_i),
                        format_color_at_position(color_j, position_j),
                    )

                    for position_k, color_k in enumerate(first_guess):
                        if color_k not in [color_i, color_j]:
                            possible_correct_combination.add(
                                Not(format_color_at_position(color_k, position_k))
                            )

                    possible_correct_combinations.add(possible_correct_combination)

        KB.add(possible_correct_combinations)

        """
        After that I made the following guess: Blue, Red, Green, Yellow.
        And I got 0 of the positions correct.
        """
        KB.add(format_color_at_position("Red", 0))
        KB.add(format_color_at_position("Blue", 1))

        for symbol in KB.symbols():
            if model_checking(KB, Self(symbol)):
                print(symbol)
    except RuntimeError as e:
        print(e)
