from utilities.constants import TANK, DPS, SUPPORT
from utilities.print_debug import print_debug


class BasicQueue:
    """
    This is a stupid queue, no attempt at match making, just the first 10 players available
    """

    def __init__(self):
        self.tank_queue = []
        self.dps_queue = []
        self.support_queue = []

    def __str__(self):
        return f'Currently {len(self.tank_queue)} players in queue for Tank, {len(self.dps_queue)} for DPS and {len(self.support_queue)} for Support'

    def enqueue_player(self, player_in_queue):
        for r in player_in_queue.player.roles:
            if r == TANK:
                self.tank_queue.append(player_in_queue)
            if r == DPS:
                self.dps_queue.append(player_in_queue)
            if r == SUPPORT:
                self.support_queue.append(player_in_queue)

    # instead of trying to figure out a way to dedup players in multiple queues, just force a minimum of 10 per queue
    def can_build_match_tank(self):
        return len(self.tank_queue) >= 10

    def can_build_match_support(self):
        return len(self.support_queue) >= 10

    def can_build_match_dps(self):
        return len(self.dps_queue) >= 10

    def dequeue_tank(self):
        player = self.tank_queue.pop(0)
        if player in self.dps_queue:
            self.dps_queue.remove(player)
        if player in self.support_queue:
            self.support_queue.remove(player)
        return player

    def dequeue_dps(self):
        player = self.dps_queue.pop(0)
        if player in self.tank_queue:
            self.tank_queue.remove(player)
        if player in self.support_queue:
            self.support_queue.remove(player)
        return player

    def dequeue_support(self):
        player = self.support_queue.pop(0)
        if player in self.tank_queue:
            self.tank_queue.remove(player)
        if player in self.dps_queue:
            self.dps_queue.remove(player)
        return player

    def build_match(self):
        if (not self.can_build_match_dps()) or (not self.can_build_match_support()) or (not self.can_build_match_tank()):
            return None

        tank1 = self.dequeue_tank()
        tank2 = self.dequeue_tank()

        dps11 = self.dequeue_dps()
        dps12 = self.dequeue_dps()

        dps21 = self.dequeue_dps()
        dps22 = self.dequeue_dps()

        support11 = self.dequeue_support()
        support12 = self.dequeue_support()

        support21 = self.dequeue_support()
        support22 = self.dequeue_support()

        return ((tank1, dps11, dps12, support11, support12), (tank2, dps21, dps22, support21, support22))
