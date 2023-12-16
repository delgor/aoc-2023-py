from pathlib import Path
from collections import namedtuple
from enum import Enum


Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])


def print_pattern(grid):
    for row in grid:
        row_str = "".join(row)
        print(f"'{row_str}'")


def tilt_grid(grid, dir: Direction):
    if dir == Direction.NORTH:
        start = 1
        end = len(grid)
    else:
        raise RuntimeError(f"Direction not implemented: {dir}")

    for row in range(start, end):
        for col in range(len(grid[0])):
            # Is round rock?
            if grid[row][col] == "O":
                # Check how far it can roll
                new_row = row
                for upwards in range(row - 1, -1, -1):
                    if grid[upwards][col] == ".":
                        new_row = upwards
                    else:
                        break
                grid[new_row][col], grid[row][col] = grid[row][col], grid[new_row][col]


def calculate_grid_load(grid, dir: Direction):
    if dir == Direction.NORTH:
        grid_weight = [len(grid) - x for x in range(len(grid))]
        start = 0
        end = len(grid)
    else:
        raise RuntimeError(f"Direction not implemented: {dir}")

    load = 0
    for row in range(start, end):
        for col in range(len(grid[0])):
            # Is round rock?
            if grid[row][col] == "O":
                load += grid_weight[row]

    return load


## Application
p = Path("input.real.txt")
file_lines = p.read_text().splitlines(keepends=False)

# Load grid(s)
all_patterns = []
current_pattern = []
for line in file_lines:
    if line:
        current_pattern.append(list(line))
    else:
        all_patterns.append(current_pattern)
        current_pattern = []

if len(current_pattern):
    all_patterns.append(current_pattern)

# Only one grid this day
grid = all_patterns[0]

print("Original pattern: ")
print_pattern(grid)
print()

tilt_grid(grid, Direction.NORTH)
print("Tilted pattern:")
print_pattern(grid)

load = calculate_grid_load(grid, Direction.NORTH)
print(f"load: {load}")
