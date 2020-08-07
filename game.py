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
from kivy.vector import Vector

from common.utils import frame_offset


class DodgeGame(FloatLayout):

    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._moving = False

    def on_kv_post(self, w):
        self.new_game()
        pass

    def new_game(self, *args):
        self.score = 0
        self.ids['player'].visible = True
        self.ids['start_timer'].start()
        log.debug('NEW GAME:')

    def game_over(self):
        self.ids['mob_timer'].stop()
        self.ids['score_timer'].stop()
        self.ids['mob_move_timer'].stop()
        self.ids['mobs'].clear_widgets()
        # self.ids['player'].visible = False
        Clock.schedule_once(self.new_game, 3)

    def start_timer_timeout(self):
        self.ids['mob_timer'].start()
        self.ids['score_timer'].start()
        self.ids['mob_move_timer'].start()

    def score_timer_timeout(self):
        self.score += 1
        log.debug(f'SCORE: {self.score}')

    def mob_timer_timeout(self):
        window = self.get_root_window()
        mobs = self.ids['mobs']

        mob = mobs.generate()
        mob.pos = (
            randint(0, window.width),
            randint(0, window.height)
        )
        mob.sprite.angle = randint(0, 90)

        mob.sprite.play()
        mobs.add_widget(mob)

        log.debug(f'TOTAL MOBS: {len(mobs.children)}')

    def mob_move_timeout(self):
        if self._moving:
            return

        self._moving = True
        player = self.ids['player']
        mobs = self.ids['mobs']
        window = self.get_root_window()

        offset = frame_offset()

        for mob in mobs.children[:]:
            if (
                (mob.x < 0 or mob.x > window.width)
                or (mob.y < 0 or mob.y > window.height)
            ):
                mobs.remove_widget(mob)
                continue

            spd = randint(5, 50)

            new_pos = Vector(mob.x, mob.y) + (Vector(spd, spd) * offset)
            mob.pos = new_pos

            if mob.collide_widget(player):
                # player.dispatch('on_hit')
                continue

        self._moving = False
