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
from kivy.clock import Clock
from kivy.logger import Logger as log
from kivy.properties import (
    AliasProperty,
    NumericProperty,
)
from kivy.vector import Vector

from common.widget import Widget
from common.utils import clamp, dist, frame_offset


class DodgePlayer(Widget):

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

    def on_hit(self): pass

    def start(self, pos):
        self.pos = pos
        self.visible = True

    def on_touch_down(self, touch):
        # TODO:
        # Call the process_movement repeatedly
        # Until you reach the destination.
        sprite = self.sprite
        speed = self.speed

        destination = Vector(touch.pos)
        current = Vector(sprite.center)
        distance = dist(current, destination)
        direction = destination - current

        self.process_movement(direction=direction)

    def on_touch_up(self, touch):
        Clock.schedule_once(lambda dt: self.sprite.stop(), 0.6)

    def on_key_release(self):
        sprite = self.ids['sprite']
        sprite.stop()

    def on_key_press(self):
        key_str = self.keyboard.keycode[1]
        if key_str == 'escape':
            log.debug('KEYBOARD: Released')
            log.info('KEYBOARD: Press ESC again to exit')
            self.keyboard.release()

        log.debug(f'KEYBOARD: Pressed ({key_str})')
        self.process_movement(key_str=key_str)

    def on_key_hold(self):
        key_str = self.keyboard.keycode[1]
        log.debug(f'KEYBOARD: Holding ({key_str})')

    def _direction_key_str(self, direction):
        # TODO:
        # - Consider a variance value for absolute l,r,u,d movement
        key_str = ''
        if direction.x == 0 and direction.y > 0:
            key_str = 'up'
        elif direction.x == 0 and direction.y < 0:
            key_str = 'down'
        elif direction.y == 0 and direction.x > 0:
            key_str = 'right'
        elif direction.y == 0 and direction.x < 0:
            key_str = 'left'
        elif direction.y > 0 and direction.x < 0:
            key_str = 'y'
        elif direction.y > 0 and direction.x > 0:
            key_str = 'u'
        elif direction.y < 0 and direction.x < 0:
            key_str = 'b'
        elif direction.y < 0 and direction.x > 0:
            key_str = 'n'
        return key_str

    def get_velocity(self, key_str=None, direction=None):
        velocity = Vector(0, 0)

        if direction and not key_str:
            key_str = self._direction_key_str(direction)

        if key_str == 'up' or key_str == 'k':
            velocity.y += 1
        elif key_str == 'down' or key_str == 'j':
            velocity.y -= 1
        elif key_str == 'left' or key_str == 'h':
            velocity.x -= 1
        elif key_str == 'right' or key_str == 'l':
            velocity.x += 1

        elif key_str == 'y':
            velocity.y += 1
            velocity.x -= 1
        elif key_str == 'u':
            velocity.y += 1
            velocity.x += 1
        elif key_str == 'b':
            velocity.y -= 1
            velocity.x -= 1
        elif key_str == 'n':
            velocity.y -= 1
            velocity.x += 1

        return velocity

    def process_movement(self, key_str=None, direction=None):
        if not self.visible:
            return

        # Process movement
        sprite = self.sprite
        velocity = self.get_velocity(key_str=key_str, direction=direction)

        if velocity.length() > 0:
            # Play animation
            velocity = velocity.normalize() * self.speed
            sprite.play()

        new_pos = Vector(self.pos) + (velocity * frame_offset())
        self.pos = (
            clamp(new_pos.x, 0, self.parent.width - sprite.width),
            clamp(new_pos.y, 0, self.parent.height - sprite.height),
        )

        # Update animation based on velocity
        if velocity.x != 0:
            sprite.animation = 'walk'
            sprite.flip_v = False
            sprite.flip_h = velocity.x < 0
            # sprite.angle += 10

        if velocity.y != 0:
            sprite.animation = 'up'
            sprite.flip_v = velocity.y < 0
            # sprite.angle -= 10

    def collide_widget(self, other):
        super().collide_widget(other)
        log.debug('PLAYER: I got hit!!!!')
