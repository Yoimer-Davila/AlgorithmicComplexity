__all__ = (
    'timeof',
)

from time import perf_counter
from typing import Callable


def near_unity(tm: float):
    units = ['s', 'ms', 'us', 'ns']
    i = 0
    for i in range(len(units)):
        if abs(tm) < 1:
            tm *= 1000
        else:
            break
    return f"{tm:.2f} {units[i]}"


def timeof(function: Callable, *args, **kwargs):
    """
    Determines the time taken by a function
    :param function: Callable to execute
    :param args: args to function
    :param kwargs: kwargs to function
    :return: function's return value
    """
    start = perf_counter()
    result = function(*args, **kwargs)
    end = perf_counter()

    print('Function {} take {}'.format(function.__name__, near_unity(end - start)))
    return result
