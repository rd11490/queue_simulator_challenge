from utilities.player import Player
import random


class PlayerBase:

    def __init__(self, size):
        self.player_base_size = size
        self._players = {}
        self._in_queue = []
        self._out_of_queue = []
        for i in range(size):
            p = Player()
            self._players[p.id] = (p, False)
            self._out_of_queue.append(p)

    def enqueue_random_player(self):
        if len(self._out_of_queue) > 0:
            p = random.choice(self._out_of_queue)
            self._out_of_queue.remove(p)
            self._in_queue.append(p)
            self._players[p.id] = (p, True)
            return p
        return None

    def dequeue_player(self, p):
        self._in_queue.remove(p)
        self._out_of_queue.append(p)
        self._players[p.id] = (p, False)
