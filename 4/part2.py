from pathlib import Path


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

sum = 0

# We start with 1 original for each card
card_counts = [1] * len(input)

for line_no in range(0, len(input)):
    line = input[line_no]
    print(f"line: {line}")
    # line example: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    card_id, raw_numbers = line.split(": ", 1)
    card_id = int(card_id[5:])

    # Discard empty elements, e.g. between multiple space when used for block indentation
    filter_func = lambda x: len(x) > 0

    winning_numbers, draw_numbers = raw_numbers.split(" | ", 1)
    winning_numbers = list(map(int, filter(filter_func, winning_numbers.split(" "))))
    draw_numbers = list(map(int, filter(filter_func, draw_numbers.split(" "))))

    # Calculate win
    card_win = 0
    for draw_number in draw_numbers:
        if draw_number in winning_numbers:
            card_win += 1

    # Apply additional cards
    # For each of the next n cards, apply our current cards count
    additional_cards = card_counts[line_no]
    for next_card in range(0, card_win):
        card_counts[line_no + 1 + next_card] += additional_cards

    print(f"Card {card_id}: win at {winning_numbers}, you got {draw_numbers}. points: {card_win}")


from functools import reduce

sum = reduce(lambda x, y: x + y, card_counts, 0)

print(f"sum: {sum}")
