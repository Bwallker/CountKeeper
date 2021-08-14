from operators import *


def operator_test_template(operator: Operator, ff: bool, tf: bool, ft: bool, tt: bool) -> None:
    if ff:
        assert operator.operation(False, False)
    else:
        assert not operator.operation(False, False)
    if tf:
        assert operator.operation(True, False)
    else:
        assert not operator.operation(True, False)
    if ft:
        assert operator.operation(False, True)
    else:
        assert not operator.operation(False, True)
    if tt:
        assert operator.operation(True, True)
    else:
        assert not operator.operation(True, True)


def test_operators_test_start():
    print("Running operator tests")


def test_and_operator():
    operator_test_template(AndOperator(), False, False, False, True)


def test_nand_operator():
    operator_test_template(NotAndOperator(), True, True, True, False)


def test_or_operator():
    operator_test_template(OrOperator(), False, True, True, True)


def test_nor_operator():
    operator_test_template(NotOrOperator(), True, False, False, False)


def test_xor_operator():
    operator_test_template(ExclusiveOrOperator(), False, True, True, False)


def test_nxor_operator():
    operator_test_template(NotExclusiveOrOperator(), True, False, False, True)


def test_reverse_operator():
    assert AndOperator().get_reverse_operator() == NotAndOperator()
    assert NotAndOperator().get_reverse_operator() == AndOperator()
    assert OrOperator().get_reverse_operator() == NotOrOperator()
    assert NotOrOperator().get_reverse_operator() == OrOperator()

    assert ExclusiveOrOperator().get_reverse_operator() == NotExclusiveOrOperator()
    assert NotExclusiveOrOperator().get_reverse_operator() == ExclusiveOrOperator()


def test_repr():
    print("Entered test_repr")
    print(OrOperator().__repr__())


def test_operators_test_stop():
    print("Finished running operator tests")
