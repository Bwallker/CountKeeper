from abc import ABC, abstractmethod
from patterns.pattern_error import *
from json import JSONEncoder, dumps


class ComponentEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__()


class Component(ABC):
    @abstractmethod
    def __init__(self):
        """
            Dummy constructor because otherwise my fucky auto-importing of components and operators in channels_file_managers won't work
        """
    @abstractmethod
    def user_applies(self, roles: dict[int, bool]) -> bool:
        """
            Abstract method that gets called when a Statement wants to know if a user applies to a component
        """
    @abstractmethod
    def __dict__(self):
        """
            Returns dictionary representation of component
        """
        return "a"

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__())

    def __eq__(self, other):
        if type(self).__name__ != type(other).__name__:
            return False
        try:
            self_annotatations = self.__annotations__
            other_annotations = other.__annotations__
        except AttributeError:
            return True
        self_instance_variables = {}
        other_instance_variables = {}
        for annotation in self_annotatations:
            value = getattr(self, annotation)
            self_instance_variables[annotation] = value
        for annotation in other_annotations:
            value = getattr(other, annotation)
            other_instance_variables[annotation] = value
        return self_instance_variables == other_instance_variables


class SimpleComponent(Component):
    """
        Parent class for all simple components
        A simple component is a component that does not contain other components
    """


class AdvancedComponent(Component):
    """
        Parent class for all advanced components
        An advanced component is a component that contains other components

    """


class NumberOfRolesLimitComponent(SimpleComponent):
    _roles_limit: int

    def __init__(self, roles_limit: int = None):
        self._roles_limit = roles_limit

    def user_applies(self, roles: dict[int, bool]) -> bool:
        number_of_roles: int = 0
        for role in roles:
            if roles[role]:
                number_of_roles += 1
        return number_of_roles <= self._roles_limit

    def __dict__(self):
        return {
            "type": type(self).__name__,
            "_roles_limit": self._roles_limit
        }


class BooleanComponent(SimpleComponent):
    _boolean: bool

    def __init__(self, boolean: bool = None) -> None:
        self._boolean = boolean

    def user_applies(self, roles: dict[int, bool]) -> bool:
        return self._boolean

    def __dict__(self):
        return {
            "type": type(self).__name__,
            "_boolean": self._boolean
        }


class RoleComponent(SimpleComponent):
    _role_id: int

    def __init__(self, role_id: int = None) -> None:
        self._role_id = role_id

    def user_applies(self, roles: dict[int, bool]) -> bool:
        if not self._role_id in roles:
            raise RoleNotInRolesError
        return roles.get(self._role_id)

    def __dict__(self):
        return {
            "type": type(self).__name__,
            "_role_id": self._role_id
        }


class ReverseComponent(AdvancedComponent):
    _super_component: Component

    def __init__(self, super_component: Component = None) -> None:
        self._super_component = super_component

    def user_applies(self, roles: dict[int, bool]) -> bool:
        return not self._super_component.user_applies(roles)

    def __dict__(self):
        return {
            "type": type(self).__name__,
            "_super_component": self._super_component.__dict__()
        }
