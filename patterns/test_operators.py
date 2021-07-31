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
    operator_test_template(NotExcluseOrOperator(), True, False, False, True)