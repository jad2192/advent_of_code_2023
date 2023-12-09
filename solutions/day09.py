from typing import List


def load_sequences(input_fp: str) -> List[List[int]]:
    return [[int(d) for d in line.split()] for line in open(input_fp).read().split("\n")]


def extrapolate_sequence(sequence: List[int], extrap_forward: bool) -> int:
    differences = [sequence] if extrap_forward else [sequence[::-1]]
    cur_seq = differences[0]
    while set(cur_seq) != {0} and len(cur_seq) > 1:
        cur_seq = [cur_seq[k + 1] - cur_seq[k] for k in range(len(cur_seq) - 1)]
        differences.append(cur_seq)
    exp_val = 0
    for diff_seq in differences[::-1]:
        exp_val += diff_seq[-1]
    return exp_val


def sum_extrapolated_vals(input_fp: str, extrap_forward: bool = True) -> int:
    sequences = load_sequences(input_fp)
    return sum([extrapolate_sequence(seq, extrap_forward) for seq in sequences])


# Tests
assert sum_extrapolated_vals("inputs/day09/test.txt") == 114
assert sum_extrapolated_vals("inputs/day09/test.txt", False) == 2


# Solutions
print(f"Part 1: Sum of Extrapolated Vals - {sum_extrapolated_vals('inputs/day09/main.txt')}")
print(f"Part 2: Sum of Extrapolated Vals - {sum_extrapolated_vals('inputs/day09/main.txt', False)}")
