
class EventSource(object):
    listeners = None

    def init_listeners(self):
        self.listeners = {}

    def listen(self, event, listener):
        if event not in self.listeners:
            self.listeners[event] = []

        self.listeners[event].append(listener)

    def emit(self, event, data):
        if event not in self.listeners:
            return

        for listener in self.listeners[event]:
            listener(event, data)
