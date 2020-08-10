"""
Mobs Generator

"""
from kivy.logger import Logger as log  # noqa
from kivy.properties import NumericProperty

from common.node import Node

from mob import DodgeMob


class DodgeMobs(Node):

    min_speed = NumericProperty(150)
    max_speed = NumericProperty(350)

    def generate(self):
        mob = DodgeMob()
        mob.min_speed = self.min_speed
        mob.max_speed = self.max_speed
        return mob
