from kivy.logger import Logger as log
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Path2D(Widget):

    targets = set()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # FPS Timer Offset
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

            window = self.get_root_window()
            w, h = window.size
            for target in self.targets:
                if not target.visible:
                    continue

                # Determine movement based on angle and spawn location
                spd = (
                    (Vector(target.speed, target.speed) * target.direction)
                ) * delta

                target.pos = Vector(*target.pos) + spd

        else:
            log.debug(f'PATH MOVEMENT: SKIPPED @ DELTA {self._time}')
