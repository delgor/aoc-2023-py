from pathlib import Path
from collections import namedtuple
from enum import Enum
from copy import deepcopy


Direction = Enum("Direction", ["NORTH", "EAST", "SOUTH", "WEST"])


def print_pattern(grid):
    for row in grid:
        row_str = "".join(row)
        print(f"{row_str}")


def tilt_grid_northsouth(grid, dir: Direction):
    if dir == Direction.NORTH:
        start = 0
        end = len(grid)
        step = 1
    elif dir == Direction.SOUTH:
        start = len(grid) - 1
        end = -1
        step = -1
    else:
        raise RuntimeError(f"Direction not implemented: {dir}")

    for row in range(start + step, end, step):
        for col in range(len(grid[0])):
            # Is round rock?
            if grid[row][col] == "O":
                # Check how far it can roll
                new_row = row
                for check_row in range(row - step, start - step, -step):
                    if grid[check_row][col] == ".":
                        new_row = check_row
                    else:
                        break
                grid[new_row][col], grid[row][col] = grid[row][col], grid[new_row][col]


def tilt_grid_eastwest(grid, dir: Direction):
    if dir == Direction.WEST:
        start = 0
        end = len(grid[0])
        step = 1
    elif dir == Direction.EAST:
        start = len(grid[0]) - 1
        end = -1
        step = -1
    else:
        raise RuntimeError(f"Direction not implemented: {dir}")

    for row in range(len(grid)):
        for col in range(start + step, end, step):
            # Is round rock?
            if grid[row][col] == "O":
                # Check how far it can roll
                new_col = col
                for check_col in range(col - step, start - step, -step):
                    if grid[row][check_col] == ".":
                        new_col = check_col
                    else:
                        break
                grid[row][col], grid[row][new_col] = grid[row][new_col], grid[row][col]


def tilt_grid(grid, dir: Direction):
    if dir == Direction.NORTH or dir == Direction.SOUTH:
        tilt_grid_northsouth(grid, dir)
    elif dir == Direction.EAST or dir == Direction.WEST:
        tilt_grid_eastwest(grid, dir)
    else:
        raise RuntimeError("Unknown direction")


def spin_grid(grid):
    tilt_grid(grid, Direction.NORTH)
    tilt_grid(grid, Direction.WEST)
    tilt_grid(grid, Direction.SOUTH)
    tilt_grid(grid, Direction.EAST)


def hash_grid(grid):
    str_rows = ["".join(row) for row in grid]
    str_repr = "".join(str_rows)
    return hash(str_repr)


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
original_grid = all_patterns[0]

print("Original pattern: ")
print_pattern(original_grid)
print()

## Part 1
grid = deepcopy(original_grid)
tilt_grid(grid, Direction.NORTH)
print("Tilted pattern:")
print_pattern(grid)

load = calculate_grid_load(grid, Direction.NORTH)
print(f"load: {load}")
print()

## Part 2
print("part 2")
grid = deepcopy(original_grid)
seen_hashes = {}
cycle_grids = {}
target_cycle = 1000000000
first_in_cycle = None
for spin in range(target_cycle):
    spin_grid(grid)
    # print(f"after {spin+1} spins")
    # print_pattern(grid)
    # print()
    grid_hash = hash_grid(grid)
    if grid_hash not in seen_hashes:
        seen_hashes[grid_hash] = spin
        cycle_grids[spin] = deepcopy(grid)
        print(f"spin {spin} - hash {grid_hash}")
    else:
        if not first_in_cycle:
            first_in_cycle = seen_hashes[grid_hash]
            cycle_len = spin - first_in_cycle
        print(f"Got repeat on spin {spin}, previously seen on {seen_hashes[grid_hash]}, hash {grid_hash}")
        break

target_grid_idx = (target_cycle - first_in_cycle) % cycle_len + first_in_cycle - 1
grid = cycle_grids[target_grid_idx]
grid_hash = hash_grid(grid)
print(f"Target {target_cycle} hash {grid_hash}")


print(f"load: {calculate_grid_load(grid, Direction.NORTH)}")
