from abc import abstractmethod


class PatternError(Exception):
    """
        Base class for the exceptions that get raised for invalid patterns
    """
    __index_of_error: int
    __pattern_with_error: str

    def __init__(self, pattern_with_error: str, index_of_error: int = None) -> None:
        super().__init__()
        self.__pattern_with_error = pattern_with_error
        if index_of_error is None:
            index_of_error = int(len(pattern_with_error)/2)
        if index_of_error < 0:
            index_of_error = len(pattern_with_error) - index_of_error
        index_of_error = int(index_of_error)
        self.__index_of_error = index_of_error

    def __str__(self):
        output: str = self.__pattern_with_error
        output += "\n"
        output += self.place_arrow()
        output += "\n\n"
        output += self.get_error_description()
        return output

    def place_arrow(self):

        output: str = ""
        RANGE = len(self.__pattern_with_error)
        for i in range(RANGE):
            output += ("^" if i == self.__index_of_error else " ")
        return output

    def get_error_description(self) -> str:
        return ""

    def get_pattern_with_error(self) -> str:
        return self.__pattern_with_error


class PatternIsNotStrError(PatternError):
    """
        Exception raised when a pattern passed into the patter verifier is not a str
    """

    def get_error_description(self) -> str:
        return "The pattern you supplied is not a string --- This should never happen and something has clearly gone quite terribly wrong"


class DoubleOperatorError(PatternError):
    """
        Exception raised if two consecutive words in a pattern are operators
    """

    def get_error_description(self) -> str:
        return "Your pattern contained two operators in a row"


class FirstWordIsoperatorError(PatternError):
    """
        Exception raised if the first word in a pattern is an operator
    """

    def get_error_description(self) -> str:
        return "The first word in your pattern was an operator"


class LastWordIsoperatorError(PatternError):
    """
        Exception raised if the last word in a pattern is an operator
    """

    def get_error_description(self) -> str:
        return "The last word in your pattern was an operator"


class DoubleSimpleComponentError(PatternError):
    """
        Exception raised if two words in a row are SimpleComponents
    """

    def get_error_description(self) -> str:
        return "Your pattern contained two simple components in a row"


class NotOperatorError(PatternError):
    """
        Exception raised if an operator given to get_operator is not a valid operator
    """

    def get_error_description(self) -> str:
        return "This operator is not a valid operator"


class NotValidSimpleComponentError(PatternError):
    """
        Exception raised if a word cannot be parsed to a valid simple component
    """

    def get_error_description(self) -> str:
        return "This component was interpreted as being a simple pattern, but it could not be parsed to a valid simple component"


class NotValidRolesLimitComponentError(PatternError):
    """
        Exception raised if a SimpleComponent is made from a word that is a number, but less than one.
        This indicates that the user was trying to create a NumberOfRolesLimitComponent with an invalid number of roles
    """

    def get_error_description(self) -> str:
        return "Your role count component has a role count of less than 1"


class NotValidComparatorError(PatternError):
    """
        Exception raised if a comparator provided with a rolelimitcomponent is not valid
    """

    def get_error_description(self) -> str:
        return "This role limit component did not come with a valid comparator"


class MoreOpeningThanClosingParenthesesError(PatternError):
    """
        Exception raised if there are more opening than closing parentheses in a pattern
    """

    def get_error_description(self) -> str:
        return "Your pattern contains more opening than closing parentheses"


class MoreClosingThanOpeningParenthesesError(PatternError):
    """
        Exception raised if there are more closing than opening parentheses in a pattern
    """

    def get_error_description(self) -> str:
        return "Your pattern contains more closing than opening parentheses"


class StatementWithoutOpeningParenthesisError(PatternError):
    """
        Exception raised if a statement does not start with an opening parenthesis
    """

    def get_error_description(self) -> str:
        return "This statement did not start with an opening parenthesis"


class StatementWithoutClosingParenthesisError(PatternError):
    """
        Exception raised if a statement does not start with a closing parenthesis
    """

    def get_error_description(self) -> str:
        return "This statement did not end with a closing parenthesis"


class TooFewCommasInStatementError(PatternError):
    """
        Exception raised if a string representation of a statement does not include exactly 2 commas
    """

    def get_error_description(self) -> str:
        return "This statement contained less than 2 commas"


