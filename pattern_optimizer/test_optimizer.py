from typing import Callable
from pattern_parser.pattern_error import PatternIsNotStrError
from pattern_parts.advanced_component import ReverseComponent, Statement
from pattern_parts.operators import AndOperator, ExclusiveOrOperator, NotAndOperator, NotExclusiveOrOperator, NotOrOperator, OrOperator
from pattern_parts.simple_component import BooleanComponent, BotComponent, RoleComponent, RolesLimitComponent
from pattern_parts.comparator_implementation import EqualToLimitComparator, GreaterThanLimitComparator, GreaterThanOrEqualToLimitComparator, LessThanLimitComparator, LessThanOrEqualToLimitComparator, NotEqualToLimitComparator
from pattern_optimizer.optimizer import optimize
from pattern_parser.simple_discord import SimpleGuild, SimpleMember
from pattern_parser.counting_channels import pattern_constructor
from pattern_parser.pattern import PatternParams
import random
from logs.log import print
import sys
from multiprocessing import Process
import time
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


def generate_guild(amount: int) -> SimpleGuild:
    members: list[SimpleMember] = []
    everyone_role_id = random.randint(1, amount)
    guild_roles = create_list_of_numbers_in_range(1, amount)

    for _ in range(amount):
        user_roles: dict[int, bool] = {}
        for i in guild_roles:
            user_roles[i] = bool(random.randint(0, 1))
        member = SimpleMember(
            user_roles, bool(random.randint(0, 1)))

        members.append(member)

    return SimpleGuild(members, guild_roles, everyone_role_id)


def template(pattern_1: str, pattern_2: str):
    params_1 = PatternParams(pattern_1, guild=GUILD)
    params_2 = PatternParams(pattern_2, guild=GUILD)
    component_1 = pattern_constructor(params_1)
    component_2 = pattern_constructor(params_2)
    assert GUILD.get_result(component_1) == GUILD.get_result(component_2)


def optimize_template(pattern: str):
    params = PatternParams(pattern, guild=GUILD)
    component = pattern_constructor(params)
    optimized = optimize(component)
    print(f"Component is {component}")
    print(f"Optimized component is {optimized}")
    assert GUILD.get_result(component) == GUILD.get_result(optimized)


def test_statement_optimize():
    statement = Statement(
        Statement(
            BooleanComponent(False),
            AndOperator(),
            BooleanComponent(True)
        ),
        ExclusiveOrOperator(),
        Statement(
            BooleanComponent(False),
            ExclusiveOrOperator(),
            BooleanComponent(True)
        )
    )
    print(statement.__repr__())
    assert optimize(statement) == BooleanComponent(True)


def test_statement_optimize_2():
    statement = Statement(
        Statement(
            Statement(
                BooleanComponent(True),
                NotExclusiveOrOperator(),
                Statement(
                    BooleanComponent(False),
                    AndOperator(),
                    BotComponent()
                )
            ),
            AndOperator(),
            Statement(
                RoleComponent(8),
                NotOrOperator(),
                RolesLimitComponent(
                    LessThanLimitComparator(5)
                )
            )
        ),
        ExclusiveOrOperator(),
        Statement(
            RolesLimitComponent(
                NotEqualToLimitComparator(3)
            ),
            ExclusiveOrOperator(),
            Statement(
                RolesLimitComponent(GreaterThanOrEqualToLimitComparator(1)),
                OrOperator(),
                BooleanComponent(False)
            )
        )
    )
    optimized = optimize(statement)
    print("ASDDADSD")
    print(optimized)
    assert GUILD.get_result(statement) == GUILD.get_result(optimized)


def work():
    my_number = 0
    for _ in range(100):
        my_number += random.randint(1, 1000)


def start_processes(amount: int, target: Callable):
    processes: list[Process] = []
    for _ in range(amount):
        process = Process(target=target)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()


def test_kill_system():
    start_time = time.time_ns()
    start_processes(1000, work)
    end_time = time.time_ns()
    delta_t = end_time-start_time
    delta_t /= 1000000
    print(f"Took {delta_t} miliseconds to finish all processes")