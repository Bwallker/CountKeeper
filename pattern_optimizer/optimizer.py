import copy
import patterns.operators as op
import patterns.comparators as comp
import patterns.components as c
import patterns.advanced_component as ac
import patterns.simple_component as sc


def optimize(component: c.Component) -> c.Component:

    if isinstance(component, ac.Statement):

        component, changes = statement_optimizer(component)
        while changes:
            if isinstance(component, ac.Statement):
                component = optimize_away_duplicate_components(component)
            component, changes = statement_optimizer(component)
        return component
    if isinstance(component, ac.ReverseComponent):
        component, _ = reverse_component_optimizer(component)
        return component
    component, _ = component_optimizer(component)
    return component


def optimize_away_duplicate_components(statement: ac.Statement) -> ac.Statement:
    """
    This function removes all the dead components later up the tree that come after that component has already been evaluated earlier in the tree by an OR or AND operator

    For example:
    ac.Statement(
        sc.RolesLimitComponent(
            cp.LessThanLimitComparator(16)
        ),
        op.NotAndOperator(),
        ac.Statement(
            sc.RolesLimitComponent(
                cp.LessThanLimitComparator(16)
            ),
            op.NotAndOperator(),
            sc.RoleComponent(100)
        )
    )


    Here the second RolesLimitComponent is redundant since if the first one evaluates to true, the result of the second doesn't matter since the pattern has already been resolved
    So the result of the second one only matters if it is false, which means that it can be replaced with a false boolean component, since it is functionally the same
    And that boolean will then get cleaned up at the next iteration through the optimizer
    """
    return optimize_away_duplicate_components_helper(statement, [])


def optimize_away_duplicate_components_helper(statement: ac.Statement, components_so_far: list[tuple[c.Component, op.Operator]]) -> ac.Statement:
    first_component = statement.first_component()
    operator = statement.operator()
    second_component = statement.second_component()

    first_component_in_components_so_far: bool = False

    first_component_operator: op.Operator

    second_component_in_components_so_far: bool = False

    second_component_operator: op.Operator
    for component in components_so_far:
        if component[0] == first_component:
            first_component_in_components_so_far = True
            first_component_operator = component[1]
            break
        if oposite_component(component[0]) == first_component:
            first_component_in_components_so_far = True
            first_component_operator = component[1].get_reverse_operator()
            break
        if isinstance(component[0], sc.RolesLimitComponent):
            if isinstance(first_component, sc.RolesLimitComponent):
                comparator = component[0].comparator()
                first_comparator = first_component.comparator()
                if isinstance(comparator, comp.LessThanLimitComparator):
                    if isinstance(first_comparator, comp.LessThanLimitComparator):
                        if comparator.role_limit() > first_comparator.role_limit():
                            first_component_in_components_so_far = True
                            first_component_operator = component[1]
                            break

                if isinstance(comparator, comp.GreaterThanLimitComparator):
                    if isinstance(first_comparator, comp.GreaterThanLimitComparator):
                        if comparator.role_limit() < first_comparator.role_limit():
                            first_component_in_components_so_far = True
                            first_component_operator = component[1]
                            break

    for component in components_so_far:
        if component[0] == second_component:
            second_component_in_components_so_far = True
            second_component_operator = component[1]
            break
        if oposite_component(component[0]) == second_component:
            second_component_in_components_so_far = True
            second_component_operator = component[1].get_reverse_operator()
            break
        if isinstance(component[0], sc.RolesLimitComponent):
            if isinstance(second_component, sc.RolesLimitComponent):
                comparator = component[0].comparator()
                second_comparator = second_component.comparator()

                if isinstance(comparator, comp.LessThanLimitComparator):
                    if isinstance(second_comparator, comp.LessThanLimitComparator):
                        if comparator.role_limit() > second_comparator.role_limit():
                            second_component_in_components_so_far = True
                            second_component_operator = component[1]
                            break
                if isinstance(comparator, comp.GreaterThanLimitComparator):
                    if isinstance(second_comparator, comp.GreaterThanLimitComparator):
                        if comparator.role_limit() < second_comparator.role_limit():
                            second_component_in_components_so_far = True
                            second_component_operator = component[1]
                            break

    if first_component_in_components_so_far:
        if isinstance(first_component_operator, op.AndOperator) or isinstance(first_component_operator, op.NotAndOperator):
            first_component = sc.BooleanComponent(True)
        elif isinstance(first_component_operator, op.OrOperator) or isinstance(first_component_operator, op.NotOrOperator):
            first_component = sc.BooleanComponent(False)

    else:
        components_so_far.append((first_component, operator))
    if second_component_in_components_so_far:
        if isinstance(second_component_operator, op.AndOperator) or isinstance(second_component_operator, op.NotAndOperator):
            second_component = sc.BooleanComponent(True)
        elif isinstance(second_component_operator, op.OrOperator) or isinstance(second_component_operator, op.NotOrOperator):
            second_component = sc.BooleanComponent(False)
    else:
        components_so_far.append((second_component, operator))

    if isinstance(first_component, ac.Statement):
        first_component = optimize_away_duplicate_components_helper(
            first_component, copy.deepcopy(components_so_far))

    if isinstance(second_component, ac.Statement):
        second_component = optimize_away_duplicate_components_helper(
            second_component, copy.deepcopy(components_so_far))

    return ac.Statement(first_component, operator, second_component)


