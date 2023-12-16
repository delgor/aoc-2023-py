from pathlib import Path
from collections import namedtuple


def aoc_hash(input_str):
    current_hash = 0
    for char in input_str:
        current_hash += ord(char)  # This is unicode and not ASCII. But surely our input is compatible enough, right?
        current_hash *= 17
        current_hash %= 256
    return current_hash


assert aoc_hash("HASH") == 52


## Load file
p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)
input_line = input_lines[0]
input_line_elems = input_line.split(",")

## Part 1
sum = 0
for elem in input_line_elems:
    sum += aoc_hash(elem)
print(f"part1 sum: {sum}")
