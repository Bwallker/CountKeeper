from patterns.simple_discord import SimpleMember
from patterns.components import Component, component
from patterns.operators import Operator
import copy


class AdvancedComponent(Component):
    """
        Parent class for all advanced components
        An advanced component is a component that contains other components

    """

    def reverse(self) -> component:
        return ReverseComponent(self)

class ReverseComponent(AdvancedComponent):
    __component: Component

    def __init__(self, super_component: Component = None) -> None:
        self.__component = super_component

    def user_applies(self, member: SimpleMember) -> bool:
        return not self.__component.user_applies(member)

    def component(self):
        return copy.deepcopy(self.__component)

    def __repr__(self) -> str:
        return f"not {self.__component.__repr__()}"


class Statement(AdvancedComponent):

    def __init__(self, first_component: Component = None, operator: Operator = None, second_component: Component = None) -> None:
        self.__first_component = first_component
        self.__operator = operator
        self.__second_component = second_component

    def user_applies(self, member: SimpleMember) -> bool:
        first_component_applies = self.__first_component.user_applies(member)
        second_component_applies = self.__second_component.user_applies(member)
        return self.__operator.operation(first_component_applies, second_component_applies)

    def first_component(self):
        return copy.deepcopy(self.__first_component)

    def second_component(self):
        return copy.deepcopy(self.__second_component)

    def operator(self):
        return copy.copy(self.__operator)

    def __repr__(self) -> str:
        return f"({self.__first_component.__repr__()}, {self.__operator.__repr__()}, {self.__second_component.__repr__()})"
