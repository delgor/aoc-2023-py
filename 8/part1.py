from pathlib import Path
from collections import namedtuple
from pprint import pprint
from enum import IntEnum


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)


directions = namedtuple("directions", "left right")

walk_sequence = list(input[0])

node_map = {}

for line in input[2:]:
    source = line[0:3]
    left = line[7:10]
    right = line[12:15]

    node_map[source] = directions(left, right)

    # print(line)
    # print(f"{source}: {left}, {right}")

current_node = "AAA"
steps = 0
while current_node != "ZZZ":
    direction = walk_sequence[steps % len(walk_sequence)]
    if direction == "L":
        next_node = node_map[current_node].left
    elif direction == "R":
        next_node = node_map[current_node].right

    print(f"step {steps}: from {current_node} to {next_node}")

    steps += 1
    current_node = next_node

print(f"total steps: {steps}")
