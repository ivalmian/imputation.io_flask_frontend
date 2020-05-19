import numpy as np
from collections import defaultdict
from time import perf_counter
import functools


def single_get_closest_value(num, data):
    return data[num] if num in data else data[min(data.keys(), key=lambda k: abs(k - num))]


def rem_duplicates(ts):
    t_new = defaultdict(float)
    for t in ts:
        if not isinstance(t[0], str):
            t_new[t[0]] += t[1]
        else:
            print(t)
    return list(t_new.items())


def smooth(x, y):
    y = np.array(y)
    x = np.array(x)
    x_var = np.var(x)
    var_scale = 0.08
    dist = np.zeros((len(x), len(x)))
    for i, x1 in enumerate(x):
        for j, x2 in enumerate(x):
            dist[i, j] = np.exp(-(x1-x2)**2/(var_scale*x_var))

    for i in range(len(y)):
        y[i] = (dist[i, :]*y).sum()/dist[i, :].sum()

    return list(y)

def timenlog(func):
    from app import app
    @functools.wraps(func)
    def timenlogs_wrapper(*args,**kwargs):
        s = perf_counter()
        ret_val = func(*args,**kwargs)
        e = perf_counter()
        msg = f'{func.__name__} took {e-s} seconds to execute'
        print(msg)
        app.logger.info(msg) # pylint: disable=no-member

        return ret_val
    return timenlogs_wrapper