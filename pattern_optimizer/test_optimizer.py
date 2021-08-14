import patterns.advanced_component as ac
import patterns.simple_component as sc
import patterns.operators as op
import patterns.comparators as cp
import patterns.optimizer as opt
import patterns.components as c
from logs.log import print
import time
import patterns.simple_discord as sd
import patterns.simple_discord as sd
import random
import pympler.asizeof as asizeof
GUILD = None


def test_init_guild_roles():
    global GUILD
    GUILD = generate_guild(100)


def create_list_of_numbers_in_range(bottom: int, top: int) -> list[int]:
    if (bottom == top):
        return [bottom]

    result = []

    while(bottom < top+1):
        result.append(bottom)
        bottom += 1
    return result


def optimizer_test_template(component: c.Component):
    global GUILD
    time_before = time.time()
    optimized = opt.optimize(component)
    time_after = time.time()
    optimize_time = time_after - time_before
    unoptimized_results: list[bool] = []
    optimized_results: list[bool] = []
    time_before = time.time()
    for member in GUILD.members():
        unoptimized_results.append(component.user_applies(member))
    time_after = time.time()
    unoptimized_eval_time = time_after - time_before

    time_before = time.time()
    for member in GUILD.members():
        optimized_results.append(optimized.user_applies(member))
    time_after = time.time()
    optimized_eval_time = time_after - time_before

    print(f"Unoptimized is\n{component.to_json()}")
    print(f"Optimized is\n{optimized.to_json()}")
    print(f"Optimizing took {optimize_time}")
    print(
        f"It took the unoptimized version {unoptimized_eval_time} to evalutate all 10000 members")
    print(
        f"It took the optimized version {optimized_eval_time} to evalutate all 10000 members")
    print(
        f"Size of unoptimized is {asizeof.asizeof(component)}")
    print(
        f"Size of optimized is {asizeof.asizeof(optimized)}")
    assert optimized_results == unoptimized_results


def generate_guild(amount: int) -> sd.SimpleGuild:
    members: list[sd.SimpleMember] = []
    everyone_role_id = random.randint(1, amount)
    guild_roles = create_list_of_numbers_in_range(1, amount)

    for _ in range(amount):
        user_roles: dict[int, bool] = {}
        for i in guild_roles:
            user_roles[i] = bool(random.randint(0, 1))
        member = sd.SimpleMember(user_roles, bool(random.randint(0, 1)))

        members.append(member)

    return sd.SimpleGuild(members, guild_roles, everyone_role_id)


def test_boolean_optimization():
    statement = ac.Statement(
        sc.BooleanComponent(True),
        op.AndOperator(),
        ac.Statement(
            sc.BooleanComponent(True),
            op.AndOperator(),
            ac.Statement(
                sc.BooleanComponent(True),
                op.AndOperator(),
                ac.Statement(
                    sc.BooleanComponent(True),
                    op.AndOperator(),
                    ac.Statement(
                        sc.BooleanComponent(True),
                        op.AndOperator(),
                        sc.BooleanComponent(False)
                    )
                )
            )
        )
    )
    optimizer_test_template(statement)


def test_mixed_optimization():
    statement = ac.Statement(
        sc.BooleanComponent(True),
        op.ExclusiveOrOperator(),
        ac.Statement(
            sc.BooleanComponent(False),
            op.AndOperator(),
            ac.Statement(
                sc.BooleanComponent(True),
                op.AndOperator(),
                ac.Statement(
                    sc.BooleanComponent(True),
                    op.AndOperator(),
                    ac.Statement(
                        sc.BooleanComponent(True),
                        op.OrOperator(),
                        sc.BooleanComponent(False)
                    )
                )
            )
        )
    )
    optimizer_test_template(statement)


def test_reverse_component_optimization():
    statement = ac.Statement(
        ac.ReverseComponent(sc.RolesLimitComponent(
            cp.EqualToLimitComparator(5))),
        op.AndOperator(),
        sc.RolesLimitComponent(cp.EqualToLimitComparator(5))
    )
    optimizer_test_template(statement)


def test_role_limit_component_optimization():
    statement = ac.Statement(
        ac.Statement(
            sc.RolesLimitComponent(cp.GreaterThanOrEqualToLimitComparator(8)),
            op.NotExclusiveOrOperator(),
            sc.BooleanComponent(True)
        ),
        op.ExclusiveOrOperator(),
        ac.Statement(
            sc.RolesLimitComponent(cp.LessThanOrEqualToLimitComparator(11)),
            op.ExclusiveOrOperator(),
            sc.RolesLimitComponent(cp.LessThanOrEqualToLimitComparator(11))
        )
    )
    optimizer_test_template(statement)


def test_giant_component_optimization():
    statement = ac.Statement(
        sc.BooleanComponent(False),
        op.OrOperator(),
        ac.Statement(
            sc.RolesLimitComponent(cp.LessThanOrEqualToLimitComparator(1)),
            op.NotOrOperator(),
            ac.Statement(
                sc.RoleComponent(10),
                op.NotExclusiveOrOperator(),
                ac.Statement(
                    sc.BooleanComponent(True),
                    op.AndOperator(),
                    sc.RolesLimitComponent(
                        cp.LessThanOrEqualToLimitComparator(3))
                )
            )
        )
    )

    optimizer_test_template(statement)


def test_role_limit_component_optimization_extreme():
    statement = ac.Statement(
        sc.BooleanComponent(False),
        op.OrOperator(),
        ac.Statement(
            sc.RolesLimitComponent(cp.LessThanOrEqualToLimitComparator(15)),
            op.NotOrOperator(),
            ac.Statement(
                sc.RolesLimitComponent(
                    cp.GreaterThanOrEqualToLimitComparator(10)),
                op.NotExclusiveOrOperator(),
                ac.Statement(
                    sc.BooleanComponent(True),
                    op.AndOperator(),
                    sc.RolesLimitComponent(
                        cp.LessThanOrEqualToLimitComparator(3))
                )
            )
        )
    )
    optimizer_test_template(statement)


def test_role_limit_component_optimization_extreme_extreme():
    statement = ac.Statement(
        sc.RolesLimitComponent(cp.LessThanOrEqualToLimitComparator(15)),
        op.OrOperator(),
        ac.Statement(
            sc.RolesLimitComponent(cp.LessThanOrEqualToLimitComparator(15)),
            op.OrOperator(),
            ac.Statement(
                sc.RolesLimitComponent(
                    cp.GreaterThanOrEqualToLimitComparator(10)),
                op.OrOperator(),
                ac.Statement(
                    sc.BooleanComponent(True),
                    op.AndOperator(),
                    sc.RolesLimitComponent(
                        cp.LessThanOrEqualToLimitComparator(3))
                )
            )
        )
    )
    optimizer_test_template(statement)
