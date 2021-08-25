from abc import ABC, abstractmethod
import pattern_parts.operators as operators
import pattern_parts.components as components
import pattern_parts.simple_component as sc
import pattern_parts.comparator as comparator
import dataclasses
import pattern_parts.simple_component as simple_component
import pattern_parts.advanced_component as advanced_component
import pattern_optimizer.helpers as helpers
import copy
from logs.log import print


@dataclasses.dataclass
class OptimizeParameters:
    bigger_limit: int
    smaller_limit: int
    self_limit: int
    other_limit: int
    other: comparator.Comparator
    operator: operators.Operator


class ComparatorImplementation(comparator.Comparator):
    def optimize(self, other: comparator.Comparator, operator: operators.Operator) -> tuple[components.Component, bool]:
        simplified: ComparatorImplementation = self.simplify()
        other_simplified = other.simplify()
        params = OptimizeParameters(max(simplified._role_limit, other_simplified._role_limit), min(
            simplified._role_limit, other_simplified._role_limit), simplified._role_limit, other_simplified._role_limit, other_simplified, operator)
        if simplified == other_simplified:
            return simple_component.optimize_same_components(simple_component.RolesLimitComponent(simplified), simple_component.RolesLimitComponent(other_simplified), operator), True
        if simplified == other_simplified.reverse():
            return simple_component.optimize_oposite_components(operator), True

        if type(simplified) == type(other_simplified):
            result = simplified.optimize_same_type(params)
        elif type(simplified) == type(other_simplified.reverse()):
            result = simplified.optimize_oposite_type(params)
        elif isinstance(params.other, EqualToLimitComparator):
            result = simplified.eq_optimize(params)
        elif isinstance(params.other, NotEqualToLimitComparator):
            result = simplified.neq_optimize(params)
        else:
            result = simplified.continue_optimize(params)
        if result is None:
            return_value = advanced_component.Statement(sc.RolesLimitComponent(
                simplified), operator, sc.RolesLimitComponent(other_simplified)), False
        else:
            return_value = result, True
        return return_value

    def continue_optimize(self, params: OptimizeParameters) -> components.Component:
        return None

    def eq_optimize(self, params: OptimizeParameters) -> components.Component:
        return None

    def neq_optimize(self, params: OptimizeParameters) -> components.Component:
        return None

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        return None

    def optimize_oposite_type(self, params: OptimizeParameters) -> components.Component:
        params.self_limit, params.other_limit = params.other_limit, params.self_limit
        other = copy.deepcopy(params.other)
        params.other = self
        return other.optimize_oposite_type(params)


