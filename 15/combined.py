from pathlib import Path
from collections import namedtuple
import re


def aoc_hash(input_str):
    current_hash = 0
    for char in input_str:
        current_hash += ord(char)  # This is unicode and not ASCII. But surely our input is compatible enough, right?
        current_hash *= 17
        current_hash %= 256
    return current_hash


assert aoc_hash("HASH") == 52


class aoc_hashmap:
    re_operation = re.compile(r"(.+)([-=])([0-9]+)?")

    def __init__(self):
        # Do not use `[[]]*256` - that will create a list with 256 references to the same inner list.
        self.boxes = []
        for _ in range(256):
            self.boxes.append([])

    def op_do(self, operation):
        parameters_match = aoc_hashmap.re_operation.fullmatch(operation)
        label = parameters_match.group(1)
        op = parameters_match.group(2)
        focal_length = int(parameters_match.group(3)) if parameters_match.group(3) else None

        print(
            f"parsed operation: label={label} op '{op}', focal length = {focal_length}, will apply to box {aoc_hash(label)}"
        )

        if op == "-":
            self.op_remove(label)
        elif op == "=":
            self.op_insert(label, focal_length)

    def op_remove(self, label):
        box_id = aoc_hash(label)
        remove_filter = lambda x: x[0] != label
        self.boxes[box_id] = list(filter(remove_filter, self.boxes[box_id]))

    def op_insert(self, label, focal_length):
        box_id = aoc_hash(label)
        for idx, lens in enumerate(self.boxes[box_id]):
            if lens[0] == label:
                self.boxes[box_id][idx] = (label, focal_length)
                return
        self.boxes[box_id].append((label, focal_length))

    def print(self):
        for id, box in enumerate(self.boxes):
            if len(box):
                print(f"  box {id}: {box}")

    def focusing_power(self):
        sum = 0
        for box_idx, box in enumerate(self.boxes):
            for lens_idx, lens in enumerate(box):
                lens_power = (box_idx + 1) * (lens_idx + 1) * lens[1]
                print(f"box {box_idx}, {lens}, power: {lens_power}")
                sum += lens_power
        return sum


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

## Part 2
hmap = aoc_hashmap()
for elem in input_line_elems:
    hmap.op_do(elem)
    hmap.print()
    print()

print(f"part2 focusing power: {hmap.focusing_power()}")
