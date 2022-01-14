from logic import Self, Not, And, XOr, Implification, model_checking

if __name__ == "__main__":
    try:
        P = "It rained today"
        Q = "Harry visited Hagrid"
        R = "Harry visited Dumbledore"

        KB = And(
            Implification(Not(P), Q),
            XOr(Q, R),
        )
        KB.add(R)

        if model_checking(KB, Self(P)):
            print(P)
    except RuntimeError as e:
        print(e)
