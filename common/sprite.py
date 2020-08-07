"""
Animated Sprite

A custom Image widget that accepts an Sprite Map Atlas as basis of
animating the sprite.

The Sprite Map Atlas must follow a certain format.

i.e. A Sprite Map with 2 animations: anim_a and anim_b
Note that frame animations must be numbered after the name: `_1` to `_n`

{
    'image.png': {
        'anim_a_1': [...],
        'anim_a_2': [...],
        'anim_b_1': [...],
        'anim_b_2': [...]
    }
}

NOTES
-----

[Updating the `sprite_map`]

You should also update the ff. variables whenever you change the `sprite_map`:
- animations
- initial_animation

[Rotatable image]

This animated sprite allows rotation via the `angle` property.

Reference:
- https://gist.github.com/tshirtman/6222891

TODO
----

[Add manual play]

Right now, animation is only on autoplay. We also want an option to allow
frame updates only on position change.

[Handle variable frame counts per animation]

Right now, we are assuming there's only 2 max frames per animation.

[Handle max and min `scale_hint`]

I've noticed that if scale_hint becomes > 1 there are discrepancies with
the position updates when the sprite moves/loads. Perhaps this is a limitation
with resizing textures beyond its normal size. Anything <= 1 seems to work
as expected.

ISSUES
------

[Improve image flipping]

Right now, if you're updating position on the same axis and flipping the
sprite, the update doesn't take effect unless you hold the direction key.


"""
from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.logger import Logger as log  # noqa
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    ObjectProperty,
    NumericProperty,
    BoundedNumericProperty,
    StringProperty,
)
from kivy.uix.image import Image


class Sprite(Image):
    flip_h = BooleanProperty(False)
    flip_v = BooleanProperty(False)
    angle = NumericProperty(0)
    scale_hint = BoundedNumericProperty(1, min=0.1, max=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Texture controls
        self._flip_h = False
        self._flip_v = False

        # Handle internal bindings
        self.bind(
            flip_h=self.handle_flip_h,
            flip_v=self.handle_flip_v,
            scale_hint=self.handle_scale_hint,
        )

    def handle_scale_hint(self, this, value):
        w, h = this.texture.size
        this.size = (w * value, h * value)

    def handle_flip_h(self, this, value):
        if (
            (this.flip_h and not this._flip_h)
            or (not this.flip_h and this._flip_h)
        ):
            this._flip_textures('horizontal')
        this._flip_h = this.flip_h

    def handle_flip_v(self, this, value):
        if (
            (this.flip_v and not this._flip_v)
            or (not this.flip_v and this._flip_v)
        ):
            this._flip_textures('vertical')
        this._flip_v = this.flip_v

    def _flip_textures(self, direction):
        attr = f'flip_{direction}'
        getattr(self.texture, attr)()


class AnimatedSprite(Sprite):

    sprite_map = StringProperty()

    animations = ListProperty()
    animation = StringProperty()
    animation_speed = BoundedNumericProperty(4, min=1, max=24)

    max_loops = NumericProperty(0)
    autoplay = BooleanProperty(False)

    _sprite_map = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Animation rate controls
        self._clock = None
        self._started = False
        self._animation_speed = .25
        self._max_frames = 1
        self._frame = 1
        self._current_loop = 0

        self.bind(
            sprite_map=self.handle_sprite_map,
            animation_speed=self.handle_animation_speed,
            animation=self.handle_animation,
            autoplay=self.play,
            max_loops=self.handle_max_loops,
        )

    def handle_sprite_map(self, this, value):
        # NOTE: self.animations and self.animation must be updated
        # if this value is updated since animation textures will no longer
        # sync.
        self._sprite_map = Atlas(value)

    def handle_max_loops(self, this, value):
        self._current_loop = 0

    def handle_animation(self, this, value):
        assert (
            value in self.animations
        ), f'Invalid animation: "{value}" not in [{self.animations}]'
        self.stop()
        self.texture = self._sprite_map[f'{value}_1']
        self._frame = 1
        self._max_frames = len([
            k for k in self._sprite_map.textures.keys() if k.startswith(value)
        ])

    def handle_animation_speed(self, this, value):
        self._animation_speed = 1 / value

        was_started = True if self._started else False
        if was_started:
            self.stop()
            self.play()

    def play(self, *args):
        if self._started:
            return
        if not self._clock:
            self._clock = Clock.schedule_interval(
                self._animate, self._animation_speed
            )
        else:
            self._clock()
        self._started = True

    def stop(self):
        if self._clock:
            self._clock.cancel()
            self._started = False

    def _animate(self, dt):
        if self._frame >= self._max_frames:
            self._frame = 1
            if self.max_loops > 0:
                self._current_loop += 1
        else:
            self._frame += 1

        self.texture = self._sprite_map[f'{self.animation}_{self._frame}']

        if self.max_loops > 0 and self._current_loop >= self.max_loops:
            return False

    def _flip_textures(self, direction):
        was_started = True if self._started else False
        if was_started:
            self.stop()

        attr = f'flip_{direction}'
        for _, v in self._sprite_map.textures.items():
            getattr(v, attr)()

        if was_started:
            self.play()
