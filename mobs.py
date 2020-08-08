"""
Mobs Generator

"""
from kivy.uix.widget import Widget

from mob import DodgeMob


class DodgeMobs(Widget):

    def generate(self):
        mob = DodgeMob()
        if hasattr(mob, 'initialize'):
            mob.initialize()
        return mob
