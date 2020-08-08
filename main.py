

if __name__ == '__main__':
    from kivy.config import Config
    from kivy.clock import Clock
    from app import DodgeApp

    Config.set('graphics', 'width', 500)
    Config.set('graphics', 'height', 700)
    Config.set('kivy', 'log_level', 'info')

    Clock.max_iteration = 5  # Iterations before the next frame
    DodgeApp().run()
