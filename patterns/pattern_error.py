class PatternError(Exception):
    """
        Base class for the exceptions that get raised for invalid patterns
    """
    __index_of_error: int
    __error_description: str
    __pattern_with_error: str

    def __init__(self, pattern_with_error: str, index_of_error: int = None) -> None:
        self.__pattern_with_error = pattern_with_error
        if index_of_error is None:
            index_of_error = int(len(pattern_with_error)/2)
        if index_of_error < 0:
            index_of_error = 0
        self.__index_of_error = index_of_error
        self.__error_description = ""
        
    

    def __str__(self):
        print(f"Entered __str__ of patternerror of type {type(self).__name__}")
        print(self.__error_description)
        print(self.__pattern_with_error)
        print(self.__index_of_error)
        output: str = self.__pattern_with_error
        output += "\n"
        output += self.place_arrow()
        output += "\n\n"
        output += self.__error_description
        return output
    def place_arrow(self):

        output: str = ""
        RANGE = len(self.__pattern_with_error)
        for i in range(RANGE):
            output += ("^" if i == self.__index_of_error else " ")
        return output

class PatternIsNotStrError(PatternError):
    """
        Exception raised when a pattern passed into the patter verifier is not a str
    """
class DoubleOperatorError(PatternError):
    """
        Exception raised if two consecutive words in a pattern are operators
    """
class FirstWordIsoperatorError(PatternError):
    """
        Exception raised if the first word in a pattern is an operator
    """
class LastWordIsoperatorError(PatternError):
    """
        Exception raised if the last word in a pattern is an operator
    """
class DoubleSimpleComponentError(PatternError):
    """
        Exception raised if two words in a row are SimpleComponents
    """
class NotOperatorError(PatternError):
    """
        Exception raised if an operator given to get_operator is not a valid operator
    """
class NotValidSimpleComponentError(PatternError):
    """
        Exception raised if a word cannot be parsed to a valid simple component
    """
class NotValidNumberOfRolesLimitComponentError(PatternError):
    """
        Exception raised if a SimpleComponent is made from a word that is a number, but less than one.
        This indicates that the user was trying to create a NumberOfRolesLimitComponent with an invalid number of roles
    """
class MoreOpeningThanClosingParenthesesError(PatternError):
    """
        Exception raised if there are more opening than closing parentheses in a pattern
    """
class MoreClosingThanOpeningParenthesesError(PatternError):
    """
        Exception raised if there are more closing than opening parentheses in a pattern
    """
class StatementWithoutOpeningParenthesisError(PatternError):
    """
        Exception raised if a statement does not start with an opening parenthesis
    """
class StatementWithoutClosingParenthesisError(PatternError):
    """
        Exception raised if a statement does not start with a closing parenthesis
    """
class TooFewCommasInStatementError(PatternError):
    """
        Exception raised if a string representation of a statement does not include exactly 2 commas
    """


class RoleNotInRolesError(PatternError):
    """
        Exception that gets thrown if a role in a statement is not a part of the roles of the guild
        Generally means that a pattern has not been properly cleaned up after a role was deleted
    """