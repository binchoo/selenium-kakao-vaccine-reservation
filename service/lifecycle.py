class LifeCycleMixin:

    def on_start(self, func):
        self.on_start_listener = func

    def on_end(self, func):
        self.on_end_listener = func

    def on_progress(self, func):
        self.on_progress_listener = func