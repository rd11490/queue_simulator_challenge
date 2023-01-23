import random
import numpy as np

from utilities.helpers import round_int, range_limit


class Team:
    def __init__(self, tank, dps1, dps2, support1, support2):
        self.tank = tank
        self.dps1 = dps1
        self.dps2 = dps2
        self.support1 = support1
        self.support2 = support2

    def average_mmr(self):
        tank_mmr = self.tank.get_tank_mmr()
        dps_mmr1 = self.dps1.get_dps_mmr()
        dps_mmr2 = self.dps2.get_dps_mmr()
        support_mmr1 = self.support1.get_support_mmr()
        support_mmr2 = self.support2.get_support_mmr()
        mmrs = [tank_mmr, dps_mmr1, dps_mmr2, support_mmr1, support_mmr2]
        scales = [.3, .2, .15, .15, .2]
        avg_mmr = 0
        for v, s in zip(mmrs, scales):
            avg_mmr += s * v
        return avg_mmr

    def average_match_mmr(self):
        tank_mmr = self.tank.get_tank_match_mmr()
        dps_mmr1 = self.dps1.get_dps_match_mmr()
        dps_mmr2 = self.dps2.get_dps_match_mmr()
        support_mmr1 = self.support1.get_support_match_mmr()
        support_mmr2 = self.support2.get_support_match_mmr()
        mmrs = [tank_mmr, dps_mmr1, dps_mmr2, support_mmr1, support_mmr2]
        scales = [.3, .2, .15, .15, .2]
        avg_mmr = 0
        for v, s in zip(mmrs, scales):
            avg_mmr += s * v
        return avg_mmr


class Match:
    AVG_MATCH_TIME = 15 * 60
    MATCH_TIME_SD = 3 * 60

    def __init__(self, team1, team2, clock):
        self.clock = clock
        self.team1 = team1
        self.team2 = team2
        self.time_limit = round_int(range_limit(np.random.normal(loc=self.AVG_MATCH_TIME, scale=self.MATCH_TIME_SD), 5 * 60, 40 * 60))
        self.start = self.clock.now()
        self.end = self.start + self.time_limit
        self.active = True
        self.sim_result = None

    def __str__(self):
        return f'Active: {self.active}, Start: {self.start}, End: {self.end}, Time: {self.time_limit}'

    def sim_match(self):
        t1_mmr = self.team1.average_match_mmr()
        t2_mmr = self.team2.average_match_mmr()
        m = (t2_mmr - t1_mmr) / 1000
        pt1 = 1 / (1 + 10 ** m)
        return pt1, random.random() <= pt1

    def is_active(self):
        return self.active

    def get_sim_results(self):
        return self.sim_result

    def tick(self):
        if self.clock.now() > self.end:
            self.active = False
            prob, win = self.sim_match()
            self.sim_result = {
                'Team 1 Estimated Probability To Win': prob,
                'ABS Value Probability To Win Difference': abs(prob - (1-prob)),
                'Team 1 Average MMR (weighted)': self.team1.average_mmr(),
                'Team 2 Average MMR (weighted)': self.team2.average_mmr(),
                'ABS MMR Difference': abs(self.team1.average_mmr() - self.team2.average_mmr())
            }


