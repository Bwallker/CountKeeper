from abc import abstractmethod
from patterns.pattern_error import MoreOpeningThanClosingParenthesesError, NotValidSimpleComponentError
from patterns.counting_channels import PatternError, pattern_constructor, operators
from logs.log import print
import json
import channels_manager
from inspect import getmembers
def pattern_test_template(pattern: str, should_fail: bool = True, error: PatternError = PatternError):
    global operators
    list_of_roles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    everyone_role_id = 1
    try:
        result = pattern_constructor(pattern, list_of_roles, operators, everyone_role_id)
        assert not should_fail
        return result
    except error as e:
        print(e)
        assert should_fail

def successful_pattern_test_template(pattern: str, as_dict: dict=None):
    component = pattern_test_template(pattern, False)
    channels_manager.init()
    component_dict = component.__dict__()
    recovered_object = channels_manager.from_dict(component_dict)
    print(recovered_object)
    print(json.dumps(recovered_object.__dict__(), indent=4))
    assert component == recovered_object
    if as_dict is not None:
        assert component_dict == as_dict
def test_pattern_verifier_1():
    pattern_test_template("I am a random string that has nothing to do with patterns")
    

def test_pattern_verifier_2():
    as_dict = {
    "type": "Statement",
    "first_component": {
        "type": "ReverseComponent",
        "_super_component": {
            "type": "NumberOfRolesLimitComponent",
            "_roles_limit": 1
        }
    },
    "operator": {
        "type": "AndOperator"
    },
    "second_component": {
        "type": "ReverseComponent",
        "_super_component": {
            "type": "RoleComponent",
            "_role_id": 2
        }
    }
}
    successful_pattern_test_template("(not 1,and,not aaa2a)", as_dict)

def test_pattern_verifier_3():
    as_dict = {
    "type": "RoleComponent",
    "_role_id": 1
}
    successful_pattern_test_template("aaa1a", as_dict)

def test_pattern_verifier_4():
    as_dict = {
    "type": "Statement",
    "first_component": {
        "type": "BooleanComponent",
        "_boolean": True
    },
    "operator": {
        "type": "AndOperator"
    },
    "second_component": {
        "type": "Statement",
        "first_component": {
            "type": "BooleanComponent",
            "_boolean": True
        },
        "operator": {
            "type": "AndOperator"
        },
        "second_component": {
            "type": "Statement",
            "first_component": {
                "type": "RoleComponent",
                "_role_id": 2
            },
            "operator": {
                "type": "AndOperator"
            },
            "second_component": {
                "type": "RoleComponent",
                "_role_id": 3
            }
        }
    }
}
    successful_pattern_test_template("(true, and, (true, and, (aaa2a, and, aaa3a)))", as_dict)

def test_pattern_verifier_5():
    as_dict = {
    "type": "Statement",
    "first_component": {
        "type": "BooleanComponent",
        "_boolean": False
    },
    "operator": {
        "type": "OrOperator"
    },
    "second_component": {
        "type": "Statement",
        "first_component": {
            "type": "NumberOfRolesLimitComponent",
            "_roles_limit": 1
        },
        "operator": {
            "type": "NotOrOperator"
        },
        "second_component": {
            "type": "Statement",
            "first_component": {
                "type": "RoleComponent",
                "_role_id": 10
            },
            "operator": {
                "type": "NotExcluseOrOperator"
            },
            "second_component": {
                "type": "Statement",
                "first_component": {
                    "type": "BooleanComponent",
                    "_boolean": True
                },
                "operator": {
                    "type": "AndOperator"
                },
                "second_component": {
                    "type": "NumberOfRolesLimitComponent",
                    "_roles_limit": 3
                }
            }
        }
    }
}
    successful_pattern_test_template("(false, or,(1, not inclusive or,(aaa10a,not exclusive or,(true, and, 3))))", as_dict)

def test_pattern_verifier_6():
    pattern_test_template("((()", MoreOpeningThanClosingParenthesesError)

def test_pattern_verifier_7():
    pattern_test_template("a", NotValidSimpleComponentError)

def test_pattern_verifier_8():
    as_dict = {
    "type": "RoleComponent",
    "_role_id": 1
}
    successful_pattern_test_template("@everyone", as_dict)

def test_pattern_verifier_9():
    as_dict = {
    "type": "Statement",
    "first_component": {
        "type": "Statement",
        "first_component": {
            "type": "BooleanComponent",
            "_boolean": True
        },
        "operator": {
            "type": "AndOperator"
        },
        "second_component": {
            "type": "BooleanComponent",
            "_boolean": True
        }
    },
    "operator": {
        "type": "AndOperator"
    },
    "second_component": {
        "type": "Statement",
        "first_component": {
            "type": "BooleanComponent",
            "_boolean": True
        },
        "operator": {
            "type": "AndOperator"
        },
        "second_component": {
            "type": "BooleanComponent",
            "_boolean": True
        }
    },
}
    successful_pattern_test_template("((true, and, true), and, (true, and, true))", as_dict)

def test_pattern_verifier_10():
    as_dict = {
    "type": "Statement",
    "first_component": {
        "type": "Statement",
        "first_component": {
            "type": "Statement",
            "first_component": {
                "type": "RoleComponent",
                "_role_id": 1
            },
            "operator": {
                "type": "AndOperator"
            },
            "second_component": {
                "type": "RoleComponent",
                "_role_id": 3
            }
        },
        "operator": {
            "type": "NotExcluseOrOperator"
        },
        "second_component": {
            "type": "RoleComponent",
            "_role_id": 2
        }
    },
    "operator": {
        "type": "ExclusiveOrOperator"
    },
    "second_component": {
        "type": "Statement",
        "first_component": {
            "type": "NumberOfRolesLimitComponent",
            "_roles_limit": 1
        },
        "operator": {
            "type": "NotOrOperator"
        },
        "second_component": {
            "type": "Statement",
            "first_component": {
                "type": "NumberOfRolesLimitComponent",
                "_roles_limit": 1
            },
            "operator": {
                "type": "AndOperator"
            },
            "second_component": {
                "type": "NumberOfRolesLimitComponent",
                "_roles_limit": 3
            }
        }
    }
}

    successful_pattern_test_template("(((aaa1a, and, aaa3a), not exclusive or, aaa2a), exclusive or, (1, not or, (1, and, 3)))", as_dict)
    