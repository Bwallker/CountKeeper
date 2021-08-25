
from pattern_parser.pattern import PatternParams

from pattern_parts.advanced_component import ReverseComponent, Statement
from pattern_parts.simple_component import BooleanComponent, BotComponent, RoleComponent, RolesLimitComponent, SimpleComponent
from pattern_parts.components import Component
from pattern_parser.pattern_error import *
import discord
from discord.channel import VoiceChannel
from discord import Guild
from logs.log import print
from pattern_parts.operators import Operator
# This file contains helper functions for updating the channels


async def update_channel(channel: VoiceChannel, role_number: int, guild: Guild) -> dict[str, str]:
    message = ""
    first_number = None
    words = channel.name.split()
    for i, word in enumerate(words):
        if word.isdigit():
            first_number = word
            words[i] = str(role_number)
            break
    words = " ".join(words)
    output = None
    if first_number is None:
        output = channel.name + " " + str(role_number)
    else:
        output = words
    previous_name = channel.name
    try:
        await channel.edit(name=output)
        print(
            f"channel {previous_name} renamed to {channel.name} in guild {guild}")
    except discord.errors.Forbidden:
        print(
            f"discord Forbidden exception raised while trying to rename channel {previous_name} in guild {guild.name}")
    return {previous_name: output}


def is_operator(parts: tuple[str], operators: dict[str, Operator]) -> tuple[Operator, int]:
    try:
        get_operator(parts, operators)
        return True
    except NotOperatorError:
        return False


def get_operator(params: PatternParams, parts: tuple[str]) -> Operator:
    """Returns the size of the operator in words and the operator"""
    joined = " ".join(parts)

    if not isinstance(parts, tuple) and not isinstance(parts, list):
        raise ValueError(f"parts is type {type(parts)}")
    operators = params.operators
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
    raise NotOperatorError(
        params.pattern, params.index_of_current_part + len(joined)/2 + 1)


def operator_constructor(params: PatternParams) -> Operator:
    operator = params.current_part

    if operator in params.operators:
        return params.operators.get(operator)()

    raise NotOperatorError(
        params.pattern, params.index_of_current_part + len(operator)/2 + 1)


def pattern_constructor(params: PatternParams) -> Component:
    """
     Function that construcs a pattern from a string representation, provided by the user in most cases
     Raises:
     FirstWordIsoperatorError if the first word of the pattern is an operator
     LastWordIsoperatorError if the last of the pattern is an operator
     DoubleOperatorError if two words in a row are operators
     NotValidSimpleComponentError if what looks like a SimpleComponent in the pattern is not one
     NotValidNumberOfRolesLimitComponentError if the pattern looks like a SimpleComponent, is a number and is less than 1

    """
    pattern = params.pattern
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
            params.current_part = words[0].strip()
            params.index_of_current_part = words[0].find(words[0].strip())
            return word_component_constructor(params, False)
        if len(words) == 2 and words[0].strip() == "not":
            params.current_part = words[1].strip()
            params.index_of_current_part = pattern.find(
                params.current_part) + 1
            return word_component_constructor(params, True)
        else:
            params.current_part = " ".join([word.strip() for word in words])
            params.index_of_current_part = pattern.find(
                params.current_part)
            return word_component_constructor(params, False)
    if pattern[0] != "(":
        raise StatementWithoutOpeningParenthesisError(pattern, 0)
    if pattern[-1] != ")":
        raise StatementWithoutClosingParenthesisError(pattern, -1)
    index_in_pattern = 0
    last_word = ""
    last_last_word = ""
    for index, word in enumerate(words):
        unmutated_word = word
        index_in_pattern += len(last_word)
        word = word.strip()
        params.current_part = word
        params.index_of_current_part = index_in_pattern
        try:
            get_operator(params, (word, last_word.strip(),
                         last_last_word.strip()))
            is_in_operators = True
        except NotOperatorError:
            is_in_operators = False
        if is_in_operators and index == 0:
            raise FirstWordIsoperatorError(pattern, 0)
        if is_in_operators and index == len(words)-1:
            raise LastWordIsoperatorError(pattern, -1)
        if is_in_operators and last_was_operator:
            raise DoubleOperatorError(
                pattern, index_in_pattern + (len(word)/2))

        last_was_operator = is_in_operators
        last_last_word = last_word
        last_word = unmutated_word

    params.current_part = params.pattern
    params.index_of_current_part = 0
    return statement_constructor(params)


def reverse(string: str) -> str:
    reversed_string: str = ""
    for char in reversed(string):
        reversed_string += char
    return reversed_string


def count_parentheses(params: PatternParams) -> str:
    number_of_opening_parentheses = 0
    number_of_closing_parentheses = 0

    for index, character in enumerate(params.current_part):
        if character == "(":
            number_of_opening_parentheses += 1
        elif character == ")":
            number_of_closing_parentheses += 1
        if number_of_opening_parentheses == number_of_closing_parentheses:
            return params.current_part[:index+1]
    if number_of_closing_parentheses > number_of_opening_parentheses:
        raise MoreClosingThanOpeningParenthesesError(
            params.pattern, params.index_of_current_part + len(params.current_part) - 1)
    if number_of_opening_parentheses > number_of_closing_parentheses:
        raise MoreOpeningThanClosingParenthesesError(
            params.pattern, params.index_of_current_part)


