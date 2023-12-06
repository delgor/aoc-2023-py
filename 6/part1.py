from pathlib import Path
from collections import namedtuple
from pprint import pprint


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)


def load_integer_list(input: str) -> [int]:
    # Discard empty elements, e.g. between multiple space when used for block indentation
    filter_func = lambda x: len(x) > 0

    numbers = list(map(int, filter(filter_func, input.split(" "))))
    return numbers


times = load_integer_list(input[0][10:])
distances = load_integer_list(input[1][10:])

races = zip(times, distances)

prod_of_margins = 1

for time, distance in races:
    max_accel = int(time / 2)
    while (time - max_accel) * max_accel > distance:
        max_accel += 1
    max_accel -= 1
    min_accel = time - max_accel
    print(f"To beat {distance}mm over {time}ms we need to accel between {min_accel}ms and {max_accel}ms")
    range = max_accel - min_accel + 1

    prod_of_margins *= range

print(f"prod_of_margins: {prod_of_margins}")
