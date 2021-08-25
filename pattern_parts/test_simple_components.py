from pattern_parser.simple_discord import SimpleGuild
from pattern_parts.comparator_implementation import GreaterThanLimitComparator, LessThanOrEqualToLimitComparator
from simple_component import *
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


def test_role_component():
    guild = SimpleGuild()
    role_component = RoleComponent(7)
    sum_of_roles = 0

    assert not role_component.user_applies(guild.members()[5])
    sum_of_roles += role_component.user_applies(guild.members()[5])

    assert role_component.user_applies(guild.members()[4])
    sum_of_roles += role_component.user_applies(guild.members()[4])

    assert role_component.user_applies(guild.members()[3])
    sum_of_roles += role_component.user_applies(guild.members()[3])

    assert sum_of_roles == 2


def test_role_count_component():
    guild = SimpleGuild()
    role_count_component = RolesLimitComponent(
        LessThanOrEqualToLimitComparator(5))

    assert role_count_component.user_applies(guild.members()[0])

    assert role_count_component.user_applies(guild.members()[3])

    assert role_count_component.user_applies(guild.members()[4])

    assert not role_count_component.user_applies(guild.members()[2])


def test_role_count_component_2():
    guild = SimpleGuild()
    role_count_component = RolesLimitComponent(GreaterThanLimitComparator(3))

    assert role_count_component.user_applies(guild.members()[0])

    assert not role_count_component.user_applies(guild.members()[1])

    assert not role_count_component.user_applies(guild.members()[5])

    assert role_count_component.user_applies(guild.members()[3])


def test_boolean_component():
    guild = SimpleGuild()
    true_component = BooleanComponent(True)
    false_component = BooleanComponent(False)

    assert true_component.user_applies(guild.members()[0])
    assert not false_component.user_applies(guild.members()[0])

    assert true_component.user_applies(guild.members()[1])
    assert not false_component.user_applies(guild.members()[1])


def test_bot_component():
    guild = SimpleGuild()
    bot_component = BotComponent()
    assert not bot_component.user_applies(guild.members()[0])
    assert bot_component.user_applies(guild.members()[1])
    assert bot_component.user_applies(guild.members()[2])
