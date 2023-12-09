from functools import reduce
from math import lcm
from typing import Dict, List, Tuple, TypeAlias

NetworkMap: TypeAlias = Dict[str, Dict[str, str]]


def get_network_map(input_rows: str) -> NetworkMap:
    return {row[:3]: {"L": row[-9:-6], "R": row[-4:-1]} for row in input_rows.split("\n")}


def count_steps(input_fp: str) -> int:
    step_seq, map_rows = tuple(open(input_fp).read().split("\n\n"))
    network_map = get_network_map(map_rows)
    steps, position = 0, "AAA"
    while position != "ZZZ":
        position = network_map[position][step_seq[steps % len(step_seq)]]
        steps += 1
    return steps


def get_cycles(step_seq: str, network_map: NetworkMap, start_pos: str) -> List[Tuple[int, int]]:
    steps, position, dx = 0, start_pos, 0
    seen_pos, z_locs = {}, []
    while (dx, position) not in seen_pos:
        seen_pos[(dx, position)] = steps
        if position.endswith("Z"):
            z_locs.append((steps, position))
        position = network_map[position][step_seq[dx]]
        steps += 1
        dx = steps % len(step_seq)
    return [(z_pos[0], steps - seen_pos[(dx, position)]) for z_pos in z_locs]


def count_spooky_ghost_steps(input_fp: str) -> int:
    step_seq, map_rows = tuple(open(input_fp).read().split("\n\n"))
    network_map = get_network_map(map_rows)
    cycles = []
    for start in [pos for pos in network_map if pos.endswith("A")]:
        cycles.extend(get_cycles(step_seq, network_map, start))
    # This only works assuming one Z pos in cycle per start. If this were not the case
    # we'd have to take the min LCM over all choices of a single Z pos per start.
    if all(cycle[1] % cycle[0] == 0 for cycle in cycles):
        return lcm(*[c[0] for c in cycles])
    # Much harder needs CRT + coprime conditions on cycle lengths...But my data seems to satisfy above...
    else:
        return 1


# Tests
assert count_steps("inputs/day08/test.txt") == 2
assert count_steps("inputs/day08/test2.txt") == 6
assert count_spooky_ghost_steps("inputs/day08/test3.txt") == 6

# Solutions
print(f"Part 1: Total Steps - {count_steps('inputs/day08/main.txt')}")
print(f"Part 2: Total Spooky Ghost Steps - {count_spooky_ghost_steps('inputs/day08/main.txt')}")
