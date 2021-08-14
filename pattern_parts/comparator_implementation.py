from abc import ABC, abstractmethod
import pattern_parts.operators as operators
from logs.log import print
import pattern_parts.components as components
import pattern_optimizer.type_agnostic_functions as type_agnostic_functions
import pattern_parts.simple_component as sc
import pattern_parts.comparator as comparator
import dataclasses
import pattern_parts.simple_component as simple_component
import pattern_parts.advanced_component as advanced_component


@dataclasses.dataclass
class OptimizeParameters:
    bigger_limit: int
    smaller_limit: int
    self_limit: int
    other_limit: int
    other: comparator.Comparator
    operator: operators.Operator


def optimize_operators(or_response: components.Component, and_response: components.Component, xor_response: components.Component, operator: operators.Operator):
    if isinstance(operator, operators.OrOperator):
        try:
            return or_response.simplify()
        except AttributeError:
            return None
    if isinstance(operator, operators.NotOrOperator):
        try:
            return or_response.reverse()
        except AttributeError:
            return None
    if isinstance(operator, operators.AndOperator):
        try:
            return and_response.simplify()
        except AttributeError:
            return None
    if isinstance(operator, operators.NotAndOperator):
        try:
            return and_response.reverse()
        except AttributeError:
            return None
    if isinstance(operator, operators.ExclusiveOrOperator):
        try:
            return xor_response.simplify()
        except AttributeError:
            return None
    if isinstance(operator, operators.NotExclusiveOrOperator):
        try:
            return xor_response.reverse()
        except AttributeError:
            return None


class ComparatorImplementation(comparator.Comparator):
    def optimize(self, other: comparator.Comparator, operator: operators.Operator) -> components.Component:
        simplified: ComparatorImplementation = self.simplify()
        other_simplified = other.simplify()
        params = OptimizeParameters(max(simplified._role_limit, other_simplified._role_limit), min(
            simplified._role_limit, other_simplified._role_limit), simplified._role_limit, other_simplified._role_limit, other_simplified, operator)
        if simplified == other_simplified:
            return type_agnostic_functions.optimize_same_components(simple_component.RolesLimitComponent(simplified), simple_component.RolesLimitComponent(other_simplified), operator)
        if simplified == other_simplified.reverse():
            return type_agnostic_functions.optimize_oposite_components(operator)

        if isinstance(operator, operators.AndOperator):
            if simplified.role_limit() == other_simplified.role_limit():
                if type(simplified) != type(other_simplified):
                    return sc.BooleanComponent(False)
        if isinstance(operator, operators.NotAndOperator):
            if simplified.role_limit() == other_simplified.role_limit():
                if type(simplified) != type(other_simplified):
                    return sc.BooleanComponent(True)

        if type(simplified) == type(other_simplified):
            result = simplified.optimize_same_type(params)
        elif type(self) == type(other.reverse()):
            result = simplified.optimize_oposite_type(params)
        elif isinstance(params.other, EqualToLimitComparator):
            result = self.eq_optimize(params)
        elif isinstance(params.other, NotEqualToLimitComparator):
            result = self.neq_optimize(params)
        else:
            result = simplified.continue_optimize(params)
        if result is not None:
            return result
        return advanced_component.Statement(sc.RolesLimitComponent(self), operator, sc.RolesLimitComponent(other))

    def continue_optimize(self, params: OptimizeParameters) -> components.Component:
        return advanced_component.Statement(self, params.operator, params.other)

    def eq_optimize(self, params: OptimizeParameters) -> components.Component:
        return advanced_component.Statement(self, params.operator, params.other)

    def neq_optimize(self, params: OptimizeParameters) -> components.Component:
        return advanced_component.Statement(self, params.operator, params.other)

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        return advanced_component.Statement(self, params.operator, params.other)

    def optimize_oposite_type(self, params: OptimizeParameters) -> components.Component:
        params.self_limit, params.other_limit = params.other_limit, params.self_limit
        params.other = self
        return self.reverse().optimize_oposite_type(params)


