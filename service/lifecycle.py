class LifeCycleMixin:

    def __init__(self):
        self.on_start(None)
        self.on_end(None)
        self.on_progress(None)
        self.on_error(None)

    def on_start(self, func):
        self.on_start_listener = func

    def on_end(self, func):
        self.on_end_listener = func

    def on_progress(self, func):
        self.on_progress_listener = func

    def on_error(self, func):
        self.on_error_listener = func

    def start(self):
        self._before_start()
        try:
            self._start()
        except Exception as e:
            self._handle_error(e)
        self._after_end()

    def _before_start(self):
        if self.on_start_listener is not None:
            self.on_start_listener(self)

    def _start(self):
        raise NotImplementedError

    def _handle_error(self, error):
        if self.on_error_listener is not None:
            self.on_error_listener(self, error)
        else:
            raise error
            
    def _after_end(self):
        if self.on_end_listener is not None:
            self.on_end_listener(self)