from termcolor import colored
from logic import Self, Not, And, Or, XOr, Implication, model_checking

AKnight = "A is a Knight"
AKnave = "A is a Knave"

BKnight = "B is a Knight"
BKnave = "B is a Knave"

CKnight = "C is a Knight"
CKnave = "C is a Knave"

# Puzzle 0
# A says "I am both a knight and a knave."
KB_0 = And(
    XOr(AKnight, AKnave),
    Implication(AKnight, And(AKnight, AKnave)),
).add(Implication(AKnave, Not(And(AKnight, AKnave))))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
KB_1 = (
    And(
        XOr(AKnight, AKnave),
        XOr(BKnight, BKnave),
    )
    .add(Implication(AKnight, And(AKnave, BKnave)))
    .add(Implication(AKnave, Not(And(AKnave, BKnave))))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
KB_2 = (
    And(
        XOr(AKnight, AKnave),
        XOr(BKnight, BKnave),
    )
    .add(Implication(AKnight, XOr(And(AKnight, BKnight), And(AKnave, BKnave))))
    .add(Implication(AKnave, Not(XOr(And(AKnight, BKnight), And(AKnave, BKnave)))))
    .add(Implication(BKnight, XOr(And(AKnight, BKnave), And(AKnave, BKnight))))
    .add(Implication(BKnave, Not(XOr(And(AKnight, BKnave), And(AKnave, BKnight)))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
KB_3 = (
    And(
        XOr(AKnight, AKnave),
        XOr(BKnight, BKnave),
    )
    .add(XOr(CKnight, CKnave))
    .add(Implication(AKnight, Or(AKnight, AKnave)))
    .add(Implication(AKnave, Not(Or(AKnight, AKnave))))
    .add(Implication(BKnight, AKnave))
    .add(Implication(BKnave, Not(AKnave)))
    .add(Implication(BKnight, CKnave))
    .add(Implication(BKnave, Not(CKnave)))
    .add(Implication(CKnight, AKnight))
    .add(Implication(CKnave, Not(AKnight)))
)


if __name__ == "__main__":
    for idx, KB in enumerate([KB_0, KB_1, KB_2, KB_3]):
        print(colored(f"Puzzle {idx}", "yellow"))
        for symbol in KB.symbols():
            if model_checking(KB, Self(symbol)):
                print(
                    "\t* " + colored(symbol, "green" if "Knight" in symbol else "red")
                )
