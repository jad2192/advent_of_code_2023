from collections import defaultdict
from functools import cmp_to_key
from typing import List, Literal, Tuple

CARD_RANK_ORDER = "AKQJT98765432"
WILD_CARD_RANK_ORDER = "AKQT98765432J"


class Hand:
    def __init__(self, hand_string: str, jokers_wild: bool = False):
        self.hand = list(hand_string)
        self.jokers_wild = jokers_wild
        if not jokers_wild:
            self.card_ranks = [CARD_RANK_ORDER.index(c) for c in list(self.hand)]
        else:
            self.card_ranks = [WILD_CARD_RANK_ORDER.index(c) for c in list(self.hand)]

    def hand_strength(self) -> int:
        counts = {card: self.hand.count(card) for card in self.hand + ["dummy"]}
        joker_count = 0
        if self.jokers_wild:
            joker_count = int(counts.get("J", 0))
            counts["J"] = 0
        sorted_cnts = sorted(counts.values())
        return 2 * (sorted_cnts[-1] + joker_count) + sorted_cnts[-2]  # Dummy ensures len(sorted_count) >= 2


def hand_compare(hand1: Hand, hand2: Hand) -> Literal[-1, 0, 1]:
    """Check if hand1 > hand2"""
    if hand1.hand_strength() != hand2.hand_strength():
        return 2 * int(hand1.hand_strength() > hand2.hand_strength()) - 1
    else:
        for card_rank_h1, card_rank_h2 in zip(hand1.card_ranks, hand2.card_ranks):
            if card_rank_h1 != card_rank_h2:
                # My encoding makes a lower card rank beat a higher card rank
                return 2 * (card_rank_h1 < card_rank_h2) - 1
        return 0


def hand_bid_compare(hand_and_bid1: Tuple[Hand, int], hand_and_bid2: Tuple[Hand, int]) -> Literal[-1, 0, 1]:
    return hand_compare(hand_and_bid1[0], hand_and_bid2[0])


def load_hands_and_bids(input_fp: str, jokers_wild: bool = False) -> List[Tuple[Hand, int]]:
    return [
        (Hand(line.split(" ")[0], jokers_wild), int(line.split(" ")[1])) for line in open(input_fp).read().split("\n")
    ]


def get_winnings(hands_and_bids: List[Tuple[Hand, int]]) -> int:
    return sum((k + 1) * hb[1] for k, hb in enumerate(sorted(hands_and_bids, key=cmp_to_key(hand_bid_compare))))


# Tests
test_hands_and_bids = load_hands_and_bids("inputs/day07/test.txt")
test_hands_and_bids_wild = load_hands_and_bids("inputs/day07/test.txt", jokers_wild=True)
assert get_winnings(test_hands_and_bids) == 6440
assert get_winnings(test_hands_and_bids_wild) == 5905


# Solutions
hands_and_bids = load_hands_and_bids("inputs/day07/main.txt")
hands_and_bids_wild = load_hands_and_bids("inputs/day07/main.txt", jokers_wild=True)
print(f"Part 1: Total winnings - {get_winnings(hands_and_bids)}")
print(f"Part 2: Total winnings - {get_winnings(hands_and_bids_wild)}")
