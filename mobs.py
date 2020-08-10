"""
Mobs Generator

"""
from kivy.logger import Logger as log  # noqa

from common.node import Node

from mob import DodgeMob


class DodgeMobs(Node):

    def generate(self):
        mob = DodgeMob()
        self.add_widget(mob)
        return mob
