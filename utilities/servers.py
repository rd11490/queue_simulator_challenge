class Servers:

    def __init__(self, size):
        self._server_size = size
        self.active_matches = []
        self.completed_matches = []



    def start_match(self, match):
        if len(self.active_matches) < self._server_size:
            self.active_matches.append(match)
            return True
        else:
            return False

    def open_matches(self):
        return self._server_size - len(self.active_matches)

    def tick(self):
        for m in self.active_matches:
            m.tick()
            if not m.is_active():
                self.active_matches.remove(m)
                self.completed_matches.append(m)
