from dataclasses import dataclass, field
from patterns.simple_discord import SimpleGuild
from patterns.operators import *
from patterns.comparators import *
OPERATORS = {
    "and": AndOperator,
    "nand": NotAndOperator,
    "not and": NotAndOperator,
    "inclusive or": OrOperator,
    "or": OrOperator,
    "nor": NotOrOperator,
    "not or": NotOrOperator,
    "not inclusive or": NotOrOperator,
    "exclusive or": ExclusiveOrOperator,
    "xor": ExclusiveOrOperator,
    "nxor": NotExclusiveOrOperator,
    "not xor": NotExclusiveOrOperator,
    "not exclusive or": NotExclusiveOrOperator
}

COMPARATORS = {
    ">=": GreaterThanOrEqualToLimitComparator,
    ">": GreaterThanLimitComparator,
    "<=": LessThanOrEqualToLimitComparator,
    "<": LessThanLimitComparator,
    "=": EqualToLimitComparator,
    "==": EqualToLimitComparator,
    "!=)": NotEqualToLimitComparator,
    "=/=": NotEqualToLimitComparator
}


def create_operators():
    global OPERATORS
    return OPERATORS


def create_comparators():
    global COMPARATORS
    return COMPARATORS


def create_simple_guild():
    return SimpleGuild()


@dataclass
class PatternParams:

    pattern: str
    index_of_current_part: int = 0
    guild: SimpleGuild = field(default_factory=create_simple_guild)
    current_part: str = ""
    operators: dict[str, Operator] = field(default_factory=create_operators)
    comparators: dict[str, Comparator] = field(
        default_factory=create_comparators)
