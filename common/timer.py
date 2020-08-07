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

        self._started = False
        self._clock = None
        self._scheduler = getattr(
            Clock, 'schedule_once' if self.oneshot else 'schedule_interval'
        )

    def on_timeout(self):
        pass

    def start(self, *args):
        if self._started:
            return
        if not self._clock:
            self._clock = self._scheduler(self._tick, self.delay)
        else:
            self._clock()
        self._started = True

    def stop(self):
        if self._clock:
            self._clock.cancel()
            self._started = False

    def _tick(self, dt):
        self.dispatch('on_timeout')
