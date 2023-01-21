import sys

import pandas as pd

from custom_queue import CustomQueue
from utilities.clock import clock
from utilities.match import Team, Match
from utilities.player_base import PlayerBase
from utilities.player_in_queue import PlayerInQueue
from utilities.dumb_queue import BasicQueue
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
                      help="The Queue to be tested, BASIC/CUSTOM")

    (options, args) = parser.parse_args()
    if (options.queue is None) or (options.queue not in ['BASIC', 'CUSTOM']):
        parser.print_help()
        sys.exit(1)

    if options.queue == 'BASIC':
        queue = BasicQueue()
    else:
        queue = CustomQueue()

    player_base = PlayerBase(100000)
    servers = Servers(1000)
    put_players_in_queue(player_base, queue, 10000)
    queue_stats = []
    running = True
    while running:
        if clock.now() % 30 == 0:
            # print_debug(f'Open Matches {servers.open_matches()}')
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
        put_players_in_queue(player_base, queue, 5)
        if clock.now() > (60 * 60 * 6):
            running = False

    time_in_queue = [{'wait': p.time_in_queue(), 'roles': p.player.roles} for p in queue_stats]

    results = []
    for m in servers.completed_matches:
        results.append(m.get_sim_results())

    results_df = pd.DataFrame(results)
    print(results_df.describe())

    wait_df = pd.DataFrame(time_in_queue)
    print(wait_df.describe())



if __name__ == "__main__":
    main()
