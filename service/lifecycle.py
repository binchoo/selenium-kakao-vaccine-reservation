class LifeCycleMixin:

    def on_start(self, func):
        self.on_start_listener = func

    def on_end(self, func):
        self.on_end_listener = func

    def on_progress(self, func):
        self.on_progress_listener = func

    def start(self):
        self.on_start_listener(self)
        self._start()
        self.on_end_listener(self)

    def _start(self):
        raise NotImplementedError