def statement_optimizer(statement: ac.Statement) -> tuple[c.Component, bool]:
    """
    First value in return touple is changed statement
    second value is wheter changes were made to the statement

    """

    if not isinstance(statement, ac.Statement):
        return component_optimizer(statement)

    first_component = statement.first_component()
    operator = statement.operator()
    second_component = statement.second_component()

    first_component, first_component_made_changes = simplify_role_limits(
        first_component)

    second_component, second_component_made_changes = simplify_role_limits(
        second_component)

    if first_component_made_changes or second_component_made_changes:
        return ac.Statement(first_component, operator, second_component), True

    first_component, first_component_made_changes = reverse_component_optimizer(
        first_component)

    second_component, second_component_made_changes = reverse_component_optimizer(
        second_component)

    if first_component_made_changes or second_component_made_changes:
        return ac.Statement(first_component, operator, second_component), True
    if first_component == second_component:
        return optimize_same_components(first_component, second_component, operator), True
    if first_component == second_component.reverse():
        return optimize_oposite_components(first_component, second_component, operator)
    boolean_first_component = optimize_boolean(
        first_component, second_component, operator)
    if boolean_first_component is not None:
        return boolean_first_component, True

    boolean_second_component = optimize_boolean(
        second_component, first_component, operator)
    if boolean_second_component is not None:
        return boolean_second_component, True

    role_limit_both_components = optimize_role_limits(
        first_component, second_component, operator)
    if role_limit_both_components is not None:
        return role_limit_both_components, True

    if isinstance(first_component, ac.Statement):
        first_component, first_made_changes = statement_optimizer(
            first_component)
        if first_made_changes:
            return ac.Statement(first_component, operator, second_component), True

    if isinstance(second_component, ac.Statement):
        second_component, second_made_changes = statement_optimizer(
            second_component)
        if second_made_changes:
            return ac.Statement(first_component, operator, second_component), True

    return ac.Statement(
        first_component, operator, second_component), False


