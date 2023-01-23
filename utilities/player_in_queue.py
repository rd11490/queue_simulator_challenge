from utilities.clock import clock


class PlayerInQueue:

    def __init__(self, player):
        self.player = player
        self.queue_start_time = clock.now()
        self.queue_end_time = None
        self.ignore = False

    def __str__(self):
        return f'Player In Queue: {self.player.id} Time in Queue: {self.time_in_queue()} (Start: {self.queue_start_time}, End: {self.queue_end_time})'

    def set_ignore(self):
        self.ignore = True

    def get_ignore(self):
        return self.ignore

    def dequeue(self):
        self.queue_end_time = clock.now()

    def time_in_queue(self):
        if self.queue_end_time is None:
            return clock.now() - self.queue_start_time
        else:
            return self.queue_end_time - self.queue_start_time
