from kivy.properties import (
    AliasProperty,
    NumericProperty,
)
from common.widget import Widget


class DodgeMob(Widget):

    speed = NumericProperty(20)

    def _get_sprite(self):
        return self.ids.get('sprite')
    sprite = AliasProperty(_get_sprite, None)

    def _get_size(self):
        return self.sprite.size

    def _set_size(self, val):
        pass

    size = AliasProperty(_get_size, _set_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
