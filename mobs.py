"""
Mobs Generator

"""
from common.widget import Widget
from mob import DodgeMob


class DodgeMobs(Widget):

    def generate(self):
        mob = DodgeMob()
        return mob
