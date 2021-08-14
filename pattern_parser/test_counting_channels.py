from abc import abstractmethod
from patterns.pattern import PatternParams
from patterns.comparators import GreaterThanOrEqualToLimitComparator, LessThanOrEqualToLimitComparator
from patterns.operators import AndOperator, ExclusiveOrOperator, NotExclusiveOrOperator, NotOrOperator, OrOperator
from patterns.advanced_component import ReverseComponent, Statement
from patterns.simple_component import BooleanComponent, BotComponent, RoleComponent, RolesLimitComponent
from patterns.components import Component
from patterns.pattern_error import MoreOpeningThanClosingParenthesesError, NotValidSimpleComponentError
from patterns.counting_channels import PatternError, get_simple_component, operator_constructor, pattern_constructor
from logs.log import print
import pickle
import time
from inspect import getmembers


def pattern_test_template(pattern: str, should_fail: bool = True, error: PatternError = PatternError):

    params = PatternParams(pattern=pattern)
    try:
        result = pattern_constructor(
            params)
        assert not should_fail
        return result
    except error as e:
        print(e)
        assert should_fail


def successful_pattern_test_template(pattern: str, correct: Component):
    time_before = time.time()
    component = pattern_test_template(pattern, False)
    time_after = time.time()
    print(f"Constructing pattern {pattern}\ntook {time_after-time_before}")
    as_bytes = pickle.dumps(component)
    recovered = pickle.loads(as_bytes)
    print(f"Component from string as dict: {component.to_dict()}")
    print(f"correct component as dict: {correct.to_dict()}")
    if correct.to_dict() == component.to_dict():
        print("Dictionary representations match")
    else:
        print("Dictionary represenations differ")

    assert recovered == component
    assert component == correct


def test_pattern_verifier_1():
    pattern_test_template(
        "I am a random string that has nothing to do with patterns")


def test_pattern_verifier_2():
    correct = Statement(
        ReverseComponent(RolesLimitComponent(
            LessThanOrEqualToLimitComparator(1))),
        AndOperator(),
        ReverseComponent(RoleComponent(2))
    )
    successful_pattern_test_template("(not <= 1,and,not aaa2a)", correct)


def test_pattern_verifier_3():
    correct = RoleComponent(1)
    successful_pattern_test_template("aaa1a", correct)


def test_pattern_verifier_4():
    correct = Statement(
        BooleanComponent(True),
        AndOperator(),
        Statement(
            BooleanComponent(True),
            AndOperator(),
            Statement(
                RoleComponent(2),
                AndOperator(),
                RoleComponent(3)
            )
        )
    )

    successful_pattern_test_template(
        "(true, and, (true, and, (aaa2a, and, aaa3a)))", correct)


def test_pattern_verifier_5():

    correct = Statement(
        BooleanComponent(False),
        OrOperator(),
        Statement(
            RolesLimitComponent(LessThanOrEqualToLimitComparator(1)),
            NotOrOperator(),
            Statement(
                RoleComponent(10),
                NotExclusiveOrOperator(),
                Statement(
                    BooleanComponent(True),
                    AndOperator(),
                    RolesLimitComponent(LessThanOrEqualToLimitComparator(3))
                )
            )
        )
    )
    successful_pattern_test_template(
        "(false, or,(<= 1, not inclusive or,(aaa10a,not exclusive or,(true, and, <= 3))))", correct)


def test_pattern_verifier_6():
    pattern_test_template("((()", MoreOpeningThanClosingParenthesesError)


def test_pattern_verifier_7():
    pattern_test_template("a", NotValidSimpleComponentError)


def test_pattern_verifier_8():
    correct = RoleComponent(1)
    successful_pattern_test_template("@everyone", correct)


def test_pattern_verifier_9():
    correct = Statement(
        Statement(
            BooleanComponent(True),
            AndOperator(),
            BooleanComponent(True)
        ),
        AndOperator(),
        Statement(
            BooleanComponent(True),
            AndOperator(),
            BooleanComponent(True)
        )
    )
    successful_pattern_test_template(
        "((true, and, true), and, (true, and, true))", correct)


def test_pattern_verifier_10():
    correct = Statement(
        Statement(
            Statement(
                RoleComponent(1),
                AndOperator(),
                RoleComponent(3)
            ),
            NotExclusiveOrOperator(),
            RoleComponent(2)
        ),
        ExclusiveOrOperator(),
        Statement(
            RolesLimitComponent(LessThanOrEqualToLimitComparator(1)),
            NotOrOperator(),
            Statement(
                RolesLimitComponent(LessThanOrEqualToLimitComparator(1)),
                AndOperator(),
                RolesLimitComponent(LessThanOrEqualToLimitComparator(3))
            )
        )
    )
    successful_pattern_test_template(
        "(((aaa1a, and, aaa3a), not exclusive or, aaa2a), exclusive or, (<= 1, not or, (<= 1, and, <= 3)))", correct)


def test_pattern_verifier_11():
    correct = Statement(
        BotComponent(),
        NotOrOperator(),
        Statement(
            Statement(
                BotComponent(),
                AndOperator(),
                RoleComponent(3)
            ),
            NotExclusiveOrOperator(),
            Statement(
                BotComponent(),
                OrOperator(),
                RolesLimitComponent(GreaterThanOrEqualToLimitComparator(3))
            )
        )
    )

    successful_pattern_test_template(
        "(bot, not or, ((bot, and, aaa3a), nxor, (bot, or, >= 3)))", correct
    )


def test_pattern_verifier_12():
    correct = RolesLimitComponent(GreaterThanOrEqualToLimitComparator(3))
    successful_pattern_test_template(">= 3", correct)


def test_pattern_verifier_13():
    pattern_test_template(
        "(bot, not or, ((bot, and, aaa3a), nxor, (bot, or, > = 3)))")


def test_get_simple_component_errors():
    #params = PatternParams("(bot, not or, ((bot, and, aaa3a), nxor, (bot, or, > = 3)))", )
    print("Running test_get_simple_component_errors")
    pattern = "(bot, not or, ((bot, and, aaa3a), nxor, (bot, or, > = 3)))"
    current_part = " > = 3"
    index_of_current_part = 49
    params = PatternParams(pattern, index_of_current_part,
                           current_part=current_part)
    try:
        get_simple_component(params)
    except PatternError as e:
        print(e.__str__())


def test_get_operator_constructor():
    pattern = "(bot, not orr, ((bot, and, aaa3a), nxor, (bot, or, > = 3)))"
    current_part = " not orr"
    index_of_current_part = 4
    params = PatternParams(pattern, index_of_current_part,
                           current_part=current_part)
    try:
        operator_constructor(params)
    except PatternError as e:
        print(e.__str__())
