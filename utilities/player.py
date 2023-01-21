import numpy as np
import random
from utilities.constants import TANK, DPS, SUPPORT
from utilities.helpers import range_limit_sr, round_int
import uuid


class Player:
    MAX_SR = 5000
    MIN_SR = 0
    ROLE_RANGE = 500
    GAME_TO_GAME_SD = 100
    ROLE_COMBOS = [
        [TANK],
        [DPS],
        [SUPPORT],
        [TANK, DPS],
        [TANK, SUPPORT],
        [DPS, SUPPORT],
        [TANK, DPS, SUPPORT]
    ]

    def __init__(self):
        self.id = uuid.uuid4()
        self._base_sr = np.random.normal(loc=2500, scale=500)
        low_range = self._base_sr - self.ROLE_RANGE
        high_range = self._base_sr + self.ROLE_RANGE
        self._tank_sr = np.random.randint(low_range, high_range)
        self._dps_sr = np.random.randint(low_range, high_range)
        self._support_sr = np.random.randint(low_range, high_range)
        self.roles = random.choice(self.ROLE_COMBOS)

    def __str__(self):
        return f'Player: {self.id}, Base SR: {self._base_sr}, Roles: {self.roles}'

    def print(self):
        print(f'Player: {self.id}')
        print(f'Base SR: {self._base_sr}')
        print(f'Tank SR: {self._tank_sr}')
        print(f'DPS SR: {self._dps_sr}')
        print(f'Support SR: {self._support_sr}')
        print(f'Preferred Roles: {self.roles}')

    def get_match_sr(self, role):
        if role == TANK:
            avg = self._tank_sr
        elif role == DPS:
            avg = self._dps_sr
        else:
            avg = self._support_sr
        return round_int(range_limit_sr(np.random.normal(loc=avg, scale=self.GAME_TO_GAME_SD)))

    def get_tank_sr(self):
        return self.get_match_sr(TANK)

    def get_dps_sr(self):
        return self.get_match_sr(DPS)

    def get_support_sr(self):
        return self.get_match_sr(SUPPORT)