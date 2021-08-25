from pattern_parts.pattern_part import *
from pattern_parts.comparator_implementation import *
from pattern_parts.components import *
from pattern_parts.simple_component import *
from pattern_parts.advanced_component import *
from pattern_parts.operators import *
import pickle


def pickle_pattern(thing: Component) -> bytes:
    return pickle.dumps(thing)


def unpickle_pattern(bytes_stream: bytes) -> Component:
    return pickle.loads(bytes_stream)
