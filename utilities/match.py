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

    def average_sr(self):
        tank_sr = self.tank.get_tank_sr()
        dps_sr1 = self.dps1.get_dps_sr()
        dps_sr2 = self.dps2.get_dps_sr()
        support_sr1 = self.support1.get_support_sr()
        support_sr2 = self.support1.get_support_sr()
        srs = [tank_sr, dps_sr1, dps_sr2, support_sr1, support_sr2]
        scales = [.3, .2, .15, .15, .2]
        avg_sr = 0
        for v, s in zip(srs, scales):
            avg_sr += s * v
        return avg_sr


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
        t1_sr = self.team1.average_sr()
        t2_sr = self.team2.average_sr()
        m = (t2_sr - t1_sr) / 1000
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
                'probability': prob,
                'probability_diff': abs(prob - (1-prob)),
                't1_win': win,
                't1_sr': self.team1.average_sr(),
                't2_sr': self.team2.average_sr(),
                'sr_diff': abs(self.team1.average_sr()-self.team2.average_sr())
            }


