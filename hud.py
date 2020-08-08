from kivy.clock import Clock
from kivy.logger import Logger as log  # noqa
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout


class Hud(BoxLayout):

    is_game_over = BooleanProperty(False)
    show_start_button = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_start_game')

    def on_start_game(self): pass

    def show_message(self, text):
        label = self.ids['message']
        label.text = text
        label.visible = True
        self.ids['message_timer'].start()

    def show_game_over(self):
        self.show_message('Game Over')
        self.is_game_over = True

    def show_title_message(self):
        label = self.ids['message']
        label.text = 'Dodge the\nCreeps!'
        label.visible = True
        Clock.schedule_once(self.show_title_timer_timeout, 1)

    def update_score(self, score):
        self.ids['score_label'].text = str(score)

    def message_timer_timeout(self, delta):
        self.ids['message'].visible = False
        if self.is_game_over:
            self.is_game_over = False
            self.show_title_message()

    def press_start(self, *args):
        if self.parent.ids['keyboard'].is_key_pressed('enter'):
            self.handle_start_button()

    def handle_start_button(self, *args):
        btn = self.ids['start_button']
        if btn.visible:
            self.ids['start_button'].visible = False
            self.dispatch('on_start_game')

    def show_title_timer_timeout(self, delta):
        self.ids['start_button'].visible = True
