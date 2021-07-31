from abc import abstractmethod
from patterns.pattern_error import MoreOpeningThanClosingParenthesesError, NotValidSimpleComponentError
from patterns.counting_channels import PatternError, pattern_constructor, operators
from logs.log import print
import json
import channels_manager
from inspect import getmembers
def pattern_test_template(pattern: str, should_fail: bool = True, error: PatternError = PatternError):
    global operators
    list_of_roles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    everyone_role_id = 1
    try:
        result = pattern_constructor(pattern, list_of_roles, operators, everyone_role_id)
        assert not should_fail
        return result
    except error as e:
        print(e)
        assert should_fail

def successful_pattern_test_template(pattern: str):
    component = pattern_test_template(pattern, False)
    channels_manager.init()
    recovered_object = channels_manager.from_dict(component.__dict__())
    print(recovered_object)
    print(recovered_object.__dict__())
    assert component == recovered_object
def test_pattern_verifier_1():
    
    pattern_test_template("I am a random string that has nothing to do with patterns")
    

def test_pattern_verifier_2():
    successful_pattern_test_template("(not 1,and,not aaa2a)")

def test_pattern_verifier_3():
    successful_pattern_test_template("aaa1a")

def test_pattern_verifier_4():
    successful_pattern_test_template("(true, and, (true, and, (aaa2a, and, aaa3a)))")

def test_pattern_verifier_5():
    successful_pattern_test_template("(false, or,(1, not inclusive or,(aaa10a,not exclusive or,(true, and, 3))))")

def test_pattern_verifier_6():
    pattern_test_template("((()", MoreOpeningThanClosingParenthesesError)

def test_pattern_verifier_7():
    pattern_test_template("a", NotValidSimpleComponentError)
def test_pattern_verifier_8():
    successful_pattern_test_template("@everyone")

