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
    # Optimal time is t/2. This can be derived via math:
    #     dist(t_accel) = t_accel * t_move  | insert t = t_accel + t_move
    # <=> dist(t_accel) = t_accel * (t - t_accel) = t*t_accel - t_accel^2  | now derive
    #  -> d/dt_accel = t - 2*t_accel + c  | =0 to find extreme points
    #                  t - 2*t_accel + c = 0
    #              <=> t_accel = t+c/2
    # This is used as a starting point, because it is always inside [min_accel, max_accel]
    #
    # From a sharp eye (probably can be derived too) we notice that min_accel+max_accel = time holds.
    # So we only search into one direction, and calculate the other bound from that.
    # Searching upwards seems faster (upper bound in examples is always nearer to t/2)
    max_accel = int(time / 2)
    while (time - max_accel) * max_accel > distance:
        max_accel += 1
    max_accel -= 1
    min_accel = time - max_accel
    print(f"To beat {distance}mm over {time}ms we need to accel between {min_accel}ms and {max_accel}ms")
    range = max_accel - min_accel + 1

    prod_of_margins *= range

print(f"prod_of_margins: {prod_of_margins}")
