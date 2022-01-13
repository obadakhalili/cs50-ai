from logic import Self, Not, And, Or, XOr, Implification, model_checking

if __name__ == "__main__":
    try:
        characters = ["Gilderoy", "Minerva", "Pomona", "Horace"]
        houses = ["Gryffindor", "Hufflepuff", "Ravenclaw", "Slytherin"]

        symbols = {
            character: {house: f"{character} belongs to {house}" for house in houses}
            for character in characters
        }

        KB = And()

        """
        Gilderoy, Minerva, Pomona and Horace each belong
        to a different one of the four houses: Gryffindor,
        Hufflepuff, Ravenclaw, and Slytherin House.
        """
        for character_i in symbols:
            one_house_each = XOr()

            for house in symbols[character_i]:
                one_house_each.add(symbols[character_i][house])

                if_char_in_house = Implification(symbols[character_i][house])
                chars_not_in_house = And()

                for character_j in symbols:
                    if character_j != character_i:
                        chars_not_in_house.add(Not(symbols[character_j][house]))

                KB.add(if_char_in_house.add(chars_not_in_house))

            KB.add(one_house_each)

        """
        Gilderoy belongs to Gryffindor or Ravenclaw
        """
        KB.add(Or(symbols["Gilderoy"]["Gryffindor"], symbols["Gilderoy"]["Ravenclaw"]))

        """
        Pomona does not belong in Slytherin.
        """
        KB.add(Not(symbols["Pomona"]["Slytherin"]))

        """
        Minerva belongs to Gryffindor.
        """
        KB.add(symbols["Minerva"]["Gryffindor"])

        for character in symbols:
            for house in symbols[character]:
                if model_checking(KB, Self(symbols[character][house])):
                    print(symbols[character][house])
    except RuntimeError as e:
        print(e)
