from pattern_error import *
from logs.log import print


def test_generic():
    print("Start of test_generic")
    print(MoreOpeningThanClosingParenthesesError("((()", 0).__str__())
