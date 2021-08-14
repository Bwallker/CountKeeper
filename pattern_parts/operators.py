import inspect
import sys
from abc import abstractmethod
from types import ModuleType
from typing import TypeVar
from patterns.pattern_part import PatternPart
from logs.log import print
OPERATOR_MODULE = sys.modules[__name__]
OPERATORS_REPR = {}


class NoOpositeOperatorFoundError(Exception):
    """
        Exception raised if no oposite operator is found for an operator
    """


operator = TypeVar("operator", bound="Operator")


class Operator (PatternPart):
    def __init__(self):
        """

        """
    @abstractmethod
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
            Abstract method.
            applies the operator to two values and returns the result
        """

    @abstractmethod
    def get_reverse_operator(self) -> operator:
        """
            Abstract method.
            Returns the logical oposite of itself
            for example AndOperator returns NotAndOperator
        """

    def __str__(self):
        return OPERATORS_REPR[type(self)]

    def __repr__(self) -> str:
        return self.__str__()


class AndOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       0
            1           0       0
            0           1       0
            1           1       1
        """
        return value_1 and value_2

    def get_reverse_operator(self) -> operator:
        return NotAndOperator()

    def __repr__(self) -> str:
        return OPERATORS_REPR[type(self)]


class NotAndOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       1
            1           0       1
            0           1       1
            1           1       0
        """
        return not value_1 or not value_2

    def get_reverse_operator(self) -> operator:
        return AndOperator()


class OrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       0
            1           0       1
            0           1       1
            1           1       1
        """
        return value_1 or value_2

    def get_reverse_operator(self) -> operator:
        return NotOrOperator()


class NotOrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       1
            1           0       0
            0           1       0
            1           1       0
        """
        return not value_1 and not value_2

    def get_reverse_operator(self) -> operator:
        return OrOperator()


class ExclusiveOrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       0
            1           0       1
            0           1       1
            1           1       0
        """
        return value_1 ^ value_2

    def get_reverse_operator(self) -> operator:
        return NotExclusiveOrOperator()


class NotExclusiveOrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       1
            1           0       0
            0           1       0
            1           1       1
        """
        return not value_1 ^ value_2

    def get_reverse_operator(self) -> operator:
        return ExclusiveOrOperator()


OPERATORS_REPR = {
    AndOperator: "and",
    NotAndOperator: "not and",
    OrOperator: "inclusive or",
    NotOrOperator: "not inclusive or",
    ExclusiveOrOperator: "exclusive or",
    NotExclusiveOrOperator: "not exclusive or"

}
