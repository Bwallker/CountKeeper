from abc import ABC, abstractmethod
from patterns.component import AdvancedComponent, Component
from patterns.operators import Operator
from logs.log import print




class Statement (AdvancedComponent):
    first_component: Component
    operator: Operator
    second_component: Component
    def __init__(self, first_component: Component = None, operator: Operator = None, second_component: Component = None) -> None:
        self.first_component = first_component
        self.operator = operator
        self.second_component = second_component

    def user_applies(self, roles: dict[int, bool]) -> bool:
        first_component_applies = self.first_component.user_applies(roles)
        second_component_applies = self.second_component.user_applies(roles)
        return self.operator.operation(first_component_applies, second_component_applies)

    def __dict__(self):
        return {
            "type": type(self).__name__,
            "first_component": self.first_component.__dict__(),
            "operator": self.operator.__dict__(),
            "second_component": self.second_component.__dict__()
        }