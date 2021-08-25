from abc import ABC, abstractmethod
import inspect
import json


def get_members(thing) -> dict:
    members = {
        "type": type(thing).__name__
    }

    for key, value in inspect.getmembers(thing):
        if key.startswith("__") and key.endswith("__"):
            continue
        if inspect.isfunction(value):
            continue
        if inspect.ismethod(value):
            continue

        if key == "_abc_impl":
            continue

        if (isinstance(value, PatternPart)):
            members[key] = value.__repr__()
        else:
            members[key] = value
    return members


class PatternPart(ABC):
    def __init__(self):
        """"""

    def to_dict(self) -> dict:
        """
            Returns dictionary representation of pattern part

            Overriding __dict__() wont work because then __dir__() breaks, so thats why this method exists
        """

        return get_members(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.to_dict(), indent=4)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return get_members(self) == get_members(other)

    def __ge__(self, other):
        """
            For parts, the >= method represents wheter the other component is equal to self, or if it is "greater" than self, in the sense that it always true when self is true, but sometimes it may be true even when self is false 
        """
        return self.__eq__(other)
