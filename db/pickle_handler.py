from patterns.pattern_part import *
from patterns.comparators import *
from patterns.components import *
from patterns.simple_component import *
from patterns.advanced_component import *
from patterns.operators import *
import pickle


def pickle_pattern(thing: Component) -> bytes:
    return pickle.dumps(thing)


def unpickle_pattern(bytes_stream: bytes) -> Component:
    return pickle.loads(bytes_stream)
