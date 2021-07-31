from component import *
def test_role_component():
    role_component = RoleComponent(11)
    sum_of_roles = 0
    user_roles = {
        5: True,
        7: False,
        11: False,
        15: True
    }
    assert not role_component.user_applies(user_roles)
    sum_of_roles += role_component.user_applies(user_roles)
    user_roles_2 = {
        5: False,
        7: False,
        11: True,
        15: False
    }
    assert role_component.user_applies(user_roles_2)
    sum_of_roles += role_component.user_applies(user_roles_2)
    user_roles_3 = {
        5: False,
        7: False,
        11: True,
        15: True
    }
    assert role_component.user_applies(user_roles_3)
    sum_of_roles += role_component.user_applies(user_roles_3)

    assert sum_of_roles == 2

def test_role_count_component():
    role_count_component = NumberOfRolesLimitComponents(5)
    user_1 = {
        1: True,
        2: True,
        3: True,
        4: True,
        5: True
    }
    assert role_count_component.user_applies(user_1)

    user_2 = {
        1: False,
        2: False,
        3: False,
        4: False,
        5: False,
        6: False,
        7: False
    }

    assert role_count_component.user_applies(user_2)

    user_3 = {
        1: True,
        2: False,
        3: True,
        4: False,
        5: True,
        6: False,
        7: True,
        8: False,
        9: True,
        10: False
    }

    assert role_count_component.user_applies(user_3)

    user_4 = {
        1: True,
        2: True,
        3: True,
        4: False,
        5: False,
        6: False,
        7: True,
        8: True,
        9: True
    }

    assert not role_count_component.user_applies(user_4)

def test_boolean_component():
    true_component = BooleanComponent(True)
    false_component = BooleanComponent(False)

    assert true_component.user_applies({})
    assert not false_component.user_applies({})

    user_1 = {
        1: True,
        2: False,
        3: True,
        4: False
    }

    assert true_component.user_applies(user_1)
    assert not false_component.user_applies(user_1)

def test_reverse_component():
    true_component = BooleanComponent(True)
    false_component = BooleanComponent(False)
    reverse_true_component = ReverseComponent(true_component)
    reverse_false_component = ReverseComponent(false_component)

    assert not reverse_true_component.user_applies({})
    assert reverse_false_component.user_applies({})

    role_count_component = NumberOfRolesLimitComponents(3)
    reverse_role_count_component = ReverseComponent(role_count_component)

    user_1 = {
        1: True,
        2: False,
        3: False,
        4: False,
        5: True
    }

    assert not reverse_role_count_component.user_applies(user_1)