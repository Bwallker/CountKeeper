import pattern_parts.advanced_component as ac
import pattern_parts.components as c
import pattern_parts.operators as operators
import pattern_parts.simple_component as sc


def optimize_same_components(first_component: c.Component, second_component: c.Component, operator: operators.Operator) -> c.Component:
    if first_component != second_component:
        return None

    reverse = first_component.reverse()

    if isinstance(operator, operators.OrOperator) or isinstance(operator, operators.AndOperator):
        return first_component
    if isinstance(operator, operators.NotOrOperator) or isinstance(operator, operators.NotAndOperator):
        return reverse
    if isinstance(operator, operators.ExclusiveOrOperator):
        return sc.BooleanComponent(False)
    if isinstance(operator, operators.NotExclusiveOrOperator):
        return sc.BooleanComponent(True)


def optimize_oposite_components(operator: operators.Operator) -> c.Component:

    if isinstance(operator, operators.OrOperator) or isinstance(operator, operators.NotAndOperator) or isinstance(operator, operators.ExclusiveOrOperator):
        return sc.BooleanComponent(True)
    else:
        return sc.BooleanComponent(False)
