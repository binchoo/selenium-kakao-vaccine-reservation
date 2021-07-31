class LifeCycleMixin:

    def on_start(self, func):
        self.on_start_listener = func

    def on_end(self, func):
        self.on_end_listener = func

    def on_progress(self, func):
        self.on_progress_listener = func

    def on_error(self, func):
        self.on_error_listener = func

    def start(self):
        self.on_start_listener(self)
        try:
            self._start()
        except Exception as e:
            self._handle_error(e)
        self.on_end_listener(self)

    def _start(self):
        raise NotImplementedError

    def _handle_error(self, error):
        if hasattr(self, 'on_error_listener'):
            self.on_error_listener(self, error)
        else:
            raise error