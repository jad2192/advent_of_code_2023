from typing import Dict, List, Set, Tuple, TypeAlias

GameMap: TypeAlias = Dict[int, Tuple[List[int], Set[int]]]


def load_games(input_fp: str) -> GameMap:
    # Track game numbers as the a tuple, map it to set of of winning numbers, append row number
    # To end of game numbers to ensure unique keys.
    game_map = {}
    split_input = [line.split(": ")[1].split(" | ") for line in open(input_fp).read().split("\n")]
    for k, game in enumerate(split_input):
        game_map[k] = ([int(d) for d in game[1].split()], set(int(d) for d in game[0].split()))
    return game_map


def count_winning_points(games: GameMap) -> List[int]:
    points = []
    for _, game_config in games.items():
        game_numbers, winning_numbers = game_config
        game_winning_numbers = [num for num in game_numbers if num in winning_numbers]
        points.append(int(2 ** (len(game_winning_numbers) - 1)))
    return points


def get_game_winning_cards(game_no: int, game_numbers: List[int], winning_numbers: Set[int]) -> List[int]:
    return list(range(game_no + 1, game_no + 1 + len([num for num in game_numbers if num in winning_numbers])))


def count_total_scratchcards(games: GameMap) -> int:
    card_count = {game_no: 1 for game_no in range(len(games))}
    for game_no, game_config in games.items():
        won_cards = get_game_winning_cards(game_no, game_config[0], game_config[1])
        for winning_game_no in won_cards:
            card_count[winning_game_no] += card_count[game_no]
    return sum(card_count.values())


# Tests
test_games = load_games("inputs/day04/test.txt")
assert count_winning_points(test_games) == [8, 2, 2, 1, 0, 0]
assert count_total_scratchcards(test_games) == 30


# Solutions
games = load_games("inputs/day04/main.txt")
print(f"Part 1: The Scratchcards have a points total of - {sum(count_winning_points(games))}")
print(f"Part 2: Total Scratchcards Won - {count_total_scratchcards(games)}")
