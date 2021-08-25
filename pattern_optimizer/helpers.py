import pattern_parts.components as components
import pattern_parts.operators as operators


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
