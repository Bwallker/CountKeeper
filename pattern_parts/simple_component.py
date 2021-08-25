from pattern_parts.operators import Operator, OrOperator, NotOrOperator, AndOperator, NotAndOperator, ExclusiveOrOperator, NotExclusiveOrOperator
from pattern_parser.simple_discord import SimpleMember
import pattern_parts.components as c
import pattern_parts.comparator as cp
from pattern_parts.advanced_component import Statement, ReverseComponent
from logs.log import print
import copy
SIMPLE_COMPONENT_REPR = {}


def optimize_same_components(first_component: c.Component, second_component: c.Component, operator: Operator) -> c.Component:
    if first_component != second_component:
        return None

    reverse = first_component.reverse()

    if isinstance(operator, OrOperator) or isinstance(operator, AndOperator):
        return first_component
    if isinstance(operator, NotOrOperator) or isinstance(operator, NotAndOperator):
        return reverse
    if isinstance(operator, ExclusiveOrOperator):
        return BooleanComponent(False)
    if isinstance(operator, NotExclusiveOrOperator):
        return BooleanComponent(True)


def optimize_oposite_components(operator: Operator) -> c.Component:

    if isinstance(operator, OrOperator) or isinstance(operator, NotAndOperator) or isinstance(operator, ExclusiveOrOperator):
        return BooleanComponent(True)
    else:
        return BooleanComponent(False)


class SimpleComponent(c.Component):
    """
        Parent class for all simple components
        A simple component is a component that does not contain other components
    """

    def reverse(self) -> c.component:
        return ReverseComponent(self)

    def optimize(self, super_component: c.component) -> tuple[c.component, bool]:
        simplified = self.simplify()
        if type(super_component) == Statement:
            return simplified.optimize_statement(super_component)
        elif type(super_component) == ReverseComponent:
            return simplified.reverse(), True
        return simplified, False

    def optimize_statement(self, statement: Statement) -> tuple[c.component, bool]:
        first_component = statement.first_component().simplify()
        operator = statement.operator()
        second_component = statement.second_component().simplify()
        other_component: c.Component
        simplified = self.simplify()
        if first_component == simplified:
            other_component = second_component
        elif second_component == simplified:
            other_component = first_component
        else:
            raise ValueError
        if first_component == second_component:
            return optimize_same_components(first_component, second_component, operator), True

        if first_component == second_component.reverse():
            return optimize_oposite_components(operator), True

        # FOR SOME REASON, the operator in the statement is of type <class 'operators.AndOperator'> and AndOperator in this module is of type <class 'pattern_parts.operators.AndOperator' >. I have probably spent over an hour debugging this shit, and for some stupid reason, python just will not let me have all the operator classes be the same between all modules. So I am comparing reprs here, since at least that is reliable, unlike the stupid module system in this god forsaken language
        if operator.__repr__() == "inclusive or":
            return simplified.or_optimize(other_component)

        if operator.__repr__() == "not inclusive or":
            return simplified.nor_optimize(other_component)
        if operator.__repr__() == "and":
            return simplified.and_optimize(other_component)
        if operator.__repr__() == "not and":
            return simplified.nand_optimize(other_component)
        if operator.__repr__() == "exclusive or":
            return simplified.xor_optimize(other_component)
        if operator.__repr__() == "not exclusive or":
            return simplified.nxor_optimize(other_component)
        raise ValueError

    def or_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        return Statement(self, OrOperator(), other), False

    def nor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        return Statement(self, NotOrOperator(), other), False

    def and_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        return Statement(self, AndOperator(), other), False

    def nand_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        return Statement(self, NotAndOperator(), other), False

    def xor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        return Statement(self, ExclusiveOrOperator(), other), False

    def nxor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        return Statement(self, NotExclusiveOrOperator(), other), False


class RolesLimitComponent(SimpleComponent):

    def __init__(self, comparator: cp.Comparator, role_limit: int = None):
        self.__comparator = comparator
        if role_limit is None:
            self.__comparator = comparator
            return
        self.__comparator = type(comparator)(role_limit)

    def user_applies(self, member: SimpleMember) -> bool:
        roles = member.roles()
        number_of_roles: int = 0
        for role in roles:
            if roles[role]:
                number_of_roles += 1
        return self.__comparator.comparison(number_of_roles)

    def comparator(self):
        return copy.copy(self.__comparator)

    def __repr__(self) -> str:
        return self.__comparator.__repr__()

    def reverse(self) -> c.component:
        return RolesLimitComponent(self.__comparator.reverse())

    def simplify(self) -> c.component:
        return RolesLimitComponent(self.__comparator.simplify())

    def or_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if not isinstance(other, RolesLimitComponent):
            return super().or_optimize(other)
        return self.__comparator.optimize(other.comparator(), OrOperator())

    def nor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        result = self.or_optimize(other)
        new_result = result[0].reverse(), result[1]
        return new_result

    def and_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if not isinstance(other, RolesLimitComponent):
            return super().and_optimize(other)
        return self.__comparator.optimize(other.comparator(), AndOperator())

    def nand_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        result = self.and_optimize(other)

        new_result = result[0].reverse(), result[1]
        return new_result

    def xor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if not isinstance(other, RolesLimitComponent):
            return super().xor_optimize(other)
        return self.__comparator.optimize(other.comparator(), ExclusiveOrOperator())

    def nxor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        result = self.xor_optimize(other)
        new_result = result[0].reverse(), result[1]
        return new_result

    def __ge__(self, other):
        if type(other) != type(self):
            return False
        return self.comparator() >= other.comparator()


class BooleanComponent(SimpleComponent):
    def __init__(self, boolean: bool = None) -> None:
        self.__boolean = boolean

    def user_applies(self, member: SimpleMember) -> bool:
        return self.__boolean

    def boolean(self):
        return self.__boolean

    def __repr__(self) -> str:
        if self.__boolean:
            return "true"
        return "false"

    def reverse(self) -> c.component:
        return BooleanComponent(not self.__boolean)

    def or_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if self.__boolean:
            return BooleanComponent(True), True
        return other, True

    def nor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if self.__boolean:
            return BooleanComponent(False), True
        else:
            return other.reverse(), True

    def and_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if self.__boolean:
            return other, True
        else:
            return BooleanComponent(False), True

    def nand_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if self.__boolean:
            return other.reverse(), True
        else:
            return BooleanComponent(True), True

    def xor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if self.__boolean:
            return other.reverse(), True
        else:
            return other, True

    def nxor_optimize(self, other: c.Component) -> tuple[c.Component, bool]:
        if self.__boolean:
            return other, True
        else:
            return other.reverse(), True


class RoleNotInRolesError(Exception):
    """
        Exception that gets thrown if a role in a statement is not a part of the roles of the guild
        Generally means that a pattern has not been properly cleaned up after a role was deleted
    """


class RoleComponent(SimpleComponent):
    def __init__(self, role_id: int = None) -> None:
        self.__role_id = role_id

    def user_applies(self, member: SimpleMember) -> bool:
        roles = member.roles()
        if not self.__role_id in roles:
            raise RoleNotInRolesError
        return roles.get(self.__role_id)

    def role_id(self):
        return self.__role_id

    def __repr__(self) -> str:
        return f"<@&{self.__role_id}>"


class BotComponent(SimpleComponent):
    def __init__(self):
        pass

    def user_applies(self, member: SimpleMember) -> bool:
        return member.is_bot()

    def __repr__(self) -> str:
        return "bot"
