def find(func, iterable, *args, **kwargs):
    for element in iterable:
        if func(element, *args, **kwargs):
            return element
    return None

def filter(func, iterable, *args, **kwargs):
    returnTouple = ()
    for element in iterable:
        if func(element, *args, **kwargs):
            returnTouple.append(element)
    if not returnTouple:
        return None
    return returnTouple