class LessThanLimitComparator(ComparatorImplementation):
    def comparison(self, number: int):
        return number < self._role_limit

    def __gt__(self, other: ComparatorImplementation):
        return self.role_limit() < other.role_limit()

    def eq_optimize(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit == params.other_limit:
            """
            (< 5, or, = 5)
            (< 5, and, = 5)
            (< 5, xor, = 5)
            """
            return helpers.optimize_operators(
                sc.RolesLimitComponent(
                    LessThanOrEqualToLimitComparator(params.self_limit)),
                sc.BooleanComponent(False),
                sc.RolesLimitComponent(
                    LessThanOrEqualToLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit - 1 == params.other_limit:
            """
            (< 6, or, = 5)
            (< 6, and, = 5)
            (< 6, xor, = 5)
            """
            return helpers.optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit - 1)),
                params.operator
            )
        if params.self_limit > params.other_limit:
            """
            (< 10, or, = 5)
            (< 10, and, = 5)
            (< 10, xor, = 5)
            """
            return helpers.optimize_operators(
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
            return helpers.optimize_operators(
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
            return helpers.optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(
                    GreaterThanLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit - 1 == params.other_limit:
            """
            (< 6, or, != 5)
            (< 6, and, != 5)
            (< 6, xor, != 5)
            """
            return helpers.optimize_operators(
                sc.BooleanComponent(True),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit - 1)),
                sc.RolesLimitComponent(
                    GreaterThanLimitComparator(params.self_limit - 2)),
                params.operator
            )
        if params.self_limit > params.other_limit:
            "params.self_limit > params.other_limit"
            """
            (< 10, or, != 5)
            (< 10, and, != 5)
            (< 10, xor, != 5)
            """
            return helpers.optimize_operators(
                sc.BooleanComponent(True),
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
            return helpers.optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(self),
                None,
                params.operator
            )

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        return helpers.optimize_operators(
            sc.RolesLimitComponent(
                LessThanLimitComparator(params.bigger_limit)),
            sc.RolesLimitComponent(
                LessThanLimitComparator(params.smaller_limit)),
            None,
            params.operator
        )

    def optimize_oposite_type(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit < params.other_limit:
            return helpers.optimize_operators(
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
            return helpers.optimize_operators(
                sc.RolesLimitComponent(
                    NotEqualToLimitComparator(params.other_limit)),
                sc.BooleanComponent(False),
                sc.RolesLimitComponent(
                    NotEqualToLimitComparator(params.self_limit)),
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
            return helpers.optimize_operators(
                sc.BooleanComponent(True),
                sc.RolesLimitComponent(
                    EqualToLimitComparator(params.other_limit + 1)),
                sc.RolesLimitComponent(
                    NotEqualToLimitComparator(params.other_limit + 1)),
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
            return helpers.optimize_operators(
                sc.BooleanComponent(True),
                None,
                None,
                params.operator
            )

    def continue_optimize(self, params: OptimizeParameters) -> components.Component:
        new_statement = advanced_component.Statement(
            sc.BooleanComponent(False),
            params.operator,
            sc.RolesLimitComponent(params.other)
        )
        if params.self_limit < 2:
            return sc.BooleanComponent(False).optimize(new_statement)[0]


class LessThanOrEqualToLimitComparator(ComparatorImplementation):
    def __gt__(self, other: ComparatorImplementation):
        return self.role_limit() < other.role_limit()

    def comparison(self, number: int):
        return number <= self._role_limit

    def simplify(self) -> comparator:
        return LessThanLimitComparator(self._role_limit+1)

    def optimize(self, other: comparator.Comparator, operator: operators.Operator) -> tuple[components.Component, bool]:
        return self.simplify().optimize(other, operator)[0], True


class GreaterThanLimitComparator(ComparatorImplementation):
    def __gt__(self, other: ComparatorImplementation):
        return self.role_limit() > other.role_limit()

    def comparison(self, number: int):
        return number > self._role_limit

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        """
            (> 10, or, > 16)
            (> 10, and, > 16)
            (> 10, xor, > 16)

            """
        return helpers.optimize_operators(
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
            return helpers.optimize_operators(
                sc.RolesLimitComponent(
                    GreaterThanOrEqualToLimitComparator(params.self_limit)),
                sc.BooleanComponent(False),
                sc.RolesLimitComponent(
                    GreaterThanOrEqualToLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit + 1 == params.other_limit:
            """
            (> 4, or, = 5)
            (> 4, and, = 5)
            (> 4, xor, = 5)
            """
            return helpers.optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(
                    GreaterThanLimitComparator(params.self_limit + 1)),
                params.operator
            )

        if params.self_limit < params.other_limit:
            """
            (> 5, or, = 10)
            (> 5, and, = 10)
            (> 5, xor, = 10)
            """
            return helpers.optimize_operators(
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(params.other),
                None,
                params.operator
            )
        if params.self_limit > params.other_limit:
            """
            (> 10, or, = 5)
            (> 10, and, = 5)
            (> 10, xor, = 5)
            """
            return helpers.optimize_operators(
                None,
                sc.BooleanComponent(False),
                None,
                params.operator
            )

    def neq_optimize(self, params: OptimizeParameters) -> components.Component:
        if params.self_limit == params.other_limit:
            """
            (> 5, or, != 5)
            (> 5, and, != 5)
            (> 5, xor, != 5)
            """
            return helpers.optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(self),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit)),
                params.operator
            )
        if params.self_limit + 1 == params.other_limit:
            """
            (> 4, or, != 5)
            (> 4, and, != 5)
            (> 4, xor, != 5)
            """
            return helpers.optimize_operators(
                sc.BooleanComponent(True),
                sc.RolesLimitComponent(
                    GreaterThanLimitComparator(params.self_limit + 1)),
                sc.RolesLimitComponent(
                    LessThanLimitComparator(params.self_limit + 2)),
                params.operator
            )
        if params.self_limit < params.other_limit:
            """
            (> 5, or, != 10)
            (> 5, and, != 10)
            (> 5, xor, != 10)
            """
            return helpers.optimize_operators(
                sc.BooleanComponent(True),
                None,
                None,
                params.operator
            )
        if params.self_limit > params.other_limit:
            """
            (> 10, or, != 5)
            (> 10, and, != 5)
            (> 10, xor, != 5)
            """
            return helpers.optimize_operators(
                sc.RolesLimitComponent(params.other),
                sc.RolesLimitComponent(self),
                None,
                params.operator
            )

    def continue_optimize(self, params: OptimizeParameters) -> components.Component:
        new_statement = advanced_component.Statement(
            sc.BooleanComponent(True),
            params.operator,
            sc.RolesLimitComponent(params.other)
        )
        if params.self_limit < 1:
            return sc.BooleanComponent(True).optimize(new_statement)[0]


class GreaterThanOrEqualToLimitComparator(ComparatorImplementation):
    def __gt__(self, other: ComparatorImplementation):
        return self.role_limit() > other.role_limit()

    def comparison(self, number: int):
        return number >= self._role_limit

    def simplify(self) -> comparator:
        return GreaterThanLimitComparator(self._role_limit-1)

    def optimize(self, other: comparator.Comparator, operator: operators.Operator) -> tuple[components.Component, bool]:
        return self.simplify().optimize(other, operator)[0], True


class EqualToLimitComparator(ComparatorImplementation):
    def __gt__(self, other: ComparatorImplementation):
        return False

    def comparison(self, number: int) -> bool:
        return number == self._role_limit

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        """
            (= 6, or, = 5)
            (= 6, and, = 5)
            (= 6, xor, = 5)

        """
        return helpers.optimize_operators(
            None,
            sc.BooleanComponent(False),
            None,
            params.operator
        )

    def optimize_oposite_type(self, params: OptimizeParameters) -> components.Component:
        """
            (= 6, or, != 5)
            (= 6, and, != 5)
            (= 6, xor, != 5)
        """
        return helpers.optimize_operators(
            sc.RolesLimitComponent(params.other),
            sc.RolesLimitComponent(self),
            None,
            params.operator
        )

    def continue_optimize(self, params: OptimizeParameters) -> components.Component:
        new_statement = advanced_component.Statement(
            sc.BooleanComponent(False),
            params.operator,
            sc.RolesLimitComponent(params.other)
        )
        if params.self_limit < 1:
            return sc.BooleanComponent(False).optimize(new_statement)[0]


class NotEqualToLimitComparator(ComparatorImplementation):
    def __gt__(self, other: ComparatorImplementation):
        return False

    def comparison(self, number: int) -> bool:
        return number != self._role_limit

    def optimize_same_type(self, params: OptimizeParameters) -> components.Component:
        """
            (!= 6, or, != 5)
            (!= 6, and, != 5)
            (!= 6, xor, != 5)

        """
        return helpers.optimize_operators(
            sc.BooleanComponent(True),
            None,
            None,
            params.operator
        )

    def continue_optimize(self, params: OptimizeParameters) -> components.Component:
        new_statement = advanced_component.Statement(
            sc.BooleanComponent(True),
            params.operator,
            sc.RolesLimitComponent(params.other)
        )
        if params.self_limit < 1:
            return sc.BooleanComponent(True).optimize(new_statement)[0]


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
