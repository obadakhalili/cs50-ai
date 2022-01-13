from termcolor import colored
from logic import Self, Not, And, Or, model_checking

if __name__ == "__main__":
    try:
        mustard = "Mustard is the killer"
        plum = "Plum is the killer"
        scarlet = "Scarlet is the killer"

        ballroom = "The Ballroom is where the murder took place"
        kitchen = "The Kitchen is where the murder took place"
        library = "The Library is where the murder took place"

        knife = "The Knife is the weapen used for the murder"
        revolver = "The Revolver is the weapen used for the murder"
        wrench = "The Wrench is the weapen used for the murder"

        """
        Initially, one random card from each set is sealed in an envolope,
        and each player is given a card from each set,
        and the goal is to figure out the cards sealed in the envolope.
        We know that the following knowledge base is true.
        """
        KB = And(
            Or(mustard, plum).add(scarlet),
            Or(ballroom, kitchen).add(library),
        ).add(Or(knife, revolver).add(wrench))

        """Assume that I was given these cards"""
        KB.add(And(Not(mustard), Not(kitchen)).add(Not(revolver)))

        """
        Someone just made a guess: Scarlet, in the Library with the Wrench.
        One of mentioned cards is not in the envolope.
        """
        KB.add(Or(Not(scarlet), Not(library)).add(Not(wrench)))

        """Imagine that someone showed me Plum and the Ballroom cards"""
        KB.add(Not(plum)).add(Not(ballroom))

        for symbol in KB.symbols():
            if model_checking(KB, Self(symbol)):
                print(f"{symbol}: {colored(True, 'green')}")
            elif not model_checking(KB, Not(symbol)):
                print(f"{symbol}: {colored('Maybe', 'yellow')}")
    except RuntimeError as e:
        print(e)
