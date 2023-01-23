from utilities.clock import clock
from utilities.constants import TANK, DPS, SUPPORT
from utilities.helpers import range_limit_sr
from utilities.print_debug import print_debug
import math


class BucketQueue:
    """
    Update this class however you want in order to make the most efficient queue possible.
    """

    def __init__(self):

        self._tank_queue = {}
        self._dps_queue = {}
        self._support_queue = {}

        for i in range(0, 5001, 100):
            self._tank_queue[i] = []
            self._dps_queue[i] = []
            self._support_queue[i] = []

        self.players_in_queue = {
            TANK: {},
            DPS: {},
            SUPPORT: {}
        }

    def __str__(self):
        return str(self.players_in_queue)

    def bucket_mmr(self, mmr):
        return int(math.floor(mmr / 100) * 100)

    def enqueue_player(self, player_in_queue):
        for r in player_in_queue.player.roles:
            if r == TANK:
                mmr = player_in_queue.player.get_tank_mmr()
                key = self.bucket_mmr(mmr)
                self._tank_queue[key].append(player_in_queue)
                self.players_in_queue[TANK][player_in_queue.player.id] = (player_in_queue, [key])

            if r == DPS:
                mmr = player_in_queue.player.get_dps_mmr()
                key = self.bucket_mmr(mmr)
                self._dps_queue[key].append(player_in_queue)
                self.players_in_queue[DPS][player_in_queue.player.id] = (player_in_queue, [key])

            if r == SUPPORT:
                mmr = player_in_queue.player.get_support_mmr()
                key = self.bucket_mmr(mmr)
                self._support_queue[key].append(player_in_queue)
                self.players_in_queue[SUPPORT][player_in_queue.player.id] = (player_in_queue, [key])

    def pop_and_remove(self, queue_pop, other_queue1, other_queue2):
        player = queue_pop.pop(0)
        if player in other_queue1:
            other_queue1.remove(player)
        if player in other_queue2:
            other_queue2.remove(player)
        return player

    def remove_from_all_queues(self, player_in_queue):
        if player_in_queue.player.id in self.players_in_queue[TANK].keys():
            player, keys = self.players_in_queue[TANK][player_in_queue.player.id]
            for k in keys:
                self._tank_queue[k].remove(player_in_queue)
            self.players_in_queue[TANK].pop(player_in_queue.player.id)

        if player_in_queue.player.id in self.players_in_queue[DPS].keys():
            player, keys = self.players_in_queue[DPS][player_in_queue.player.id]
            for k in keys:
                self._dps_queue[k].remove(player_in_queue)
            self.players_in_queue[DPS].pop(player_in_queue.player.id)

        if player_in_queue.player.id in self.players_in_queue[SUPPORT].keys():
            player, keys = self.players_in_queue[SUPPORT][player_in_queue.player.id]
            for k in keys:
                self._support_queue[k].remove(player_in_queue)
            self.players_in_queue[SUPPORT].pop(player_in_queue.player.id)

    # REQUIRED
    def build_match(self):
        """
        The method for pulling out a group of players that would make a "balanced" game
        :return: None or A touple of touples: ((tank1, dps11, dps12, support11, support12), (tank2, dps21, dps22, support21, support22))
        """
        for i in range(5000, 0, -100):
            tank_queue = self._tank_queue[i]
            dps_queue = self._dps_queue[i]
            support_queue = self._support_queue[i]

            tank_queue_copy = [i for i in tank_queue]
            dps_queue_copy = [i for i in dps_queue]
            support_queue_copy = [i for i in support_queue]

            if len(tank_queue_copy) >= 2:
                tank1 = self.pop_and_remove(tank_queue_copy, dps_queue_copy, support_queue_copy)
                tank2 = self.pop_and_remove(tank_queue_copy, dps_queue_copy, support_queue_copy)

                if len(dps_queue_copy) >= 4:
                    dps11 = self.pop_and_remove(dps_queue_copy, tank_queue_copy, support_queue_copy)
                    dps12 = self.pop_and_remove(dps_queue_copy, tank_queue_copy, support_queue_copy)
                    dps21 = self.pop_and_remove(dps_queue_copy, tank_queue_copy, support_queue_copy)
                    dps22 = self.pop_and_remove(dps_queue_copy, tank_queue_copy, support_queue_copy)

                    if len(support_queue_copy) >= 4:
                        support11 = self.pop_and_remove(support_queue_copy, dps_queue_copy, tank_queue_copy)
                        support12 = self.pop_and_remove(support_queue_copy, dps_queue_copy, tank_queue_copy)
                        support21 = self.pop_and_remove(support_queue_copy, dps_queue_copy, tank_queue_copy)
                        support22 = self.pop_and_remove(support_queue_copy, dps_queue_copy, tank_queue_copy)

                        self.remove_from_all_queues(tank1)
                        self.remove_from_all_queues(dps11)
                        self.remove_from_all_queues(dps12)
                        self.remove_from_all_queues(support11)
                        self.remove_from_all_queues(support12)

                        self.remove_from_all_queues(tank2)
                        self.remove_from_all_queues(dps21)
                        self.remove_from_all_queues(dps22)
                        self.remove_from_all_queues(support21)
                        self.remove_from_all_queues(support22)

                        return (
                        (tank1, dps11, dps12, support11, support12), (tank2, dps21, dps22, support21, support22))

        return None

    # Required
    def tick(self):
        """
        Does not have to do anything, but present in case you want to handle a tick
        :return: None
        """

        if (clock.now() > 0) and (clock.now() % 60 == 0):
            # expand player mmr range by 1
            tank_players = self.players_in_queue[TANK]
            for i in tank_players.keys():
                player_in_queue, keys = tank_players[i]
                if len(keys) > 0:
                    key = self.bucket_mmr(player_in_queue.player.get_tank_mmr())
                    min_in_queue = int(math.floor(player_in_queue.time_in_queue() / 60))
                    adjust = 100 * min_in_queue

                    lower = range_limit_sr(key - adjust)
                    higher = range_limit_sr(key - adjust)

                    if lower not in keys:
                        self._tank_queue[lower].append(player_in_queue)
                        keys.append(lower)

                    if higher not in keys:
                        self._tank_queue[higher].append(player_in_queue)
                        keys.append(higher)

            dps_players = self.players_in_queue[DPS]
            for i in dps_players.keys():
                player_in_queue, keys = dps_players[i]
                if len(keys) > 0:
                    key = self.bucket_mmr(player_in_queue.player.get_dps_mmr())
                    min_in_queue = int(math.floor(player_in_queue.time_in_queue() / 60))
                    adjust = 100 * min_in_queue
                    lower = range_limit_sr(key - adjust)
                    higher = range_limit_sr(key - adjust)

                    if lower not in keys:
                        self._dps_queue[lower].append(player_in_queue)
                        keys.append(lower)

                    if higher not in keys:
                        self._dps_queue[higher].append(player_in_queue)
                        keys.append(higher)

            support_players = self.players_in_queue[SUPPORT]
            for i in support_players.keys():
                player_in_queue, keys = support_players[i]
                if len(keys) > 0:
                    key = self.bucket_mmr(player_in_queue.player.get_support_mmr())
                    min_in_queue = int(math.floor(player_in_queue.time_in_queue() / 60))
                    adjust = 100 * min_in_queue
                    lower = range_limit_sr(key - adjust)
                    higher = range_limit_sr(key - adjust)

                    if lower not in keys:
                        self._support_queue[lower].append(player_in_queue)
                        keys.append(lower)

                    if higher not in keys:
                        self._support_queue[higher].append(player_in_queue)
                        keys.append(higher)
