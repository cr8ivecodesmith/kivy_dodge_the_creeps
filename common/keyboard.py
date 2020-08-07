from kivy.core.window import Window
from kivy.uix.widget import Widget


class Keyboard(Widget):
    """Keyboard System

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_event_type('on_key_press')
        self.register_event_type('on_key_hold')
        self.register_event_type('on_key_release')

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text'
        )

        if self._keyboard.widget:
            pass

        self._keyboard.bind(
            on_key_down=self._on_keyboard_down,
            on_key_up=self._on_keyboard_up,
        )

        self.keycode = None
        self.modifiers = None

        self._prev_key_str = None
        self._kb_reference = None

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_up(self, keyboard, keycode):
        self._prev_key_str = None
        self._kb_reference = keyboard
        self.keycode = keycode
        self.dispatch('on_key_release')

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self._kb_reference = keyboard
        self.keycode = keycode
        self.modifiers = modifiers

        key_str = keycode[1]
        if self._prev_key_str == key_str:
            self.dispatch('on_key_hold')
        else:
            self._prev_key_str = key_str
            self.dispatch('on_key_press')

        return True

    def release(self):
        if self._kb_reference:
            self._kb_reference.release()

    def on_key_press(self): pass

    def on_key_hold(self): pass

    def on_key_release(self): pass
