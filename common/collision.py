"""
Collision Detection System

General checking process:

- Pick target A
- Get all collision coords from the target A's collsion shape (NOT IMPLEMENTED)
- Pick target B
- Get all collision coords from the target B's collsion shape (NOT IMPLEMENTED)
- If any of their points are within the collision shape's area, trigger
  their `on_body_entered` event
- Remove both of them from the

"""  #noqa
from itertools import combinations

from kivy.logger import Logger as log
from kivy.uix.widget import Widget


class CollisionSystem(Widget):

    targets = set()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # FPS Offset Timers
        self._time = .0
        self._rate = 1 / 60

    def register(self, target):
        self.targets.add(target)

    def unregister(self, target):
        if target in self.targets:
            self.targets.remove(target)

    def process(self, delta):
        self._time += delta
        if self._time > self._rate:
            self._time -= self._rate

            for a, b in combinations(self.targets, 2):
                # Ignore invalid comparisons
                if not a.visible or not b.visible:
                    continue
                if set(a.neutral_groups) & set(b.neutral_groups):
                    continue

                # TODO: Get target collision shapes if it exists
                if a.collide_widget(b):
                    a.dispatch('on_body_entered', b)
                    b.dispatch('on_body_entered', a)
        else:
            log.debug(f'COLISSION CHECKS: SKIPPED @ DELTA {self._time}')
