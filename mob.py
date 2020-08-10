from kivy.properties import (
    AliasProperty,
    NumericProperty,
)

from common.node import Node


class DodgeMob(Node):

    min_speed = NumericProperty(150)
    max_speed = NumericProperty(350)

    def _get_size(self): return self.sprite.size

    def _set_size(self, val): pass

    size = AliasProperty(_get_size, _set_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = None
        self.direction = None

    def initialize(self):
        super().initialize()
        self.sprite = self.ids['sprite']
