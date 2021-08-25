from pattern_parser.simple_discord import SimpleGuild
from pattern_parts.comparator_implementation import LessThanOrEqualToLimitComparator, NotEqualToLimitComparator
from advanced_component import *
from simple_component import *
from operators import *
from logs.log import print
"""members = [
                0SimpleMember(
                    {
                        1: False,
                        2: True,
                        3: False,
                        4: True,
                        5: False,
                        6: True,
                        7: False,
                        8: True,
                        9: False,
                        10: True
                    }
                ),
                1SimpleMember(
                    {
                        1: False,
                        2: False,
                        3: False,
                        4: False,
                        5: False,
                        6: False,
                        7: False,
                        8: False,
                        9: False,
                        10: False
                    }, True
                ),
                2SimpleMember(
                    {
                        1: True,
                        2: True,
                        3: True,
                        4: False,
                        5: True,
                        6: True,
                        7: False,
                        8: False,
                        9: True,
                        10: False
                    }, True
                ),
                3SimpleMember(
                    {
                        1: True,
                        2: True,
                        3: False,
                        4: False,
                        5: False,
                        6: False,
                        7: True,
                        8: False,
                        9: False,
                        10: True
                    }
                ),
                4SimpleMember(
                    {
                        1: True,
                        2: False,
                        3: False,
                        4: True,
                        5: False,
                        6: False,
                        7: True,
                        8: False,
                        9: False,
                        10: False
                    }, True
                ),
                5SimpleMember(
                    {
                        1: True,
                        2: True,
                        3: True,
                        4: False,
                        5: False,
                        6: False,
                        7: False,
                        8: False,
                        9: False,
                        10: False
                    }
                )

            ]"""


def test_reverse_component():
    guild: SimpleGuild = SimpleGuild()
    true_component = BooleanComponent(True)
    false_component = BooleanComponent(False)
    reverse_true_component = ReverseComponent(true_component)
    reverse_false_component = ReverseComponent(false_component)

    assert not reverse_true_component.user_applies(guild.members()[0])
    assert reverse_false_component.user_applies(guild.members()[0])

    role_count_component = RolesLimitComponent(
        LessThanOrEqualToLimitComparator(3))
    reverse_role_count_component = ReverseComponent(role_count_component)

    assert reverse_role_count_component.user_applies(guild.members()[0])


def test_statement():
    guild: SimpleGuild = SimpleGuild()
    inner_statement = Statement(RoleComponent(
        1), AndOperator(), RoleComponent(2))
    outer_statement = Statement(
        inner_statement, ExclusiveOrOperator(), RolesLimitComponent(LessThanOrEqualToLimitComparator(3)))

    assert not inner_statement.user_applies(guild.members()[0])
    assert inner_statement.user_applies(guild.members()[2])
    assert outer_statement.user_applies(guild.members()[1])

    assert not outer_statement.user_applies(guild.members()[5])


def test_statement_repr():
    statement = Statement(
        RolesLimitComponent(LessThanOrEqualToLimitComparator(5)),
        AndOperator(),
        Statement(
            RoleComponent(6),
            OrOperator(),
            RoleComponent(3)
        )
    )
    print("Printing statement repr")
    print(statement.__repr__())


def test_statement_repr_2():
    statement = Statement(
        Statement(
            BooleanComponent(False),
            ExclusiveOrOperator(),
            RolesLimitComponent(NotEqualToLimitComparator(69))
        ),
        AndOperator(),
        Statement(
            ReverseComponent(RoleComponent(6)),
            OrOperator(),
            RoleComponent(3)
        )
    )
    print("Printing statement repr")
    print(statement.__repr__())
