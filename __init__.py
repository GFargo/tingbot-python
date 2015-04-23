from .graphics import Screen
from .input import Input
# from . import error
import sys


class Tingbot:
    import error
    from . import platform_specific

    def __init__(self):
        platform_specific.fixup_env()
        
        self.loops_per_second = 30

        self.plugins = [self.screen, self.input]

    @property
    def screen(self):
        if not hasattr(self, '_screen'):
            self._screen = Screen()
        return self._screen

    @property
    def input(self):
        if not hasattr(self, '_input'):
            self._input = Input()
        return self._input

    def run(self, app):
        import time
        import sys

        self.plugins.append(app)

        for plugin in self.plugins:
            if hasattr(plugin, 'setup'):
                plugin.setup()

        while True:
            try:
                start_time = time.time()

                for plugin in self.plugins:
                    if hasattr(plugin, 'before_loop'):
                        plugin.before_loop()

                for plugin in self.plugins:
                    if hasattr(plugin, 'loop'):
                        plugin.loop()

                for plugin in self.plugins:
                    if hasattr(plugin, 'after_loop'):
                        plugin.after_loop()
            except Exception as e:
                print e
                import traceback; traceback.print_exc();

                self.error.error_screen(self.screen, sys.exc_info())
                time.sleep(0.5)

            period = 1 / self.loops_per_second

            while time.time() < start_time + period:
                time.sleep(0.001)

                for plugin in self.plugins:
                    if hasattr(plugin, 'during_wait'):
                        plugin.during_wait()

sys.modules[__name__] = Tingbot()
