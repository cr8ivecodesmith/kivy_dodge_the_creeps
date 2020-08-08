from random import randint

from kivy.properties import (
    AliasProperty,
    NumericProperty,
)
from common.node import Node


class DodgeMob(Node):

    min_speed = NumericProperty(150)
    max_speed = NumericProperty(350)
    speed = NumericProperty(0)

    def _get_sprite(self):
        return self.ids.get('sprite')
    sprite = AliasProperty(_get_sprite, None)

    def _get_size(self): return self.sprite.size

    def _set_size(self, val): pass

    size = AliasProperty(_get_size, _set_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            min_speed=self.handle_speed,
            max_speed=self.handle_speed,
        )

    def handle_speed(self, *args):
        self.speed = randint(self.min_speed, self.max_speed)
