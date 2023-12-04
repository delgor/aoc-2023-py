from pathlib import Path
import re


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

sum = 0

for line in input:
    print(f"line: {line}")
    # line example: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    card_id, raw_numbers = line.split(": ", 1)
    card_id = int(card_id[5:])

    # Discard empty elements, e.g. between multiple space when used for block indentation
    filter_func = lambda x: len(x) > 0

    # Convert to int
    map_func = int

    winning_numbers, draw_numbers = raw_numbers.split(" | ", 1)
    winning_numbers = list(
        map(map_func, filter(filter_func, winning_numbers.split(" ")))
    )
    draw_numbers = list(map(map_func, filter(filter_func, draw_numbers.split(" "))))

    # Calculate win
    card_win = 0.5
    for draw_number in draw_numbers:
        if draw_number in winning_numbers:
            card_win *= 2

    # This will clamp 0.5 to 0, if no win was drawn. This is simpler than nesting another if inside the above loop imho
    card_win = int(card_win)

    print(
        f"Card {card_id}: win at {winning_numbers}, you got {draw_numbers}. points: {card_win}"
    )

    sum += card_win

print(f"sum: {sum}")