def reverse_count_parentheses(params: PatternParams) -> tuple[str, int]:

    reversed_current_part = reverse(params.current_part)
    number_of_opening_parentheses = 0
    number_of_closing_parentheses = 0
    for index, character in enumerate(reversed_current_part):
        if character == "(":
            number_of_opening_parentheses += 1
        elif character == ")":
            number_of_closing_parentheses += 1
        if number_of_opening_parentheses - number_of_closing_parentheses == 0:

            return_slice = len(params.current_part) - index - 1
            return_value = params.current_part[return_slice:]
            return return_value
    if number_of_closing_parentheses > number_of_opening_parentheses:
        raise MoreClosingThanOpeningParenthesesError(
            params.pattern, params.index_of_current_part + len(params.current_part) - 1)
    if number_of_opening_parentheses > number_of_closing_parentheses:
        raise MoreOpeningThanClosingParenthesesError(
            params.pattern, params.index_of_current_part)


def statement_constructor(params: PatternParams) -> Statement:
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
    current_part = params.current_part
    index_of_current_part = params.index_of_current_part

    current_part = current_part.strip()
    if current_part[0] != "(":
        raise StatementWithoutOpeningParenthesisError(
            params.pattern, params.index_of_current_part)
    if current_part[-1] != ")":
        raise StatementWithoutClosingParenthesisError(
            params.pattern, params.index_of_current_part + len(params.current_part)-1)

    current_part = current_part[1:]
    current_part = current_part[:-1]
    index_of_current_part += 1
    parts = current_part.split(",")

    if len(parts) < 3:
        raise TooFewCommasInStatementError(
            params.pattern, params.index_of_current_part + (len(params.current_part)/2) + 1)

    params.current_part = current_part
    params.index_of_current_part = index_of_current_part

    if current_part[0] == "(":
        component_1_str = count_parentheses(params)
        index = 0
    else:
        component_1_str = parts[0].strip()
        index = parts[0].find(parts[0].strip())
    params.current_part = component_1_str
    params.index_of_current_part += index
    component_1_first_index = params.index_of_current_part
    component_1_last_index = component_1_first_index + len(component_1_str) - 1

    component_1 = component_constructor(params)
    params.index_of_current_part = index_of_current_part
    params.current_part = current_part
    if current_part[-1] == ")":
        component_2_str = reverse_count_parentheses(params)
    else:
        component_2_str = parts[-1].strip()
    params.current_part = component_2_str
    params.index_of_current_part += len(current_part) - \
        len(component_2_str)
    component_2_first_index = params.index_of_current_part
    component_2_last_index = component_2_first_index + len(component_2_str) - 1
    predicted_component_2_str = ""
    i = component_2_first_index
    while i <= component_2_last_index:
        predicted_component_2_str += params.pattern[i]
        i += 1

    component_2 = component_constructor(params)
    # We take everything that is not the first or the second component
    operator_str = params.pattern[component_1_last_index +
                                  1:component_2_first_index]

    # We take the stuff that is between the two commas
    actual_operator_str = operator_str.split(",")[1].strip()
    params.current_part = actual_operator_str
    params.index_of_current_part = component_1_last_index + 1 + \
        operator_str.find(actual_operator_str)
    operator = operator_constructor(params)

    return Statement(component_1, operator, component_2)


def component_constructor(params: PatternParams) -> Component:

    component = params.current_part

    component = component.strip()
    if component[0] == "(":
        return statement_constructor(params)
    words = component.split()
    # Count how many whitespaces get yeeted from the first word, since that affects index_of_current_part
    whitespaces = 0
    for char in words[0]:
        if char == " ":
            whitespaces += 1
        else:
            break
    words = [word.strip() for word in words]
    if words[0] == "not":
        words.pop(0)
        new_component = " ".join(words)
        params.index_of_current_part = params.index_of_current_part + \
            params.current_part.find(new_component)
        params.current_part = new_component
        return word_component_constructor(params, True)
    new_component = " ".join(words)
    params.current_part = new_component
    params.index_of_current_part += whitespaces

    return word_component_constructor(params, False)


def word_component_constructor(params: PatternParams, reverse_component: bool) -> Component:
    """
    Creates a component from a single word
    Can create anything but Statements at the moment
    raises NotValidSimpleComponentError and NotValidNumberOfRolesLimitComponentError if it does not match any known component
    """

    component = get_simple_component(
        params)
    if reverse_component:
        return ReverseComponent(component)
    return component


def get_simple_component(params: PatternParams) -> SimpleComponent:
    word = params.current_part
    if word.startswith("<@&") and word.endswith(">"):
        word_as_role_id = word[3:-1]
        for role_id in params.guild.roles():
            if word_as_role_id == str(role_id):
                return RoleComponent(role_id)

    if word == "@everyone":
        return RoleComponent(params.guild.everyone_role())
    if word == "true":
        return BooleanComponent(True)
    if word == "false":
        return BooleanComponent(False)
    if word == "bot":
        return BotComponent()
    symbol = word.split()[0].strip()
    index = word.find(symbol) + \
        params.index_of_current_part + len(symbol)/2 + 1
    if not symbol in params.comparators:
        raise NotValidSimpleComponentError(
            params.pattern, index)
    comparator_class = params.comparators[symbol]

    try:
        limit = word.split()[1].strip()
        int_limit = int(limit)
    except ValueError:
        raise NotValidSimpleComponentError(
            params.pattern, params.index_of_current_part + len(params.current_part)/2)
    except IndexError:
        raise NotValidSimpleComponentError(
            params.pattern, params.index_of_current_part + len(params.current_part)/2)
    if int_limit < 1:
        raise NotValidRolesLimitComponentError(
            params.pattern, params.index_of_current_part + len(params.current_part)/2)
    return RolesLimitComponent(comparator_class(int_limit))
