from typing import Optional, Union
from patterns.statement import Statement
from patterns.component import BooleanComponent, Component, NumberOfRolesLimitComponent, ReverseComponent, RoleComponent, SimpleComponent
from patterns.pattern_error import *
import discord
from discord.channel import VoiceChannel
from discord import Guild
from db import db
from utils import utils
from logs.log import print
from patterns.operators import Operator, AndOperator, OrOperator, NotAndOperator, NotOrOperator, ExclusiveOrOperator, NotExcluseOrOperator
# This file contains helper functions for updating the channels


operators = {
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
    "nxor": NotExcluseOrOperator,
    "not xor": NotExcluseOrOperator,
    "not exclusive or": NotExcluseOrOperator
}


async def update_channel(channel: VoiceChannel, role_number: int, guild: Guild):
    first_number = None
    words = channel.name.split()
    for i, word in enumerate(words):
        if word.isdigit():
            first_number = word
            words[i] = str(role_number)
            break
    words = " ".join(words)
    print(words)
    output = None
    if first_number is None:
        output = channel.name + str(role_number)
    else:
        output = words
    previous_name = channel.name
    try:
        await channel.edit(name=output)
        print(
            f"channel {previous_name} renamed to {channel.name} in guild {guild}")
    except discord.errors.Forbidden as e:
        print(
            f"discord Forbidden exception raised while trying to rename channel {previous_name} in guild {guild.name}")


def is_operator(parts: tuple[str], operators: dict[str, Operator]) -> tuple[Operator, int]:
    try:
        get_operator(parts, operators)
        return True
    except NotOperatorError:
        return False


def get_operator(parts: tuple[str], operators: dict[str, Operator]) -> Operator:
    """Returns the size of the operator in words and the operator"""
    if not isinstance(parts, tuple) and not isinstance(parts, list):
        raise ValueError(f"parts is type {type(parts)}")
    operator = parts[-1].strip()
    if operator in operators:
        return operators.get(operator)()
    index = 1
    while index < len(parts):
        next_operator = parts[index].strip()
        operator = next_operator + " " + operator
        if operator in operators:
            return operators.get(operator)()
        index += 1
    raise NotOperatorError(" ".join(parts))


def operator_constructor(operator: str, operators: dict[str, Operator]) -> Operator:
    if not isinstance(operator, str):
        raise ValueError(
            f"Operator is not a str, instead it is of type {type(operator)}")

    if operator in operators:
        return operators.get(operator)()
    raise NotOperatorError(operator)


def pattern_constructor(pattern: str, role_ids_in_guild: list[int], operators: dict[str, Operator], everyone_role_id: int) -> Component:
    """
     Function that checks to see if a pattern is correct
     Raises:
     FirstWordIsoperatorError if the first word of the pattern is an operator
     LastWordIsoperatorError if the last of the pattern is an operator
     DoubleOperatorError if two words in a row are operators
     NotValidSimpleComponentError if what looks like a SimpleComponent in the pattern is not one
     NotValidNumberOfRolesLimitComponentError if the pattern looks like a SimpleComponent, is a number and is less than 1

    """
    if not isinstance(pattern, str):
        raise PatternIsNotStrError
    pattern = pattern.lower().strip()
    number_of_opening_parentheses: int = 0
    number_of_closing_parentheses: int = 0
    for character in pattern:
        if character == "(":
            number_of_opening_parentheses += 1
        elif character == ")":
            number_of_closing_parentheses += 1
    if number_of_opening_parentheses > number_of_closing_parentheses:
        raise MoreOpeningThanClosingParenthesesError(pattern)
    if number_of_closing_parentheses > number_of_opening_parentheses:
        raise MoreClosingThanOpeningParenthesesError(pattern)

    words = pattern.split()
    if pattern[0] != "(":
        if len(words) == 1:
            return word_component_constructor(words[0].strip(), False, role_ids_in_guild, everyone_role_id)
        if len(words) == 2 and words[0].strip() == "not":
            return word_component_constructor(words[1].strip(), True, role_ids_in_guild, everyone_role_id)

    if pattern[0] != "(":
        raise StatementWithoutOpeningParenthesisError(pattern)
    if pattern[-1] != ")":
        raise StatementWithoutClosingParenthesisError(pattern)

    for index, word in enumerate(words):
        word = word.strip()
        if index == 0:
            last_word = ""
            last_last_word = ""
        elif index == 1:
            last_word = words[index-1].strip()
            last_last_word = ""
        else:
            last_word = words[index-1].strip()
            last_last_word = words[index-2].strip()

        try:
            get_operator((word, last_word, last_last_word), operators)
            is_in_operators = True
        except NotOperatorError:
            is_in_operators = False
        if is_in_operators and index == 0:
            raise FirstWordIsoperatorError(pattern)
        if is_in_operators and index == len(words)-1:
            raise LastWordIsoperatorError(pattern)
        if is_in_operators and last_was_operator:
            raise DoubleOperatorError

        last_was_operator = is_in_operators

    return statement_constructor(pattern, role_ids_in_guild, operators, everyone_role_id)


def reverse(string: str) -> str:
    reversed_string: str = ""
    for char in reversed(string):
        reversed_string += char
    return reversed_string


