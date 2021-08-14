from pattern_error import *
from logs.log import print


def test_generic():
    print("Start of test_generic")
    print(MoreOpeningThanClosingParenthesesError("((()", 0).__str__())


def test_successful():
    print(SuccessfullyConstructedComponent("abcdef").__str__())
