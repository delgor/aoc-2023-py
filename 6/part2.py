from pathlib import Path
from collections import namedtuple
from pprint import pprint


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

time = int(input[0].replace(" ", "")[5:])
distance = int(input[1].replace(" ", "")[9:])

max_accel = int(time / 2)
while (time - max_accel) * max_accel > distance:
    max_accel += 1
max_accel -= 1
min_accel = time - max_accel
range = max_accel - min_accel + 1

print(f"To beat {distance}mm over {time}ms we need to accel between {min_accel}ms and {max_accel}ms (range {range})")
