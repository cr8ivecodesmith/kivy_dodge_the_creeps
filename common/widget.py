from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget as KivyWidget


class Widget(KivyWidget):
    """Common Widget

    """
    visible = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(visible=self._handle_visible)

    def _handle_visible(self, this, value):
        self.size_hint_x = 1 if value else 0
        self.opacity = 1 if value else 0
        self.disabled = not value
