import datetime
import sys

import pandas as pd

from custom_queue import CustomQueue
from utilities.bucket_queue import BucketQueue
from utilities.clock import clock
from utilities.match import Team, Match
from utilities.player_base import PlayerBase
from utilities.player_in_queue import PlayerInQueue
from utilities.basic_queue import BasicQueue
from utilities.print_debug import print_debug
from utilities.servers import Servers
from optparse import OptionParser


def put_player_in_queue(player_base, queue):
    player = player_base.enqueue_random_player()
    if player is not None:
        player_in_queue = PlayerInQueue(player)
        queue.enqueue_player(player_in_queue)


def put_players_in_queue(player_base, queue, n):
    for i in range(n):
        put_player_in_queue(player_base, queue)


def dequeue_player(team, queue_stats, index):
    player = team[index]
    player.dequeue()
    if clock.now() > 60*60:
        queue_stats.append(player)
    return player


def build_team(team, queue_stats):
    tank1 = dequeue_player(team, queue_stats, 0)
    dps11 = dequeue_player(team, queue_stats, 1)
    dps12 = dequeue_player(team, queue_stats, 2)
    support11 = dequeue_player(team, queue_stats, 3)
    support12 = dequeue_player(team, queue_stats, 4)

    return Team(tank1.player, dps11.player, dps12.player, support11.player, support12.player)


def main():
    parser = OptionParser()
    parser.add_option("-q", "--queue", dest="queue",
                      help="The Queue to be tested, BASIC/BUCKET/CUSTOM")

    (options, args) = parser.parse_args()
    if (options.queue is None) or (options.queue not in ['BASIC', 'BUCKET', 'CUSTOM']):
        parser.print_help()
        sys.exit(1)

    if options.queue == 'BASIC':
        queue = BasicQueue()
    elif options.queue == 'BUCKET':
        queue = BucketQueue()
    else:
        queue = CustomQueue()

    player_base = PlayerBase(100000)
    servers = Servers(1000)
    put_players_in_queue(player_base, queue, 10000)
    queue_stats = []
    running = True
    while running:
        if clock.now() % 30 == 0:
            print_debug(f'Open Matches {servers.open_matches()}')
            while servers.open_matches() > 0:
                teams = queue.build_match()
                if teams is not None:
                    team1_players, team2_players = teams
                    team1 = build_team(team1_players, queue_stats)
                    team2 = build_team(team2_players, queue_stats)
                    match = Match(team1, team2, clock)
                    servers.start_match(match)
                    for p in team1_players + team2_players:
                        player_base.dequeue_player(p.player)
                else:
                    break
        clock.tick()
        servers.tick()
        queue.tick()
        put_players_in_queue(player_base, queue, 5)
        if clock.now() > (60 * 60 * 6):
            running = False

    time_in_queue = [{'Wait': p.time_in_queue(), 'Roles': p.player.roles, 'Id': p.player.id, 'Tank': p.player.get_tank_mmr(), 'DPS': p.player.get_dps_mmr(), 'Support': p.player.get_support_mmr()} for p in queue_stats]

    results = []
    for m in servers.completed_matches:
        results.append(m.get_sim_results())

    results_df = pd.DataFrame(results)
    results_df.to_csv(f'match_results_{options.queue}_{datetime.datetime.now()}.csv', index=False)
    results_desc = results_df.describe()
    mean_mmr_diff = results_desc.loc['mean']['ABS MMR Difference']
    std_mmr_diff = results_desc.loc['std']['ABS MMR Difference']

    wait_df = pd.DataFrame(time_in_queue)
    wait_df.to_csv(f'time_in_queue_{options.queue}_{datetime.datetime.now()}.csv', index=False)
    wait_desc = wait_df.describe()
    mean_wait = wait_desc.loc['mean']['Wait']
    std_wait = wait_desc.loc['std']['Wait']

    score_wait = int(mean_wait ** 2 + std_wait)
    score_mmr = int(mean_mmr_diff ** 2 + std_mmr_diff)

    score = score_mmr + score_wait

    print(f'Score: {score} - Wait Score: {score_wait} - MMR Score: {score_mmr}')
    print(results_desc)
    print(wait_desc)



if __name__ == "__main__":
    main()
