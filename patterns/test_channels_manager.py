from patterns.pattern_error import PatternError, SuccessfullyConstructedComponent
from patterns.channels_manager import read_from_file, write_to_file, init, create_component
from patterns.component import Component, RoleComponent
from channels_manager import gather_all_operators_and_components
from logs.log import print
from inspect import getmembers
from test_counting_channels import pattern_test_template, successful_pattern_test_template


def test_rw():
    init()
    component = pattern_test_template("(false,or,false)", False)
    write_to_file(component, 100, 200)
    retrieved_object = read_from_file(100, 200)
    assert component == retrieved_object


def test_update_guild():
    pass


def test_file_not_found():
    try:
        read_from_file(100, "I am not the name of a guild")
        assert False
    except FileNotFoundError:
        assert True


def create_component_template(pattern: str, should_fail: bool):
    everyone_role_id: int = 1
    list_of_roles: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    guild_id = 10000
    channel_id = 20000
    exception, _ = create_component(
        pattern, list_of_roles, everyone_role_id, guild_id, channel_id)
    print(f"{exception.__str__()}, {should_fail}")
    assert should_fail is not isinstance(
        exception, SuccessfullyConstructedComponent)


def test_create_component():
    create_component_template("(true, and, true)", False)
    create_component_template("(((", True)