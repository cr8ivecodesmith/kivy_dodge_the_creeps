"""
The Game Screen


"""
from random import randint

from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger as log

from kivy.properties import (
    NumericProperty,
)


class DodgeGame(FloatLayout):

    score = NumericProperty(0)

    def set_player_start(self):
        window = self.get_root_window()
        w, h = window.size
        player = self.ids['player']
        player.visible = True
        player.pos = (w / 2 - 30, h / 2 - 30)
        player.sprite.flip_h = False
        player.sprite.flip_v = False
        player.sprite.animation = 'walk'

    def new_game(self, *args):
        self.score = 0
        self.set_player_start()

        hud = self.ids['hud']
        hud.update_score(self.score)
        hud.show_message('Get Ready')

        self.ids['start_timer'].start()

    def game_over(self):
        self.ids['mob_timer'].stop()
        self.ids['score_timer'].stop()

        self.ids['player'].visible = False
        self.ids['hud'].show_game_over()

        # Remove all mobs
        mobs = self.ids['mobs']
        collision = self.ids['collision_system']
        collision.targets = collision.targets - set(mobs.children)
        mobs.clear_widgets()

    def start_timer_timeout(self):
        self.ids['score_timer'].start()
        self.ids['mob_timer'].start()

    def score_timer_timeout(self):
        if not self.ids['player'].visible:
            return
        self.score += 1
        self.ids['hud'].update_score(self.score)
        log.debug(f'SCORE: {self.score}')

    def mob_timer_timeout(self):
        if not self.ids['player'].visible:
            return

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
        mobs.add_widget(mob)

        # Register to game systems
        path.register(mob)
        collision.register(mob)

        log.debug(f'TOTAL MOBS: {len(mobs.children)}')
