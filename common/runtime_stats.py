from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock

from kivy.properties import NumericProperty, BooleanProperty


class RuntimeStats(Widget):

    boottime = NumericProperty()
    fps = NumericProperty()
    rfps = NumericProperty()
    frames_drawn = NumericProperty()
    frames_total = NumericProperty()

    show = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        label = Label(
            pos=(30, 5), font_size='12sp',
            color=(1, 1, 1, 1),
        )
        self.label = label

        self.bind(
            fps=self.update_text,
            rfps=self.update_text,
            boottime=self.update_text,
            frames_drawn=self.update_text,
            frames_total=self.update_text,

            show=self.do_show,
        )

        self.add_widget(label)

        self._clock = Clock.schedule_interval(self.update, 1.0)
        self._clock.cancel()

    def do_show(self, this, value):
        if value:
            self._clock()
        else:
            self._clock.cancel()

    def update_text(self, instance, value):
        fd = self.frames_drawn
        ft = self.frames_total
        fx = ft - fd
        text = (
            f'FPS: {self.rfps} (ave: {self.fps:.1f})\n'
            f'FRAMES: {fd} of {ft} ({fx})\n'
            f'RUNTIME: {self.boottime:.2f}s'
        )
        self.label.text = text

    def update(self, dt):
        self.boottime = Clock.get_boottime()
        self.fps = Clock.get_fps()
        self.rfps = Clock.get_rfps()
        self.frames_drawn = Clock.frames_displayed
        self.frames_total = Clock.frames
