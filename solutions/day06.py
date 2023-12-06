import math
from typing import List, Tuple, TypeAlias

RaceStats: TypeAlias = List[Tuple[int, int]]  # (duration, record) = single stat


def load_race_stats(input_fp: str) -> RaceStats:
    lines = open(input_fp).read().split("\n")
    stats = []
    for d, r in zip(lines[0].replace("Time:", "").split(), lines[1].replace("Distance:", "").split()):
        stats.append((int(d), int(r)))
    return stats


def get_no_winning_times(duration: int, record: int) -> int:
    # Need to solve record < (duration - hold_time) * hold_time or in polynomial form
    # 0 > x^2 - Dx + R  (D = duration, x = holdtime, R = record)
    discrim_root = math.sqrt(duration**2 - (4 * record))
    return math.ceil(0.5 * (duration + discrim_root)) - int(0.5 * (duration - discrim_root)) - 1


def get_margin_of_error(race_stats: RaceStats) -> int:
    margin = 1
    for duration, record in race_stats:
        margin *= get_no_winning_times(duration, record)
    return margin


def fix_race_stat(race_stats: RaceStats) -> Tuple[int, int]:
    # Take list of races and concatenate into the corrected single race.
    duration_str, record_str = "", ""
    for duration, record in race_stats:
        duration_str += str(duration)
        record_str += str(record)
    return int(duration_str), int(record_str)


# Tests
test_races = load_race_stats("inputs/day06/test.txt")
assert get_no_winning_times(15, 40) == 8
assert get_margin_of_error(test_races) == 288
assert fix_race_stat(test_races) == (71530, 940200)


# Solutions
races = load_race_stats("inputs/day06/main.txt")
long_d, long_r = fix_race_stat(races)
print(f"Part 1: Margin of Error - {get_margin_of_error(races)}")
print(f"Part 2: Number of ways to win - {get_no_winning_times(long_d, long_r)}")
