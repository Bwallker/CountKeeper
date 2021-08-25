import pattern_parts.components as components
import pattern_parser.simple_discord as simple_discord
from pattern_parts.operators import Operator, OrOperator, NotOrOperator, AndOperator, NotAndOperator, ExclusiveOrOperator, NotExclusiveOrOperator
import copy
import typing
from logs.log import print


class AdvancedComponent(components.Component):
    """
        Parent class for all advanced components
        An advanced component is a component that contains other components

    """

    def reverse(self) -> components.component:
        return ReverseComponent(self)


class ReverseComponent(AdvancedComponent):
    __component: components.Component

    def __init__(self, super_component: components.Component = None) -> None:
        self.__component = super_component

    def user_applies(self, member: simple_discord.SimpleMember) -> bool:
        return not self.__component.user_applies(member)

    def component(self):
        return copy.deepcopy(self.__component)

    def __repr__(self) -> str:
        return f"not {self.__component.__repr__()}"

    def optimize(self, super_component: component) -> tuple[component, bool]:
        output = self.__component.reverse()
        if super_component == None:
            return output, not isinstance(output, ReverseComponent)

        if isinstance(super_component, Statement):
            other_component: components.Component
            first_component = super_component.first_component()
            second_component = super_component.second_component()
            if first_component == self:
                other_component = second_component
            elif second_component == self:
                other_component = first_component
            else:
                raise ValueError

            return Statement(
                output,
                super_component.operator(),
                other_component
            ), not isinstance(output, ReverseComponent)

    def reverse(self) -> components.component:
        return self.__component


statement = typing.TypeVar("statement", bound="Statement")


class Statement(AdvancedComponent):

    def __init__(self, first_component: components.Component = None, operator: Operator = None, second_component: components.Component = None) -> None:
        self.__first_component = first_component
        self.__operator = operator
        self.__second_component = second_component

    def user_applies(self, member: simple_discord.SimpleMember) -> bool:
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

    def reverse(self) -> components.component:
        return Statement(self.__first_component, self.__operator.get_reverse_operator(), self.__second_component)

    def optimize(self, super_component: components.component) -> tuple[components.component, bool]:
        new_statement, changes_were_made = self.__first_component.optimize(
            self)
        if changes_were_made:
            if isinstance(self.__first_component, Statement):
                return Statement(
                    new_statement,
                    self.__operator,
                    self.__second_component
                ), True
            return new_statement, True
        new_statement, changes_were_made = self.__second_component.optimize(
            self)
        if changes_were_made:
            if isinstance(self.__second_component, Statement):
                return Statement(
                    self.__first_component,
                    self.__operator,
                    new_statement
                ), True
            return new_statement, True
        return self.optimize_away_duplicate_components()

    def __eq__(self, other):
        if super().__eq__(other):
            return True
        if isinstance(other, Statement):
            return other.first_component() == self.__second_component and other.second_component() == self.__first_component
        return False

    def optimize_away_duplicate_components(self) -> tuple[statement, bool]:
        """
        This function removes all the dead components later up the tree that come after that component has already been evaluated earlier in the tree by an OR or AND operator

        For example:
        Statement(
            RolesLimitComponent(
                LessThanLimitComparator(16)
            ),
            NotAndOperator(),
            Statement(
                RolesLimitComponent(
                    LessThanLimitComparator(16)
                ),
                NotAndOperator(),
                RoleComponent(100)
            )
        )


        Here the second RolesLimitComponent is redundant since if the first one evaluates to true, the result of the second doesn't matter since the pattern has already been resolved
        So the result of the second one only matters if it is false, which means that it can be replaced with a false boolean component, since it is functionally the same
        And that boolean will then get cleaned up at the next iteration through the optimizer
        """
        return self.optimize_away_duplicate_components_helper([])

    def optimize_away_duplicate_components_helper(self, components_so_far: list[tuple[components.Component, Operator]]) -> tuple[statement, bool]:
        import pattern_parts.simple_component as simple_component
        changes_were_made = False

        first_component = self.first_component()
        operator = self.operator()
        second_component = self.second_component()

        first_component_in_components_so_far: bool = False

        first_component_operator: Operator

        second_component_in_components_so_far: bool = False

        second_component_operator: Operator
        for component in components_so_far:
            if component[0] == first_component:
                first_component_in_components_so_far = True
                first_component_operator = component[1]
                break
            if component[0].reverse() == first_component:
                first_component_in_components_so_far = True
                if type(component[1]) == AndOperator or type(component[1]) == NotAndOperator:
                    first_component_operator = OrOperator()
                elif type(component[1]) == OrOperator or type(component[1]) == NotOrOperator:
                    first_component_operator = AndOperator()
                else:
                    first_component_operator = component[1]

        for component in components_so_far:
            if component[0] == second_component:
                second_component_in_components_so_far = True
                second_component_operator = component[1]
                break
            if component[0].reverse() == second_component:
                second_component_in_components_so_far = True
                if type(component[1]) == AndOperator or type(component[1]) == NotAndOperator:
                    second_component_operator = OrOperator()
                elif type(component[1]) == OrOperator or type(component[1]) == NotOrOperator:
                    second_component_operator = AndOperator()
                else:
                    second_component_operator = component[1]
                break

        if first_component_in_components_so_far:
            if isinstance(first_component_operator, AndOperator) or isinstance(first_component_operator, NotAndOperator):
                first_component = simple_component.BooleanComponent(True)
                changes_were_made = True
            elif isinstance(first_component_operator, OrOperator) or isinstance(first_component_operator, NotOrOperator):
                first_component = simple_component.BooleanComponent(False)
                changes_were_made = True

        else:
            components_so_far.append((first_component, operator))
        if second_component_in_components_so_far:
            if isinstance(second_component_operator, AndOperator) or isinstance(second_component_operator, NotAndOperator):
                second_component = simple_component.BooleanComponent(True)
                changes_were_made = True
            elif isinstance(second_component_operator, OrOperator) or isinstance(second_component_operator, NotOrOperator):
                second_component = simple_component.BooleanComponent(False)
                changes_were_made = True
        else:
            components_so_far.append((second_component, operator))

        if isinstance(first_component, Statement):
            first_component, first_component_changes_made = first_component.optimize_away_duplicate_components_helper(
                copy.deepcopy(components_so_far))
            if first_component_changes_made:
                changes_were_made = True
        if isinstance(second_component, Statement):
            second_component, second_component_changes_made = second_component.optimize_away_duplicate_components_helper(
                copy.deepcopy(components_so_far))
            if second_component_changes_made:
                changes_were_made = True

        return Statement(first_component, operator, second_component), changes_were_made
