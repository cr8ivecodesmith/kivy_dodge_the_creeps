"""
Main app loader

TODO
----

- Create ScreenManager(s) to allow different screens i.e.
  Main menu, Settings, Game, etc.
- Create an RuntimeStats widget

"""
from kivy.app import App
from kivy.clock import Clock
from kivy.logger import Logger as log

from game import DodgeGame


class DodgeApp(App):

    def build(self):
        return DodgeGame()

    def on_start(self):
        pass

    def on_stop(self):
        fd = Clock.frames_displayed
        ft = Clock.frames
        fx = ft - fd
        log.debug(f'FPS: {Clock.get_rfps()} (ave: {Clock.get_fps():.1f})')
        log.debug(f'FRAMES: {fd} of {ft} ({fx})')
        log.debug(f'RUNTIME: {Clock.get_boottime():.2f}s')
