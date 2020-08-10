"""
The Game Screen


"""
from random import randint, choice

from kivy.uix.floatlayout import FloatLayout
from kivy.logger import Logger as log
from kivy.vector import Vector

from kivy.properties import (
    NumericProperty,
)


class DodgeGame(FloatLayout):

    score = NumericProperty(0)

    def exit_game(self):
        kb = self.ids['keyboard']
        if kb.is_key_pressed('escape'):
            log.debug('KEYBOARD: Released')
            kb.release()
            log.info('KEYBOARD: Press ESC again to exit')

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
        mobs.clear_widgets()

    def start_timer_timeout(self):
        self.ids['score_timer'].start()
        self.ids['mob_timer'].start()

    def score_timer_timeout(self):
        if not self.ids['player'].visible:
            return
        self.score += 1
        self.ids['hud'].update_score(self.score)

    def mob_timer_timeout(self):
        if not self.ids['player'].visible:
            return

        mobs = self.ids['mobs']
        mob = mobs.generate()

        # Choose a spawn point within the window borders
        window = self.get_root_window()
        w, h = window.size
        borders = {
            'left': ((0, h), (0, 0)),  # left
            'right': ((w, 0), (w, h)),  # right
            'top': ((w, h), (0, h)),  # top
            'bottom': ((0, 0,), (w, 0)),  # bot
        }
        bkey = choice(tuple(borders.keys()))
        p1, p2 = borders[bkey]
        px = (p1[0], p2[0],)
        py = (p1[1], p2[1],)
        pos = (
            randint(min(px), max(px)),
            randint(min(py), max(py))
        )

        # Determine the direction based on pos and angle
        direction = Vector(0, 0)
        if pos[1] >= h / 2:
            direction.y -= 1
        else:
            direction.y += 1
        if pos[0] >= w / 2:
            direction.x -= 1
        else:
            direction.x += 1

        # Depending on the spawn point and direction, determine the angle.
        # By default, the sprite is facing to the right.
        # NOTE: Angle should be based on position and direction but for now,
        # we'll just randomize it.
        x, y = pos
        if bkey == 'left':
            angle = 0
            if y > h / 2:  # top
                angle += randint(-20, 0)
            else:
                angle += randint(0, 20)
        if bkey == 'right':
            angle = 180
            if y > h / 2:  # top
                angle += randint(-20, 0)
            else:
                angle += randint(0, 20)
        if bkey == 'top':
            angle = -90
            if x < w / 2:  # left
                angle += randint(0, 20)
            else:
                angle += randint(-20, 0)
        if bkey == 'bottom':
            angle = 90
            if x < w / 2:  # left
                angle += randint(-20, 0)
            else:
                angle += randint(0, 20)

        # Determine the speed
        speed = randint(mob.min_speed, mob.max_speed)

        # Register the mob node
        mob.speed = speed
        mob.direction = direction
        mob.pos = pos
        mob.sprite.angle = angle
        mobs.add_widget(mob)
