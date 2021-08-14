from statement import Statement
from component import *
from operators import *
def test_statement():
    inner_statement = Statement(RoleComponent(5), AndOperator(), RoleComponent(7))
    outer_statement = Statement(inner_statement, ExclusiveOrOperator(), NumberOfRolesLimitComponent(3))

    user_1 = {
        5: True,
        7: False,
        11: True,
        13: True,
        15: False
    }
    assert not inner_statement.user_applies(user_1)
    assert outer_statement.user_applies(user_1)

    user_2 = {
        5: True,
        7: True,
    }
    assert inner_statement.user_applies(user_2)
    assert not outer_statement.user_applies(user_2)