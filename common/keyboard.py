"""
Keyboard Component

"""
from kivy.core.window import Window
from kivy.uix.widget import Widget


class Keyboard(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_event_type('on_key_press')
        self.register_event_type('on_key_down')
        self.register_event_type('on_key_release')

        self._is_attached = False
        self.attach()

    def attach(self):
        if self._is_attached:
            return

        self._keyboard = Window.request_keyboard(
            self.detach, self, 'text'
        )

        if self._keyboard.widget:
            pass

        self._keyboard.bind(
            on_key_down=self._on_keyboard_down,
            on_key_up=self._on_keyboard_up,
        )

        self.keycode = None
        self.modifiers = None

        self._kb_reference = None

        self._keys_pressed = set()
        self._keys_down = set()
        self._is_attached = True

    def detach(self):
        if not self._is_attached:
            return

        self._keyboard.unbind(
            on_key_down=self._on_keyboard_down,
            on_key_up=self._on_keyboard_up,
        )
        self._keyboard = None
        self._is_attached = False

    def _on_keyboard_up(self, keyboard, keycode):
        self._kb_reference = keyboard
        self.keycode = keycode

        key = keycode[1]

        if key in self._keys_pressed:
            self._keys_pressed.remove(key)
        if key in self._keys_down:
            self._keys_down.remove(key)

        self.dispatch('on_key_release')

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self._kb_reference = keyboard
        self.keycode = keycode
        self.modifiers = modifiers

        key = keycode[1]

        if key in self._keys_pressed:
            self._keys_pressed.remove(key)
            self._keys_down.add(key)
            self.dispatch('on_key_down')
        else:
            self._keys_pressed.add(key)
            self.dispatch('on_key_press')

        return True

    def is_key_pressed(self, key):
        if isinstance(key, str):
            key = (key,)
        return True if set(key) & self._keys_pressed else False

    def is_key_down(self, key):
        if isinstance(key, str):
            key = (key,)
        return True if set(key) & self._keys_down else False

    def release(self):
        if self._kb_reference:
            self._kb_reference.release()

    def on_key_press(self): pass

    def on_key_down(self): pass

    def on_key_release(self): pass