def optimize_role_limits(first_component: c.Component, second_component: c.Component, operator: op.Operator) -> c.Component:
    if first_component == second_component:
        return optimize_same_components(first_component, second_component, operator)

    if first_component == second_component.reverse():
        return optimize_oposite_components(first_component, second_component, operator)

    if not isinstance(first_component, sc.RolesLimitComponent) or not isinstance(second_component, sc.RolesLimitComponent):
        return None

    if are_oposite_role_components(first_component, second_component):
        return optimize_oposite_components(first_component, second_component, operator)

    first_comparator = first_component.comparator()
    second_comparator = second_component.comparator()
    first_limit = first_comparator.role_limit()
    second_limit = second_comparator.role_limit()

    gt: comp.GreaterThanLimitComparator = None
    gt_limit: int
    lt: comp.LessThanLimitComparator = None
    lt_limit: int
    eq: comp.EqualToLimitComparator = None
    eq_limit: int
    neq: comp.NotEqualToLimitComparator = None
    neq_limit: int

    if isinstance(first_comparator, comp.LessThanLimitComparator) and isinstance(second_comparator, comp.GreaterThanLimitComparator):
        lt_and_gt = True
        gt = second_comparator
        gt_limit = second_limit
        lt = first_comparator
        lt_limit = first_limit
    if isinstance(first_comparator, comp.GreaterThanLimitComparator) and isinstance(second_comparator, comp.LessThanLimitComparator):
        lt_and_gt = True
        gt = first_comparator
        gt_limit = first_limit
        lt = second_comparator
        lt_limit = second_limit

    if isinstance(first_comparator, comp.GreaterThanLimitComparator) ^ isinstance(second_comparator, comp.GreaterThanLimitComparator):
        if isinstance(first_comparator, comp.GreaterThanLimitComparator):
            gt = first_comparator
        else:
            gt = second_comparator

    if isinstance(first_comparator, comp.LessThanLimitComparator) ^ isinstance(second_comparator, comp.LessThanLimitComparator):
        if isinstance(first_comparator, comp.LessThanLimitComparator):
            lt = first_comparator
        else:
            lt = second_comparator

    if isinstance(first_comparator, comp.EqualToLimitComparator) ^ isinstance(second_comparator, comp.EqualToLimitComparator):
        if isinstance(first_comparator, comp.EqualToLimitComparator):
            eq = first_comparator
        else:
            eq = second_comparator

    if isinstance(first_comparator, comp.NotEqualToLimitComparator) ^ isinstance(second_comparator, comp.NotEqualToLimitComparator):
        if isinstance(first_comparator, comp.NotEqualToLimitComparator):
            neq = first_comparator
        else:
            neq = second_comparator
    #
    #
    #
    if isinstance(first_comparator, comp.GreaterThanLimitComparator) and isinstance(second_comparator, comp.GreaterThanLimitComparator):

        bigger_limit = max(first_limit, second_limit)
        smaller_limit = min(first_limit, second_limit)

        if isinstance(operator, op.OrOperator):
            return sc.RolesLimitComponent(comp.GreaterThanLimitComparator(smaller_limit))
        if isinstance(operator, op.NotOrOperator):
            return sc.RolesLimitComponent(comp.LessThanLimitComparator(smaller_limit+1))
        if isinstance(operator, op.AndOperator):
            return sc.RolesLimitComponent(comp.GreaterThanLimitComparator(bigger_limit))
        if isinstance(operator, op.NotAndOperator):
            return sc.RolesLimitComponent(comp.LessThanLimitComparator(bigger_limit+1))
        if isinstance(operator, op.ExclusiveOrOperator):
            """
                (> 10, xor, > 16)
                true if greater than 10 but less than 17
                aka cannot be optimized to a non statement

            """
        if isinstance(operator, op.NotExclusiveOrOperator):
            """
                (> 10, nxor, > 16)
                true if less than 11 or greater than 16
                aka cannot be optimized to a non statement

            """
    if isinstance(first_comparator, comp.LessThanLimitComparator) and isinstance(second_comparator, comp.LessThanLimitComparator):
        if first_limit == second_limit:
            return optimize_same_components(first_component, second_component, operator)
        bigger_limit = max(first_limit, second_limit)
        smaller_limit = min(first_limit, second_limit)

        if isinstance(operator, op.OrOperator):
            return sc.RolesLimitComponent(comp.LessThanLimitComparator(bigger_limit))
        if isinstance(operator, op.NotOrOperator):
            return sc.RolesLimitComponent(comp.GreaterThanLimitComparator(bigger_limit-1))

        if isinstance(operator, op.AndOperator):
            return sc.RolesLimitComponent(comp.LessThanLimitComparator(smaller_limit))
        if isinstance(operator, op.NotAndOperator):
            return sc.RolesLimitComponent(comp.GreaterThanLimitComparator(smaller_limit-1))

        if isinstance(operator, op.ExclusiveOrOperator):
            """
                (< 10, xor, < 16)
                true if greater than 9 but less than 16
                aka cannot be optimized to a non statement

            """
        if isinstance(operator, op.NotExclusiveOrOperator):
            """
                (< 10, nxor, < 16)
                true less than 10 or greater than 15
                aka cannot be optimized to a non statement
            """
    if isinstance(first_comparator, comp.EqualToLimitComparator) and isinstance(second_comparator, comp.EqualToLimitComparator):
        """
            (= 10, or, = 11)
            ()
        """
        # Roles limit cannot be equal, because then first_component == second_component => Handled by the first line of the function
        if first_limit == second_limit:
            return optimize_same_components(first_component, second_component, operator)
        else:
            if isinstance(operator, op.AndOperator):
                return sc.BooleanComponent(False)
            if isinstance(operator, op.NotAndOperator):
                return sc.BooleanComponent(True)
    if isinstance(first_comparator, comp.NotEqualToLimitComparator) and isinstance(second_comparator, comp.NotEqualToLimitComparator):
        """
            (!= 10, or, != 11)
            (!= 10, nor, != 11)
            (!= 10, and, != 11)
            (!= 10, nand, != 11)
        """
        if first_limit == second_limit:
            return optimize_same_components(first_component, second_component, operator)
        else:
            if isinstance(operator, op.OrOperator):
                return sc.BooleanComponent(True)
            if isinstance(operator, op.NotOrOperator):
                return sc.BooleanComponent(False)
        # WARNING ---- Horrific block of if statements ahead
        # Not sure how you could improve this, since most of the logic is unique to each scenario...
    if lt and gt:
        lt_limit = lt.role_limit()
        gt_limit = gt.role_limit()
        if lt_limit < gt_limit:
            """

                ( < 4, or , > 5)
                (< 4, nor, > 5)

                ( < 4, and , > 5)
                (< 4, nand, > 5)

                (< 4, xor, > 5)
                (< 4, nxor, > 5)

                Incase you want to think it through yourself
            """
            if isinstance(operator, op.AndOperator):
                return sc.BooleanComponent(False)
            if isinstance(operator, op.NotAndOperator):
                return sc.BooleanComponent(True)
            """The result are not solvable in general"""
            return None
        if gt_limit == lt_limit:
            """

                ( < 5, or , > 5)
                (< 5, nor, > 5)

                ( < 5, and , > 5)
                (< 5, nand, > 5)

                (< 5, xor, > 5)
                (< 5, nxor, > 5)

                Incase you want to think it through yourself
            """

            if isinstance(operator, op.OrOperator) or isinstance(operator, op.ExclusiveOrOperator):
                return sc.RolesLimitComponent(comp.NotEqualToLimitComparator(gt_limit-1))
            if isinstance(operator, op.NotOrOperator) or isinstance(operator, op.NotExclusiveOrOperator):
                return sc.RolesLimitComponent(comp.EqualToLimitComparator(gt_limit-1))

            if isinstance(operator, op.AndOperator):
                return sc.BooleanComponent(False)
            if isinstance(operator, op.NotAndOperator):
                return sc.BooleanComponent(True)
        if lt_limit == gt_limit + 1:
            """

                ( < 6, or , > 5)
                (< 6, nor, > 5)

                ( < 6, and , > 5)
                (< 6, nand, > 5)

                (< 6, xor, > 5)
                (< 6, nxor, > 5)

                Incase you want to think it through yourself
            """
            if isinstance(operator, op.OrOperator) or isinstance(operator, op.ExclusiveOrOperator) or isinstance(operator, op.NotAndOperator):
                return sc.BooleanComponent(True)
            if isinstance(operator, op.NotOrOperator) or isinstance(operator, op.NotExclusiveOrOperator) or isinstance(operator, op.AndOperator):
                return sc.BooleanComponent(False)
        if lt_limit == gt_limit + 2:
            """

                ( < 7, or , > 5)
                (< 7, nor, > 5)

                ( < 7, and , > 5)
                (< 7, nand, > 5)

                (< 7, xor, > 5)
                (< 7, nxor, > 5)

                Incase you want to think it through yourself
            """
            if isinstance(operator, op.OrOperator):
                return sc.BooleanComponent(True)
            if isinstance(operator, op.NotOrOperator):
                return sc.BooleanComponent(False)
            if isinstance(operator, op.AndOperator):
                return sc.RolesLimitComponent(comp.EqualToLimitComparator(gt_limit+1))
            if isinstance(operator, op.NotAndOperator):
                return sc.RolesLimitComponent(comp.NotEqualToLimitComparator(gt_limit+1))

            if isinstance(operator, op.ExclusiveOrOperator):
                """
                    Not solvable in the general case
                    means it's either NOT equal to gt_limit + 1
                    or less than lt_limit or greater than gt_limit
                """
            if isinstance(operator, op.NotExclusiveOrOperator):
                return sc.RolesLimitComponent(comp.EqualToLimitComparator(gt_limit+1))
            return None
        if lt_limit > gt_limit:
            """

                (< 8, or, > 5)
                (< 8, nor, > 5)

                (< 8, and, > 5)
                (< 8, nand, > 5)

                (< 8, xor, > 5)
                (< 8, nxor, > 5)


                Incase you want to think it through yourself
            """
            if isinstance(operator, op.OrOperator):
                return sc.BooleanComponent(True)
            if isinstance(operator, op.NotOrOperator):
                return sc.BooleanComponent(False)
            if isinstance(operator, op.AndOperator):
                """
                    Matches if requal to gt_limit + 1 or gt_limit + 2 if lit_limit == gt_limit + 3
                    Not solvable without creating a new nested statement, which would not be performative (probably). I also have to stop sometime
                """
            if isinstance(operator, op.NotAndOperator):
                """
                    Not solvable in general without nested statement
                """

            if isinstance(operator, op.ExclusiveOrOperator):
                """
                    Not solvable in general without nested statement
                """

            if isinstance(operator, op.NotExclusiveOrOperator):
                """
                    Not solvable in general without nested statement
                """
            return None

    return None


