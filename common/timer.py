"""
Timer widget


"""
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import (
    BooleanProperty,
    BoundedNumericProperty,
)


class Timer(Widget):

    delay = BoundedNumericProperty(1, min=.005, max=3600)  # seconds
    oneshot = BooleanProperty(False)
    autoplay = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_timeout')
        self.bind(autoplay=self.start)

        self._clock = None
        self._scheduler = Clock.create_trigger
        self.delta = 0.

    def on_timeout(self): pass

    def start(self, *args):
        if self._clock and self._clock.is_triggered:
            return
        if not self._clock:
            self._clock = self._scheduler(self._tick, self.delay)
            self._clock()
        else:
            self._clock()

    def stop(self):
        if self._clock:
            self._clock.cancel()

    def _tick(self, dt):
        self.delta = dt
        self.dispatch('on_timeout')
        if not self.oneshot:
            self._clock()
