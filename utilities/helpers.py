def round_int(val):
    return int(round(val))


def range_limit(val, low, high):
    if val < low:
        return low
    if val > high:
        return high
    return val


def range_limit_sr(val):
    return range_limit(val, 0, 5000)