def optimize_boolean(bool_component: sc.BooleanComponent, other_component: c.Component, operator: op.Operator) -> c.Component:
    if not isinstance(bool_component, sc.BooleanComponent):
        return None

    boolean = bool_component.boolean()

    other, _ = component_optimizer(other_component)

    reverse_other, _ = reverse_component_optimizer(
        ac.ReverseComponent(other))

    if isinstance(operator, op.OrOperator):
        if boolean:
            return sc.BooleanComponent(True)
        else:
            return other

    if isinstance(operator, op.NotOrOperator):
        if boolean:
            return sc.BooleanComponent(False)
        else:
            return reverse_other

    if isinstance(operator, op.AndOperator):
        if boolean:
            return other
        else:
            return sc.BooleanComponent(False)

    if isinstance(operator, op.NotAndOperator):
        if boolean:
            return reverse_other
        else:
            return sc.BooleanComponent(True)

    if isinstance(operator, op.ExclusiveOrOperator):
        if boolean:
            return reverse_other
        else:
            return other

    if isinstance(operator, op.NotExclusiveOrOperator):
        if boolean:
            return other
        else:
            return reverse_other

    return None


def are_oposite_role_components(first_component: sc.RolesLimitComponent, second_component: sc.RolesLimitComponent) -> bool:

    return reverse_role_limit_component(first_component)[0] == simplify_role_limits(second_component)[0]


