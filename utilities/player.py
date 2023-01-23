import numpy as np
import random
from utilities.constants import TANK, DPS, SUPPORT
from utilities.helpers import range_limit_sr, round_int
import uuid


class Player:
    MAX_MMR = 5000
    MIN_MMR = 0
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
        self._base_mmr = round_int(range_limit_sr(np.random.normal(loc=2500, scale=500)))
        low_range = self._base_mmr - self.ROLE_RANGE
        high_range = self._base_mmr + self.ROLE_RANGE
        self._tank_mmr = round_int(range_limit_sr(np.random.randint(low_range, high_range)))
        self._dps_mmr = round_int(range_limit_sr(np.random.randint(low_range, high_range)))
        self._support_mmr = round_int(range_limit_sr(np.random.randint(low_range, high_range)))
        self.roles = random.choice(self.ROLE_COMBOS)

    def __str__(self):
        return f'Player: {self.id}, Base SR: {self._base_mmr}, Roles: {self.roles}'

    def print(self):
        print(f'Player: {self.id}')
        print(f'Base MMR: {self._base_mmr}')
        print(f'Tank MMR: {self._tank_mmr}')
        print(f'DPS MMR: {self._dps_mmr}')
        print(f'Support MMR: {self._support_mmr}')
        print(f'Preferred Roles: {self.roles}')

    def get_match_sr(self, role):
        if role == TANK:
            avg = self._tank_mmr
        elif role == DPS:
            avg = self._dps_mmr
        else:
            avg = self._support_mmr
        return round_int(range_limit_sr(np.random.normal(loc=avg, scale=self.GAME_TO_GAME_SD)))

    def get_tank_match_mmr(self):
        return self.get_match_sr(TANK)

    def get_dps_match_mmr(self):
        return self.get_match_sr(DPS)

    def get_support_match_mmr(self):
        return self.get_match_sr(SUPPORT)

    def get_tank_mmr(self):
        return self._tank_mmr

    def get_dps_mmr(self):
        return self._dps_mmr

    def get_support_mmr(self):
        return self._support_mmr
