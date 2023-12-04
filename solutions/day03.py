from functools import reduce
from typing import List, Literal, Set, Tuple, TypeAlias

Schematic: TypeAlias = List[str]


def parse_schematic(input_fp: str) -> Schematic:
    return open(input_fp).read().split("\n")


def generate_grid_neighbors(row_ix: int, col_ix: int, num_rows: int, num_cols: int) -> Set[Tuple[int, int]]:
    plus_mins = {-1, 0, 1}
    possible_directions = [
        (min(num_cols - 1, max(0, row_ix + dx)), min(num_cols - 1, max(0, col_ix + dy)))
        for dx in plus_mins
        for dy in plus_mins
    ]
    return set(possible_directions).difference({(row_ix, col_ix)})


def symbol_check(symbol: str) -> bool:
    return symbol != "." and not symbol.isdigit()


def get_parts_numbers(schematic: Schematic, return_type: Literal["part_nos", "gear_ratios"] = "part_nos") -> List[int]:
    N, M = len(schematic), len(schematic[0])  # num rows and cols
    # Parse grid postions of all integers
    part_nos = []
    part_pos_dict = {}
    gear_ratio_pos = []
    for row_ix, row in enumerate(schematic):
        cur_int = ""
        cur_positions = []
        for col_ix, chr in enumerate(row):
            if chr.isdigit():
                cur_int += chr
                cur_positions.append((row_ix, col_ix))
            if cur_int and (col_ix == M - 1 or not chr.isdigit()):
                # case we have found full integer
                neighbors = reduce(set.union, [generate_grid_neighbors(pos[0], pos[1], N, M) for pos in cur_positions])
                if any(symbol_check(schematic[nbr[0]][nbr[1]]) for nbr in neighbors):
                    part_nos.append(int(cur_int))
                    # keep track of individual digit positions and there corresponding part no
                    #  / all digit positions in the integer.
                    part_pos_dict = part_pos_dict | {pos: (tuple(cur_positions), int(cur_int)) for pos in cur_positions}
                cur_int = ""
                cur_positions = []
            if chr == "*" and return_type == "gear_ratios":
                neighbors = generate_grid_neighbors(row_ix, col_ix, N, M)
                # record all neigbors of gear that are a digit, hence that digit belongs to a
                # part no (since "*"" is a symbol != "."). Will use part_pos_dict to get unique part neighbors
                gear_ratio_pos.append([nbr for nbr in neighbors if schematic[nbr[0]][nbr[1]].isdigit()])
    if return_type == "part_nos":
        return part_nos
    else:
        # dedupe gear digit neighbors
        positions = [list(set([part_pos_dict[pos] for pos in gear])) for gear in gear_ratio_pos]
        return [gear[0][1] * gear[-1][1] for gear in positions if len(gear) == 2]


# Tests
test_schema = parse_schematic("inputs/day03/test.txt")
assert sum(get_parts_numbers(test_schema)) == 4361
assert sum(get_parts_numbers(test_schema, return_type="gear_ratios")) == 467835

# Solutions
schema = parse_schematic("inputs/day03/main.txt")
print(f"Part 1: The Sum of Parts Numbers - {sum(get_parts_numbers(schema))}")
print(f"Part 2: The Sum of Gear Rations - {sum(get_parts_numbers(schema, return_type='gear_ratios'))}")