def reverse_role_limit_component(role_limit_component: sc.RolesLimitComponent) -> tuple[c.Component, bool]:

    if not isinstance(role_limit_component, sc.RolesLimitComponent):
        return role_limit_component, False
    component_comparator = role_limit_component.comparator()

    return sc.RolesLimitComponent(__reverse_comparator(component_comparator)), True


def __reverse_comparator(comparator: comp.Comparator) -> comp.Comparator:

    limit = comparator.role_limit()
    if isinstance(comparator, comp.LessThanOrEqualToLimitComparator):
        return comp.GreaterThanLimitComparator(limit)
    if isinstance(comparator, comp.GreaterThanOrEqualToLimitComparator):
        return comp.LessThanLimitComparator(limit)

    if isinstance(comparator, comp.NotEqualToLimitComparator):
        return comp.EqualToLimitComparator(limit)
    if isinstance(comparator, comp.EqualToLimitComparator):
        return comp.NotEqualToLimitComparator(limit)

    if isinstance(comparator, comp.LessThanLimitComparator):
        return comp.GreaterThanLimitComparator(limit-1)
    if isinstance(comparator, comp.GreaterThanLimitComparator):
        return comp.LessThanLimitComparator(limit+1)


def oposite_component(component: c.Component) -> c.Component:
    if isinstance(component, sc.RolesLimitComponent):
        return reverse_role_limit_component(component)[0]
    if isinstance(component, sc.BooleanComponent):
        return sc.BooleanComponent(not component.boolean())
    if isinstance(component, ac.ReverseComponent):
        return component_optimizer(component.component())[0]
    if isinstance(component, ac.Statement):
        return ac.Statement(component_optimizer(component.first_component())[0], component.operator().get_reverse_operator(), component_optimizer(component.second_component())[0])
    return reverse_component_optimizer(ac.ReverseComponent(component))[0]


