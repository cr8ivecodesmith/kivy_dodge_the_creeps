"""
Base Entity Node

"""
from kivy.properties import AliasProperty, BooleanProperty
from kivy.uix.widget import Widget


class Node(Widget):

    visible = BooleanProperty(True)

    def _set_ng(self, val): self._neutral_groups = set(val)

    def _get_ng(self): return self._neutral_groups

    neutral_groups = AliasProperty(_get_ng, _set_ng)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_body_entered')
        self.bind(
            visible=self._handle_visible,
        )
        self._neutral_groups = set()

    def on_body_entered(self, other):
        pass

    def _handle_visible(self, this, value):
        # self.size_hint_x = 1 if value else 0
        self.opacity = 1 if self.visible else 0
        self.disabled = not self.visible
