"""
Player

TODO
----

- Handle touch-based movement properly


References
----------

- https://kivy.org/doc/stable/api-kivy.core.window.html#kivy.core.window.Keyboard

NOTES
-----

- Binds the window keyboard events
- on_key_down event must return True otherwise the event is propagated
  directly to the Window

"""  # noqa
from kivy.logger import Logger as log  # noqa
from kivy.properties import (
    AliasProperty,
    NumericProperty,
)
from kivy.vector import Vector

from common.node import Node
from common.utils import clamp


class DodgePlayer(Node):

    speed = NumericProperty(20)

    def _get_sprite(self): return self.ids.get('sprite')

    sprite = AliasProperty(_get_sprite, None)

    def _get_kb(self): return self.parent.ids['keyboard']

    keyboard = AliasProperty(_get_kb, None)

    def _get_size(self): return self.sprite.size

    def _set_size(self, val): pass

    size = AliasProperty(_get_size, _set_size)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_hit')

        self.up_keys = ('up', 'k', 'w',)
        self.down_keys = ('down', 'j', 's',)
        self.left_keys = ('left', 'h', 'a',)
        self.right_keys = ('right', 'l', 'd',)

    def on_hit(self): pass

    def handle_body_entered(self, other):
        self.dispatch('on_hit')

    def get_velocity(self):
        velocity = Vector(0, 0)
        kb = self.keyboard
        if kb.is_key_pressed(self.up_keys) or kb.is_key_down(self.up_keys):
            velocity.y += 1
        if kb.is_key_pressed(self.down_keys) or kb.is_key_down(self.down_keys):
            velocity.y -= 1
        if kb.is_key_pressed(self.left_keys) or kb.is_key_down(self.left_keys):
            velocity.x -= 1
        if (
            kb.is_key_pressed(self.right_keys)
            or kb.is_key_down(self.right_keys)
        ):
            velocity.x += 1
        return velocity

    def process(self, delta):
        if not self.visible:
            return

        # Process movement
        sprite = self.sprite
        velocity = self.get_velocity()

        if velocity.length() > 0:
            # Play animation
            velocity = velocity.normalize() * self.speed
            sprite.play()
        else:
            sprite.stop()

        new_pos = Vector(self.pos) + velocity * delta
        self.pos = (
            clamp(new_pos.x, 0, self.parent.width - sprite.width),
            clamp(new_pos.y, 0, self.parent.height - sprite.height),
        )

        # Update animation based on velocity
        if velocity.x != 0:
            sprite.animation = 'walk'
            sprite.flip_v = False
            sprite.flip_h = velocity.x < 0

        if velocity.y != 0:
            sprite.animation = 'up'
            sprite.flip_v = velocity.y < 0
