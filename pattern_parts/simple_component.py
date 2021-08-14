from os import putenv
from typing import Union
import pattern_parts.operators as op
from pattern_parser.simple_discord import SimpleMember
from discord.enums import Enum
from pattern_parser.pattern_error import RoleNotInRolesError
import pattern_parts.components as c
import pattern_parts.advanced_component as ac
import pattern_parts.comparator as cp

from logs.log import print
import copy
SIMPLE_COMPONENT_REPR = {}


class SimpleComponent(c.Component):
    """
        Parent class for all simple components
        A simple component is a component that does not contain other components
    """

    def reverse(self) -> c.component:
        return ac.ReverseComponent(self)

    def optimize(self, super_component: c.component) -> c.component:
        simplified = self.simplify()
        if isinstance(super_component, ac.Statement):
            return simplified.optimize_statement(self, super_component)
        elif isinstance(super_component, ac.ReverseComponent):
            return simplified.reverse()
        return simplified

    def optimize_statement(self, statement: ac.Statement):
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

        if isinstance(operator, op.OrOperator):
            return simplified.or_optimize(other_component)
        if isinstance(operator, op.NotOrOperator):
            return simplified.nor_optimize(other_component)
        if isinstance(operator, op.AndOperator):
            return simplified.and_optimize(other_component)
        if isinstance(operator, op.NotAndOperator):
            return simplified.nand_optimize(other_component)
        if isinstance(operator, op.ExclusiveOrOperator):
            return simplified.xor_optimize(other_component)
        if isinstance(operator, op.NotExclusiveOrOperator):
            return simplified.nxor_optimize(other_component)

        raise ValueError

    def or_optimize(self, other: c.Component) -> c.Component:
        return ac.Statement(self, op.OrOperator(), other)

    def nor_optimize(self, other: c.Component) -> c.Component:
        return ac.Statement(self, op.NotOrOperator(), other)

    def and_optimize(self, other: c.Component) -> c.Component:
        return ac.Statement(self, op.AndOperator(), other)

    def nand_optimize(self, other: c.Component) -> c.Component:
        return ac.Statement(self, op.NotAndOperator(), other)

    def xor_optimize(self, other: c.Component) -> c.Component:
        return ac.Statement(self, op.ExclusiveOrOperator(), other)

    def nxor_optimize(self, other: c.Component) -> c.Component:
        return ac.Statement(self, op.NotExclusiveOrOperator(), other)


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

    def or_optimize(self, other: c.Component) -> c.Component:
        if not isinstance(other, RolesLimitComponent):
            return super().or_optimize(other)
        return self.__comparator.optimize(other, op.OrOperator())

    def nor_optimize(self, other: c.Component) -> c.Component:
        if not isinstance(other, RolesLimitComponent):
            return super().nor_optimize(other)
        return self.__comparator.optimize(other, op.NotOrOperator())

    def and_optimize(self, other: c.Component) -> c.Component:
        if not isinstance(other, RolesLimitComponent):
            return super().and_optimize(other)
        return self.__comparator.optimize(other, op.AndOperator())

    def nand_optimize(self, other: c.Component) -> c.Component:
        if not isinstance(other, RolesLimitComponent):
            return super().nand_optimize(other)
        return self.__comparator.optimize(other, op.NotAndOperator())

    def xor_optimize(self, other: c.Component) -> c.Component:
        if not isinstance(other, RolesLimitComponent):
            return super().xor_optimize(other)
        return self.__comparator.optimize(other, op.ExclusiveOrOperator())

    def nxor_optimize(self, other: c.Component) -> c.Component:
        if not isinstance(other, RolesLimitComponent):
            return super().nxor_optimize(other)
        output = self.__comparator.optimize(other, op.NotExclusiveOrOperator())
        return self.__comparator.optimize(other, op.NotExclusiveOrOperator())


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
