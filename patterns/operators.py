from abc import ABC, abstractmethod

class Operator (ABC):
    def __init__(self):
        """
            
        """
    @abstractmethod
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
            Abstract method.
            applies the operator to two values and returns the result
        """
    def __dict__(self):
        return {
            "type": type(self).__name__
        }
    def __str__(self):
        return type(self).__name__
    def __eq__(self, other):
        if type(self).__name__ != type(other).__name__: return False
        try:
            self_annotatations = self.__annotations__
            other_annotations = other.__annotations__
        except AttributeError:
            return True
        self_instance_variables = {}
        other_instance_variables = {}
        for annotation in self_annotatations:
            value = getattr(self, annotation)
            self_instance_variables[annotation] = value
        for annotation in other_annotations:
            value = getattr(other, annotation)
            other_instance_variables[annotation] = value
        return self_instance_variables == other_instance_variables
class AndOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       0
            1           0       0
            0           1       0
            1           1       1
        """
        return value_1 and value_2

class NotAndOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       1
            1           0       1
            0           1       1
            1           1       0
        """
        return not value_1 or not value_2

class OrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       0
            1           0       1
            0           1       1
            1           1       1
        """
        return value_1 or value_2

class NotOrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       1
            1           0       0
            0           1       0
            1           1       0
        """
        return not value_1 and not value_2

class ExclusiveOrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       0
            1           0       1
            0           1       1
            1           1       0
        """
        return value_1 ^ value_2

class NotExcluseOrOperator(Operator):
    def operation(self, value_1: bool, value_2: bool) -> bool:
        """
        Truth table:
        value_1     value_2     result
            0           0       1
            1           0       0
            0           1       0
            1           1       1
        """
        return not value_1 ^ value_2