def count_parentheses(string: str) -> str:
    number_of_opening_parentheses = 0
    number_of_closing_parentheses = 0

    for index, character in enumerate(string):
        if character == "(":
            number_of_opening_parentheses += 1
        elif character == ")":
            number_of_closing_parentheses += 1
        if number_of_opening_parentheses - number_of_closing_parentheses == 0:
            return string[:index+1]
    if number_of_closing_parentheses > number_of_opening_parentheses:
        raise MoreClosingThanOpeningParenthesesError(string)
    if number_of_opening_parentheses > number_of_closing_parentheses:
        raise MoreOpeningThanClosingParenthesesError(string)


def reverse_count_parentheses(string: str) -> str:
    reversed_string = reverse(string)
    number_of_opening_parentheses = 0
    number_of_closing_parentheses = 0
    for index, character in enumerate(reversed_string):
        if character == "(":
            number_of_opening_parentheses += 1
        elif character == ")":
            number_of_closing_parentheses += 1
        if number_of_opening_parentheses - number_of_closing_parentheses == 0:

            return_slice = len(string) - index - 1
            return_value = string[return_slice:]
            return return_value
    if number_of_closing_parentheses > number_of_opening_parentheses:
        raise MoreClosingThanOpeningParenthesesError(string)
    if number_of_opening_parentheses > number_of_closing_parentheses:
        raise MoreOpeningThanClosingParenthesesError(string)


def statement_constructor(string: str, role_ids_in_guild: list[int], operators: dict[str, Operator, ], everyone_role_id: int) -> Statement:
    """
        Constructs a statement from a string
        Raises:
        StatementWithoutOpeningParenthesisError if the first character is not an opening parenthesis
        StatementWithoutClosingParenthesisError if the last character is not a closing parenthesis
        TooFewCommasInStatementError if there are less than 2 commas in the string
        ValueError --- This means a programming error has occured
        NotOperatorError if the operator of the statement is not a valid operator
        NotValidSimpleComponentError if a simple component in the statement is invalid
        NotValidNumberOfRolesLimitComponentError if a simple component in the statement is a number but less than 1
    """
    string = string.strip()
    if string[0] != "(":
        raise StatementWithoutOpeningParenthesisError(string)
    if string[-1] != ")":
        raise StatementWithoutClosingParenthesisError(string)

    string = string[1:]
    string = string[:-1]

    parts = string.split(",")
    if len(parts) < 3:
        raise TooFewCommasInStatementError(string)

    if string[0] == "(":
        component_1_str = count_parentheses(string)
    else:
        component_1_str = parts[0].strip()

    component_1 = component_constructor(
        component_1_str, role_ids_in_guild, operators, everyone_role_id)

    if string[-1] == ")":
        component_2_str = reverse_count_parentheses(string)
    else:
        component_2_str = parts[-1].strip()

    component_2 = component_constructor(
        component_2_str, role_ids_in_guild, operators, everyone_role_id)
    # not_operator_part_1 is the first component
    not_operator_part_1 = len(component_1_str)-1
    # not_operator_part_2 is the second component
    not_operator_part_2 = len(string) - len(component_2_str)
    # We take everything that is not the first or the second component
    operator_str = string[not_operator_part_1:not_operator_part_2]
    # We take the stuff that is between the two commas
    operator_str = operator_str.split(",")[1].strip()

    operator = operator_constructor(operator_str, operators)

    return Statement(component_1, operator, component_2)


def component_constructor(component: str, role_ids_in_guild: list[int], operators: dict[str, Operator], everyone_role_id) -> Component:
    component = component.strip()
    if component[0] == "(":
        return statement_constructor(component, role_ids_in_guild, operators, everyone_role_id)
    words = component.split()
    if words[0].strip() == "not":
        return word_component_constructor(words[1].strip(), True, role_ids_in_guild, everyone_role_id)
    return word_component_constructor(words[0].strip(), False, role_ids_in_guild, everyone_role_id)


def word_component_constructor(word: str, reverse_component: bool, role_ids_in_guild: list[int], everyone_role_id: int) -> Component:
    """
    Creates a component from a single word
    Can create anything but Statements at the moment
    raises NotValidSimpleComponentError and NotValidNumberOfRolesLimitComponentError if it does not match any known component
    """

    component = get_simple_component(word, role_ids_in_guild, everyone_role_id)
    if reverse_component:
        return ReverseComponent(component)
    return component


def get_simple_component(word: str, role_ids_in_guild: list[int], everyone_role_id: int) -> SimpleComponent:
    word_as_role_id = word[3:-1]
    TOO_SHORT = len(word) < 5
    for role_id in role_ids_in_guild:
        if TOO_SHORT:
            break
        if word_as_role_id == str(role_id):
            return RoleComponent(role_id)
    if word == "@everyone":
        return RoleComponent(everyone_role_id)
    if word == "true":
        return BooleanComponent(True)
    if word == "false":
        return BooleanComponent(False)
    try:
        int_word = int(word)
    except ValueError:
        raise NotValidSimpleComponentError(word)
    if int_word < 1:
        raise NotValidNumberOfRolesLimitComponentError(word)
    return NumberOfRolesLimitComponent(int_word)
