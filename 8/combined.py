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


def how_many_steps(start_node, end_condition, print=lambda x: x) -> int:
    current_node = start_node
    steps = 0
    while not end_condition(current_node):
        direction = walk_sequence[steps % len(walk_sequence)]
        if direction == "L":
            next_node = node_map[current_node].left
        elif direction == "R":
            next_node = node_map[current_node].right

        print(f"step {steps}: from {current_node} to {next_node}")

        steps += 1
        current_node = next_node

    return steps


## Part 1
steps_p1 = how_many_steps("AAA", lambda x: x == "ZZZ")
print(f"p1 total steps: {steps_p1}")

## Part 2
# This solution makes one assumption:
# all start nodes loop, starting again from the start node, after reaching their first ending Z
#
# If this was not the case, you'd need to detect loops manually, maybe handle the case where the loop does not line up
# with the end condition and offset, and then calculate the global solution from that.
# luckily, this is not needed here.
end_condition = lambda x: x[2] == "Z"

p2_start_nodes = list(filter(lambda x: x[2] == "A", node_map.keys()))
p2_to_target = {}
for p2_node in p2_start_nodes:
    p2_to_target[p2_node] = how_many_steps(p2_node, end_condition)

for p2_node in p2_start_nodes:
    print(f"p2 start at {p2_node} ends after {p2_to_target[p2_node]} steps")

import math

p2_steps = math.lcm(*p2_to_target.values())
print(f"p2 total steps: {p2_steps}")
