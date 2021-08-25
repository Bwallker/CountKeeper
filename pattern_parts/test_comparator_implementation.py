from pattern_parser.simple_discord import SimpleGuild
from pattern_parts.simple_component import RolesLimitComponent
import pattern_parts.advanced_component as advanced
from pattern_parts.comparator import Comparator
import pattern_parts.comparator_implementation as comparators
import pattern_parser.simple_discord as simple_discord
import random
import pattern_parts.operators as operators
from logs.log import print
GUILD: SimpleGuild


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


"""def optimizer_test_template(component: c.Component):
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
    assert optimized_results == unoptimized_results"""


def generate_guild(amount: int) -> simple_discord.SimpleGuild:
    members: list[simple_discord.SimpleMember] = []
    everyone_role_id = random.randint(1, amount)
    guild_roles = create_list_of_numbers_in_range(1, amount)

    for _ in range(amount):
        user_roles: dict[int, bool] = {}
        for i in guild_roles:
            user_roles[i] = bool(random.randint(0, 1))
        member = simple_discord.SimpleMember(
            user_roles, bool(random.randint(0, 1)))

        members.append(member)

    return simple_discord.SimpleGuild(members, guild_roles, everyone_role_id)


def test_less_than_limit_comparator():
    comparator = comparators.LessThanLimitComparator(5)
    assert comparator.comparison(4)
    assert not comparator.comparison(5)


def test_comparator_repr():
    assert comparators.GreaterThanLimitComparator(5).__repr__() == "> 5"


def test_reverse_comparator():
    assert comparators.GreaterThanLimitComparator(
        5).reverse() == comparators.LessThanLimitComparator(6)

    assert comparators.EqualToLimitComparator(
        5).reverse() == comparators.NotEqualToLimitComparator(5)


def test_simplify_comparator():
    assert comparators.GreaterThanOrEqualToLimitComparator(
        5).simplify() == comparators.GreaterThanLimitComparator(4)
    assert comparators.EqualToLimitComparator(
        5).simplify() == comparators.EqualToLimitComparator(5)


def random_operator() -> operators.Operator:
    return random.choice((operators.OrOperator, operators.NotOrOperator, operators.AndOperator, operators.NotAndOperator, operators.ExclusiveOrOperator, operators.NotExclusiveOrOperator))()


def random_comparator(role_limit: int) -> comparators.ComparatorImplementation:
    return random.choice((comparators.LessThanLimitComparator, comparators.LessThanOrEqualToLimitComparator, comparators.GreaterThanLimitComparator,
                          comparators.GreaterThanOrEqualToLimitComparator, comparators.EqualToLimitComparator, comparators.NotEqualToLimitComparator))(role_limit)


def test_failed_test():
    first_component = RolesLimitComponent(comparators.LessThanOrEqualToLimitComparator(
        0))
    second_component = RolesLimitComponent(
        comparators.NotEqualToLimitComparator(0))
    operator = operators.NotAndOperator()
    statement = advanced.Statement(first_component, operator, second_component)
    optimized_statement_1, _ = first_component.optimize(statement)
    optimized_statement_2, _ = second_component.optimize(statement)
    print(optimized_statement_1)
    print(optimized_statement_2)
    assert GUILD.get_result(statement) == GUILD.get_result(
        optimized_statement_1)
    assert GUILD.get_result(statement) == GUILD.get_result(
        optimized_statement_2)

    """(<= 0, nand, != 0)"""


def test_optimize():
    """
    for _ in range(100):
        print("NEW ITERATION")
        role_limit_1 = random.randint(0, 100)
        first_comparator = random_comparator(role_limit_1)
        role_limit_2 = random.choice((role_limit_1, role_limit_1+1, role_limit_1-1,
                                      role_limit_1+2, role_limit_1-2, role_limit_1+5, role_limit_1-5))
        if role_limit_2 < 0:
            role_limit_2 = 0
        second_comparator = random_comparator(role_limit_2)

        operator = random_operator()

        statement = advanced.Statement(RolesLimitComponent(
            first_comparator), operator, RolesLimitComponent(second_comparator))
        first_component = RolesLimitComponent(first_comparator)
        second_component = RolesLimitComponent(second_comparator)
        print(f"Unoptimized statement is {statement}")
        print(f"First component is {first_component}")
        print(f"Operator is {operator}")
        print(f"Second component is {second_component}")
        optimized_statement_1, _ = first_component.optimize(
            statement)
        print(f"First optimised is {optimized_statement_1}")
        optimized_statement_2, _ = second_component.optimize(
            statement)
        print(f"Second optimised is {optimized_statement_2}")
        assert GUILD.get_result(statement) == GUILD.get_result(
            optimized_statement_1)
        assert GUILD.get_result(statement) == GUILD.get_result(
            optimized_statement_2)
    """