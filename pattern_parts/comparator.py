from abc import ABC, abstractmethod
from pattern_parts.pattern_part import PatternPart
from logs.log import print
from typing import TypeVar
comparator = TypeVar("comparator", bound="Comparator")

COMPARATORS_REPRS = {}
REVERSE_COMPARATORS = {}




class Comparator(PatternPart):
    def __init__(self, role_limit: int = None):
        self._role_limit = role_limit

    def role_limit(self):
        return self._role_limit

    @abstractmethod
    def comparison(self, number: int) -> bool:
        """
            Compares two numbers using the comparators rules
        """

    def __hash__(self) -> int:
        return hash(type(self))

    def __eq__(self, other):
        return type(self) == type(other)

    def __repr__(self) -> str:
        return f"{COMPARATORS_REPRS[type(self)]} {self._role_limit}"

    def simplify(self) -> comparator:
        return self

    def reverse(self) -> comparator:
        for comparator_class_1, comparator_class_2 in REVERSE_COMPARATORS.items():
            if comparator_class_1 == type(self):
                return comparator_class_2(self._role_limit).simplify()
            if comparator_class_2 == type(self):
                return comparator_class_1(self._role_limit).simplify()

    