class LessThanLimitComparator(ComparatorImplementation):
    def comparison(self, number: int):
        return number < self._role_limit

    def eq_optimize(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit == params.other_limit:
            """
            (< 5, or, = 5)
            (< 5, and, = 5)
            (< 5, xor, = 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(
                    LessThanOrEqualToLimitComparator(params.self_limit)),
                sc.BooleanComponent(False),
                sc.RolesLimitComponent(
                    LessThanOrEqualToLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit + 1 == params.other_limit:
            """
            (< 6, or, = 5)
            (< 6, and, = 5)
            (< 6, xor, = 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit-1)),
                params.operator
            )
        if params.self_limit > params.other_limit:
            """
            (< 10, or, = 5)
            (< 10, and, = 5)
            (< 10, xor, = 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                None,
                params.operator
            )
        if params.self_limit < params.other_limit:
            """
            (< 5, or, = 10)
            (< 5, and, = 10)
            (< 5, xor, = 10)
            """
            return optimize_operators(
                None,
                sc.BooleanComponent(False),
                None,
                params.operator
            )

    def neq_optimize(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit == params.other_limit:
            """
            (< 5, or, != 5)
            (< 5, and, != 5)
            (< 5, xor, != 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(
                    GreaterThanLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit + 1 == params.other_limit:
            """
            (< 6, or, != 5)
            (< 6, and, != 5)
            (< 6, xor, != 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit-1)),
                sc.RolesLimitComponent(
                    GreaterThanLimitComparator(params.self_limit-2)),
                params.operator
            )
        if params.self_limit > params.other_limit:
            """
            (< 10, or, != 5)
            (< 10, and, != 5)
            (< 10, xor, != 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(params.other),
                None,
                None,
                params.operator
            )
        if params.self_limit < params.other_limit:
            """
            (< 5, or, != 10)
            (< 5, and, != 10)
            (< 5, xor, != 10)
            """
            return optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(self),
                None,
                params.operator
            )

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        return optimize_operators(
            sc.RolesLimitComponent(
                LessThanLimitComparator(params.bigger_limit)),
            sc.RolesLimitComponent(
                LessThanLimitComparator(params.smaller_limit)),
            None,
            params.operator
        )

    def optimize_oposite_type(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit < params.other_limit:
            return optimize_operators(
                None,
                sc.BooleanComponent(False),
                None,
                params.operator
            )
        if params.self_limit == params.other_limit:
            """

                (< 5, or , > 5)
                (< 5, nor, > 5)

                (< 5, and , > 5)
                (< 5, nand, > 5)

                (< 5, xor, > 5)
                (< 5, nxor, > 5)

                Incase you want to think it through yourself
            """
            return optimize_operators(
                sc.RolesLimitComponent(
                    NotEqualToLimitComparator(params.other_limit)),
                sc.RolesLimitComponent(
                    NotEqualToLimitComparator(params.other_limit)),
                None,
                params.operator
            )
        if params.self_limit == params.other_limit + 2:
            """

                (< 7, or, > 5)
                (< 7, nor, > 5)

                (< 7, and, > 5)
                (< 7, nand, > 5)

                (< 7, xor, > 5)
                (< 7, nxor, > 5)


                Incase you want to think it through yourself
            """
            return optimize_operators(
                sc.BooleanComponent(True),
                sc.RolesLimitComponent(
                    EqualToLimitComparator(params.other_limit+1)),
                sc.RolesLimitComponent(
                    NotEqualToLimitComparator(params.other_limit+1)),
                params.operator
            )
        if params.self_limit > params.other_limit:
            """

                (< 8, or, > 5)
                (< 8, nor, > 5)

                (< 8, and, > 5)
                (< 8, nand, > 5)

                (< 8, xor, > 5)
                (< 8, nxor, > 5)


                Incase you want to think it through yourself
            """
            return optimize_operators(
                sc.BooleanComponent(True),
                None,
                None,
                params.operator
            )


class LessThanOrEqualToLimitComparator(ComparatorImplementation):
    def comparison(self, number: int):
        return number <= self._role_limit

    def simplify(self) -> comparator:
        return LessThanLimitComparator(self._role_limit+1)


class GreaterThanLimitComparator(ComparatorImplementation):
    def comparison(self, number: int):
        return number > self._role_limit

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        """
            (> 10, or, > 16)
            (> 10, and, > 16)
            (> 10, xor, > 16)

            """
        return optimize_operators(
            sc.RolesLimitComponent(
                GreaterThanLimitComparator(params.smaller_limit)),
            sc.RolesLimitComponent(
                GreaterThanLimitComparator(params.bigger_limit)),
            None,
            params.operator
        )

    def eq_optimize(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit == params.other_limit:
            """
            (> 5, or, = 5)
            (> 5, and, = 5)
            (> 5, xor, = 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(
                    GreaterThanOrEqualToLimitComparator(params.self_limit)),
                sc.BooleanComponent(False),
                sc.RolesLimitComponent(
                    GreaterThanOrEqualToLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit + 1 == params.other_limit:
            """
            (< 6, or, = 5)
            (< 6, and, = 5)
            (< 6, xor, = 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit-1)),
                params.operator
            )
        if params.self_limit > params.other_limit:
            """
            (< 10, or, = 5)
            (< 10, and, = 5)
            (< 10, xor, = 5)
            """
            return optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                None,
                params.operator
            )
        if params.self_limit < params.other_limit:
            """
            (< 5, or, = 10)
            (< 5, and, = 10)
            (< 5, xor, = 10)
            """
            return optimize_operators(
                None,
                sc.BooleanComponent(False),
                None,
                params.operator
            )


class GreaterThanOrEqualToLimitComparator(ComparatorImplementation):
    def comparison(self, number: int):
        return number >= self._role_limit

    def simplify(self) -> comparator:
        return GreaterThanLimitComparator(self._role_limit-1)


class EqualToLimitComparator(ComparatorImplementation):
    def comparison(self, number: int) -> bool:
        return number == self._role_limit


class NotEqualToLimitComparator(ComparatorImplementation):
    def comparison(self, number: int) -> bool:
        return number != self._role_limit


comparator.COMPARATORS_REPRS = {
    LessThanLimitComparator: "<",
    LessThanOrEqualToLimitComparator: "<=",
    GreaterThanLimitComparator: ">",
    GreaterThanOrEqualToLimitComparator: ">=",
    EqualToLimitComparator: "=",
    NotEqualToLimitComparator: "=/="
}

comparator.REVERSE_COMPARATORS = {
    LessThanLimitComparator: GreaterThanOrEqualToLimitComparator,
    LessThanOrEqualToLimitComparator: GreaterThanLimitComparator,
    EqualToLimitComparator: NotEqualToLimitComparator,
}
