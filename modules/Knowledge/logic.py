from functools import reduce
from itertools import product
from copy import copy


class LogicalConnective:
    def __init__(self, *operands):
        self.operands = operands

    def evaluate(self, model):
        try:
            return [
                model[operand] if isinstance(operand, str) else operand.evaluate(model)
                for operand in self.operands
            ]
        except KeyError as e:
            raise RuntimeError(f"can't find operand {e} in model")
        except AttributeError:
            raise RuntimeError("an operand is neither a symbol nor a LogicalConnective")

    def symbols(self):
        symbols = set()

        for operand in self.operands:
            if isinstance(operand, str):
                symbols.add(operand)
            elif isinstance(operand, LogicalConnective):
                symbols.update(operand.symbols())
            else:
                raise RuntimeError(
                    "an operand is neither a symbol nor a LogicalConnective"
                )

        return symbols


class UnaryLogicalConnective(LogicalConnective):
    def add(self, operand):
        if not self.operands:
            self.operands = (operand,)
        return self


class BinaryLogicalConnective(LogicalConnective):
    def add(self, operand):
        if len(self.operands) < 2:
            self.operands = self.operands + (operand,)
        else:
            self.operands = (copy(self), operand)
        return self


class Self(UnaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P] = super().evaluate(model)
            return P
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 1 operand")


class Not(UnaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P] = super().evaluate(model)
            return not P
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 1 operand")

    def add(self, operand):
        if not self.operands:
            self.operands = (operand,)
        return self


class And(BinaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P, Q] = super().evaluate(model)
            return P and Q
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 2 operands")


class Or(BinaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P, Q] = super().evaluate(model)
            return P or Q
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 2 operands")


class XOr(BinaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P, Q] = super().evaluate(model)
            return P != Q
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 2 operands")


class Implication(BinaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P, Q] = super().evaluate(model)
            return not P or Q
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 2 operands")


class BiImplication(BinaryLogicalConnective):
    def evaluate(self, model):
        try:
            [P, Q] = super().evaluate(model)
            return P == Q
        except ValueError:
            raise RuntimeError(f"'{self.__class__.__name__}' should take 2 operands")


def model_checking(KB, query):
    symbols = KB.symbols().union(query.symbols())
    possible_models = map(
        lambda combination: reduce(
            lambda model, symbol: {**model, symbol[1]: combination[symbol[0]]},
            enumerate(symbols),
            {},
        ),
        product([False, True], repeat=len(symbols)),
    )

    for model in possible_models:
        if KB.evaluate(model) and not query.evaluate(model):
            return False

    return True
