from logic import Self, Not, And, Or, XOr, Implication, model_checking


def format_character_in_house(character, house):
    return f"{character} belongs to {house}"


if __name__ == "__main__":
    try:
        characters = ["Gilderoy", "Minerva", "Pomona", "Horace"]
        houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

        KB = And()

        """
        Gilderoy, Minerva, Pomona and Horace each belong
        to a different one of the four houses: Gryffindor,
        Hufflepuff, Ravenclaw, and Slytherin House.
        """
        for character_i in characters:
            one_house_per_char = XOr()

            for house in houses:
                one_house_per_char.add(format_character_in_house(character_i, house))

                one_char_per_house = Implication(
                    format_character_in_house(character_i, house)
                )
                chars_not_in_house = And()

                for character_j in characters:
                    if character_j != character_i:
                        chars_not_in_house.add(
                            Not(format_character_in_house(character_j, house))
                        )

                KB.add(one_char_per_house.add(chars_not_in_house))

            KB.add(one_house_per_char)

        """
        Gilderoy belongs to Gryffindor or Ravenclaw
        """
        KB.add(
            Or(
                format_character_in_house("Gilderoy", "Gryffindor"),
                format_character_in_house("Gilderoy", "Ravenclaw"),
            )
        )

        """
        Pomona does not belong in Slytherin.
        """
        KB.add(Not(format_character_in_house("Pomona", "Slytherin")))

        """
        Minerva belongs to Gryffindor.
        """
        KB.add(format_character_in_house("Minerva", "Gryffindor"))

        for symbol in KB.symbols():
            if model_checking(KB, Self(symbol)):
                print(symbol)
    except RuntimeError as e:
        print(e)