def component_optimizer(component: c.Component) -> tuple[c.Component, bool]:
    """
    First value in return touple is changed component
    second value is wheter changes were made to the component
    """
    if isinstance(component, ac.ReverseComponent):
        return reverse_component_optimizer(component)
    if isinstance(component, ac.Statement):
        return statement_optimizer(component)
    if isinstance(component, sc.RolesLimitComponent):
        return simplify_role_limits(component)
    return component, False


def simplify_role_limits(component: c.Component) -> tuple[c.Component, bool]:
    if isinstance(component, sc.RolesLimitComponent):
        comparator = component.comparator()
        changes = False
        if isinstance(comparator, comp.LessThanOrEqualToLimitComparator):
            comparator = comp.LessThanLimitComparator(
                comparator.role_limit()+1)
            changes = True
        elif isinstance(comparator, comp.GreaterThanOrEqualToLimitComparator):
            comparator = comp.GreaterThanLimitComparator(
                comparator.role_limit()-1)
            changes = True
        return sc.RolesLimitComponent(comparator), changes
    return component, False




def reverse_component_optimizer(reverse_component: ac.ReverseComponent) -> tuple[c.Component, bool]:
    """
    First value in return touple is changed reverse_component
    second value is wheter changes were made to the reverse_component
    """

    if not isinstance(reverse_component, ac.ReverseComponent):
        return reverse_component, False

    super_component = reverse_component.component()
    super_component, _ = component_optimizer(
        super_component)
    if isinstance(super_component, ac.Statement):
        new_first_component = super_component.first_component()
        new_operator = super_component.operator().get_reverse_operator()
        new_second_component = super_component.second_component()
        return statement_optimizer(ac.Statement(new_first_component, new_operator, new_second_component)), True
    if isinstance(super_component, sc.BooleanComponent):

        return sc.BooleanComponent(not super_component.boolean()), True
    if isinstance(super_component, sc.RolesLimitComponent):
        return reverse_role_limit_component(super_component)[0], True
    if isinstance(super_component, ac.ReverseComponent):
        super_super_component = super_component.component()

        return component_optimizer(super_super_component)[0], True
    return reverse_component, False
