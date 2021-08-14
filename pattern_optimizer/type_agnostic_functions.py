import pattern_parts.advanced_component as ac
import pattern_parts.components as c
import pattern_parts.operators as op
import pattern_parts.simple_component as sc


def optimize_same_components(first_component: c.Component, second_component: c.Component, operator: op.Operator) -> c.Component:
    if first_component != second_component:
        return None

    reverse = first_component.reverse()

    if isinstance(operator, op.OrOperator) or isinstance(operator, op.AndOperator):
        return first_component
    if isinstance(operator, op.NotOrOperator) or isinstance(operator, op.NotAndOperator):
        return reverse
    if isinstance(operator, op.ExclusiveOrOperator):
        return sc.BooleanComponent(False)
    if isinstance(operator, op.NotExclusiveOrOperator):
        return sc.BooleanComponent(True)


def optimize_oposite_components(operator: op.Operator) -> c.Component:

    if isinstance(operator, op.OrOperator) or isinstance(operator, op.NotAndOperator) or isinstance(operator, op.ExclusiveOrOperator):
        return sc.BooleanComponent(True)
    else:
        return sc.BooleanComponent(False)
