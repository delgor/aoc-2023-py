from pathlib import Path
from collections import namedtuple
from pprint import pprint
from enum import IntEnum


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

card_strength = {
    "A": 15,
    "K": 14,
    "Q": 13,
    "J": 12,
    "T": 11,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


class HandType(IntEnum):
    FIVE_OF_A_KIND = 10
    FOUR_OF_A_KIND = 9
    FULL_HOUSE = 8
    THREE_OF_A_KIND = 7
    TWO_PAIR = 6
    ONE_PAIR = 5
    HIGH_CARD = 4


class HandCls(object):
    def __init__(self, input):
        assert len(input) == 5
        self.str_hand = input
        self.num_hand = list(map(lambda x: card_strength[x], list(input)))

    def __str__(self):
        return self.str_hand

    @property
    def type(self) -> HandType:
        # sorted_hand = sorted(self.num_hand, reverse=True)

        # Get a sorted count of symbols
        symbol_counts = list()
        for symbol in set(self.num_hand):
            symbol_counts.append({"symbol": symbol, "count": self.num_hand.count(symbol)})
        symbol_counts = sorted(symbol_counts, key=lambda x: x["count"], reverse=True)

        # print(f"  {self}: {symbol_counts}")

        if symbol_counts[0]["count"] == 5:
            return HandType.FIVE_OF_A_KIND
        elif symbol_counts[0]["count"] == 4:
            return HandType.FOUR_OF_A_KIND
        elif symbol_counts[0]["count"] == 3 and symbol_counts[1]["count"] == 2:
            return HandType.FULL_HOUSE
        elif symbol_counts[0]["count"] == 3:
            return HandType.THREE_OF_A_KIND
        elif symbol_counts[0]["count"] == 2 and symbol_counts[1]["count"] == 2:
            return HandType.TWO_PAIR
        elif symbol_counts[0]["count"] == 2:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @property
    def sort_key(self):
        return self.type, *self.num_hand


all_hands = list()

for line in input:
    hand = HandCls(line[0:5])
    bid = int(line[6:])
    print(f"{hand}: {hand.type} {bid}")
    all_hands.append((hand, bid))

all_hands_sorted = sorted(all_hands, key=lambda x: x[0].sort_key)

rank = 1
total_winnings = 0
for hand, bid in all_hands_sorted:
    ranked_bid = bid * rank
    print(f"{hand} (sort {hand.sort_key}, bid {bid}, rank {rank}, ranked_bid: {ranked_bid})")
    total_winnings += ranked_bid
    rank += 1

print(f"total winnings: {total_winnings}")
