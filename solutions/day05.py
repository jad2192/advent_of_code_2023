from functools import partial
from typing import Dict, List, Optional, Tuple, TypeAlias

Interval: TypeAlias = Tuple[int, int]  # We will represent union of intervals as an ordered even numbered list.
AlmanacMap: TypeAlias = Dict[str, partial[Tuple[int, str]]]


def get_interval_intersection_and_difference(
    intv1: Interval, intv2: Interval
) -> Tuple[Optional[Interval], List[Interval]]:
    """Calculate the intersection and (non-symmetric) set difference intv1 - intv2"""
    difference = []
    if (intv1[1] < intv2[0]) or (intv2[1] < intv1[0]):
        return None, [intv1]
    else:
        intersection = (max(intv1[0], intv2[0]), min(intv1[1], intv2[1]))
        if intv2[0] > intv1[0]:
            difference.append((intv1[0], max(intv1[0], intv2[0] - 1)))
        if intv1[1] > intv2[1]:
            difference.append((min(intv1[1], intv2[1] + 1), intv1[1]))
        return intersection, difference


def attribute_map(
    input_ranges: List[Interval],
    source_ranges: List[Interval],
    target_ranges: List[Interval],
    target_name: str,
) -> Tuple[List[Interval], str]:
    mapped_intervals: List[Interval] = []
    cur_differences: List[Interval] = input_ranges
    for source_range, target_range in zip(source_ranges, target_ranges):
        new_differences: List[Interval] = []
        for input_range in cur_differences:
            intersection, differences = get_interval_intersection_and_difference(input_range, source_range)
            # Smart extension to ensure min lower bound always first element
            new_differences = sorted(new_differences + differences, key=lambda intv: intv[0])
            if intersection is not None:
                mapped_range = (
                    target_range[0] + (intersection[0] - source_range[0]),
                    target_range[0] + (intersection[1] - source_range[0]),
                )
                # We will smartly append to ensure first value in mapped interval has min lb
                mapped_intervals = sorted([mapped_range] + mapped_intervals, key=lambda intv: intv[0])
        cur_differences = new_differences
    # combine any unmapped intervals with mapped intervals, ensure min lb always first element
    if not cur_differences or not mapped_intervals or cur_differences[0][0] > mapped_intervals[0][0]:
        return mapped_intervals + cur_differences, target_name
    else:
        return cur_differences + mapped_intervals, target_name


def load_almanac_map(input_fp: str) -> Tuple[List[Interval], List[Interval], AlmanacMap]:
    parts = open(input_fp).read().split("\n\n")
    seeds_nos = [int(d) for d in parts[0][len("seeds: ") :].split()]
    seed_singletons = [(seed, seed) for seed in seeds_nos]
    seed_ranges = [(seeds_nos[k], seeds_nos[k] + seeds_nos[k + 1] - 1) for k in range(0, len(seeds_nos), 2)]
    almanac_map = {}
    for raw_mapping in parts[1:]:
        map_parts = raw_mapping.split("\n")
        source, target = tuple(map_parts[0].split()[0].split("-to-"))
        target_ranges, source_ranges = [], []
        for map in map_parts[1:]:
            target_start, source_start, intv_len = tuple(map.split())
            target_ranges.append((int(target_start), int(target_start) + int(intv_len) - 1))
            source_ranges.append((int(source_start), int(source_start) + int(intv_len) - 1))
        almanac_map[source] = partial(
            attribute_map,
            target_name=str(target),
            source_ranges=list(source_ranges),
            target_ranges=list(target_ranges),
        )
    return seed_singletons, seed_ranges, almanac_map


def get_min_seed_location(seed_ranges: List[Interval], almanac_map: AlmanacMap) -> int:
    target = "seed"
    return_val = seed_ranges
    while target != "location":
        return_val, target = almanac_map[target](return_val)
    return return_val[0][0]


# Tests
test_seeds, test_seed_ranges, test_map = load_almanac_map("inputs/day05/test.txt")
assert get_min_seed_location(test_seeds, test_map) == 35
assert get_min_seed_location(test_seed_ranges, test_map) == 46


# Solutions
seeds, seed_ranges, almanac_map = load_almanac_map("inputs/day05/main.txt")
print(f"Part 1: Closest Location - {get_min_seed_location(seeds, almanac_map)}")
print(f"Part 2: Closet Location - {get_min_seed_location(seed_ranges, almanac_map)}")
