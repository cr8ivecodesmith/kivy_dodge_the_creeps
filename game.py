"""
The Game Screen


"""
from random import randint

from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger as log

from kivy.properties import (
    NumericProperty,
)


class DodgeGame(FloatLayout):

    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._moving = False

    def on_kv_post(self, w):
        collision = self.ids['collision_system']
        collision.register(self.ids['player'])
        self.new_game()

    def new_game(self, *args):
        self.score = 0
        self.ids['player'].visible = True
        self.ids['start_timer'].start()
        log.debug('NEW GAME:')

    def game_over(self):
        self.ids['mob_timer'].stop()
        self.ids['score_timer'].stop()
        self.ids['mobs'].clear_widgets()
        # self.ids['player'].visible = False
        Clock.schedule_once(self.new_game, 3)

    def start_timer_timeout(self):
        self.ids['mob_timer'].start()
        self.ids['score_timer'].start()

    def score_timer_timeout(self):
        self.score += 1
        log.debug(f'SCORE: {self.score}')

    def mob_timer_timeout(self):
        window = self.get_root_window()
        mobs = self.ids['mobs']
        path = self.ids['mob_path']
        collision = self.ids['collision_system']

        mob = mobs.generate()
        mob.pos = (
            randint(0, window.width),
            randint(0, window.height)
        )
        mob.sprite.angle = randint(0, 90)

        mob.sprite.play()
        mobs.add_widget(mob)

        # Register to game systems
        path.register(mob)
        collision.register(mob)

        log.debug(f'TOTAL MOBS: {len(mobs.children)}')
