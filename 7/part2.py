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
    "T": 11,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,  # J is now weakest individual card
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
        joker_symbol = card_strength["J"]
        joker_count = self.num_hand.count(joker_symbol)
        # Count only non-jokers - we will later check joker count separately in symbol_count()
        for symbol in set(self.num_hand):
            if symbol != joker_symbol:
                symbol_counts.append({"symbol": symbol, "count": self.num_hand.count(symbol)})
        symbol_counts = sorted(symbol_counts, key=lambda x: x["count"], reverse=True)

        # print(f"  {self}: {symbol_counts}")

        def symbol_count(pos):
            # Catch "all jokers" case first - then symbol_counts will be empty and cause errors.
            # With 4 jokers, there would be a five of a kind
            # With 3 jokers, there would be a four of a kind
            # With 2 jokers, there are enough symbols that either pos==1 exists,
            # or if there is only one other symbol, it would be 5 of a kind, which is checked first.
            # Yes, this is a bit hacky on the index access front.
            if joker_count == 5:
                return 5

            actual_count = symbol_counts[pos]["count"]

            # Only count jokers if the symbol is at position 0 (most occurrences).
            # We know this cannot be a joker itself.
            if pos == 0:
                actual_count += joker_count

            return actual_count

        if symbol_count(0) == 5:
            return HandType.FIVE_OF_A_KIND
        elif symbol_count(0) == 4:
            return HandType.FOUR_OF_A_KIND
        elif symbol_count(0) == 3 and symbol_count(1) == 2:
            return HandType.FULL_HOUSE
        elif symbol_count(0) == 3:
            return HandType.THREE_OF_A_KIND
        elif symbol_count(0) == 2 and symbol_count(1) == 2:
            return HandType.TWO_PAIR
        elif symbol_count(0) == 2:
            return HandType.ONE_PAIR
        else:
            return HandType.HIGH_CARD

    @property
    def sort_key(self):
        # sorted() already handles multiple elements in a sort key correctly, we just need to provide all elements
        return self.type, *self.num_hand


all_hands = list()

for line in input:
    hand = HandCls(line[0:5])
    bid = int(line[6:])
    print(f"Read hand {hand}: {hand.type} {bid}")
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
