from utilities.clock import clock


def print_debug(string):
    print(f'({clock.now()}): {string}')