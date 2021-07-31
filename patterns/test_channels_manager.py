from patterns.channels_manager import read_from_file, write_to_file, init
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