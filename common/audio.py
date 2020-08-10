from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.widget import Widget


class Audio(Widget):

    source = StringProperty()
    autoplay = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._audio = None
        self._is_playing = False
        self.bind(autoplay=self.play)

    def play(self, *args):
        if not self._audio:
            self._audio = SoundLoader.load(self.source)
        if not self._audio.state == 'playing':
            self._audio.play()

    def stop(self, *args):
        if self._audio:
            self._audio.stop()
