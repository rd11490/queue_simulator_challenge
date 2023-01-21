from utilities.constants import TANK, DPS, SUPPORT
from utilities.print_debug import print_debug

class CustomQueue:
    """
    Update this class however you want in order to make the most efficient queue possible.
    """

    def __init__(self):
        pass

    # REQUIRED
    def enqueue_player(self, player_in_queue):
        """
        Put a player in the queue
        :param player_in_queue: Takes in a PlayerInQueue Instance and places them in queue
        :return:
        """
        pass

    # REQUIRED
    def build_match(self):
        """
        The method for pulling out a group of players that would make a "balanced" game
        :return: None or A touple of touples: ((tank1, dps11, dps12, support11, support12), (tank2, dps21, dps22, support21, support22))
        """
        return None

        # return ((tank1, dps11, dps12, support11, support12), (tank2, dps21, dps22, support21, support22))
