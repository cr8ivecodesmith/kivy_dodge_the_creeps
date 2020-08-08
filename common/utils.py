__all__ = (
    'dist',
    'clamp',
    'Profiler',
)

import cProfile

try:
    from math import dist
except ImportError:
    # If Python version is < 3.8
    from math import sqrt

    def dist(p, q):
        return sqrt(sum((px - qx) ** 2.0 for px, qx in zip(p, q)))


def clamp(val, lower, upper):
    if val >= lower and val <= upper:
        return val
    if val < lower:
        return lower
    elif val > upper:
        return upper


class Profiler:
    """
    Quick implementation of cProfile

    Usage:

    - Initialize on kivy.app.App class.
    - Run `start` from App.on_start.
    - Run `stop` from App.on_stop.
    - Check the profile dump file with the pstats module.

    """
    def __init__(self, dump_file=None):
        self._profiler = cProfile()
        self._dump_file = dump_file or 'app.profile'

    def start(self):
        self._profiler.enable()

    def stop(self):
        self._profiler.disable()
        self._profiler.dump_stats(self._dump_file)
