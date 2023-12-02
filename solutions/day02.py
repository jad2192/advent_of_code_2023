from typing import Dict, List, Tuple, TypeAlias

RGBCounts: TypeAlias = Tuple[int, int, int]


def parse_game_results(input_path: str) -> List[List[str]]:
    # Split each line by Game delimiter, ": ", then by round set delimiter "; ". List index will track game no.
    return [line.split(": ")[1].split("; ") for line in open(input_path).read().split("\n")]


def is_valid_game(seen_min_counts: RGBCounts, game_max_counts: RGBCounts) -> bool:
    return all(seen_min_counts[k] <= game_max_counts[k] for k in range(3))


def get_min_colors_per_game(game_results: List[List[str]]) -> Dict[int, RGBCounts]:
    min_count_dict = {}
    for k, game in enumerate(game_results):
        min_r, min_g, min_b = 0, 0, 0
        for round in game:
            for color in round.split(", "):
                match color.split(" "):
                    case [num_cube, "red"]:
                        min_r = max(min_r, int(num_cube))
                    case [num_cube, "green"]:
                        min_g = max(min_g, int(num_cube))
                    case [num_cube, "blue"]:
                        min_b = max(min_b, int(num_cube))
        min_count_dict[k + 1] = (min_r, min_g, min_b)
    return min_count_dict


def get_valid_games(min_colors: Dict[int, RGBCounts], max_colors: RGBCounts) -> List[int]:
    return [key for key, val in min_colors.items() if is_valid_game(val, max_colors)]


def min_color_set_power(min_counts: RGBCounts) -> int:
    return min_counts[0] * min_counts[1] * min_counts[2]


# Tests
test_game = parse_game_results("inputs/day02/day02_test.txt")
test_maxes: RGBCounts = (12, 13, 14)
test_min_colors = get_min_colors_per_game(test_game)
assert get_valid_games(test_min_colors, test_maxes) == [1, 2, 5]
assert [min_color_set_power(val) for val in test_min_colors.values()] == [48, 12, 1560, 630, 36]


# Part 1
game_results = parse_game_results("inputs/day02/day02.txt")
maxes: RGBCounts = (12, 13, 14)
min_colors = get_min_colors_per_game(game_results)
print(f"Part 1: The sum of the IDs of valid games is - {sum(get_valid_games(min_colors, maxes))}")
print(f"Part 2: Sum of the all game set powers - {sum(min_color_set_power(min_c) for min_c in min_colors.values())}")
