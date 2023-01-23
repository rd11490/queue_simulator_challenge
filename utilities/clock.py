class Clock:

    def __init__(self):
        self.time = 0

    def tick(self, time=1):
        self.time += time

    def now(self):
        return self.time


clock = Clock()
