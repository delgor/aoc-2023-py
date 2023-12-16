from pathlib import Path
from collections import namedtuple


# Prepare vec(tor) / point type
vec = namedtuple("vec", "y x")


def vec_add(v1: vec, v2: vec) -> vec:
    return vec(v1.y + v2.y, v1.x + v2.x)


def vec_sub(v1: vec, v2: vec) -> vec:
    return vec(v1.y - v2.y, v1.x - v2.x)


def vec_rotate_cw(self: vec) -> vec:
    return vec(self.x, -self.y)


def vec_rotate_ccw(self: vec) -> vec:
    return vec(-self.x, self.y)


vec.__add__ = vec_add
vec.__sub__ = vec_sub
vec.rotate_cw = vec_rotate_cw
vec.rotate_ccw = vec_rotate_ccw


def print_pattern(grid):
    for row in grid:
        row_str = "".join(row)
        print(f"{row_str}")


energize_grid_split_check = []


def energize_grid(beam_start: vec, beam_dir: vec, grid, energy_grid):
    pos = beam_start
    print(f"Energize from {beam_start} moving {beam_dir}")
    while 0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[0]):
        # Energize current tile
        energy_grid[pos.y][pos.x] += 1
        print(f"Visited {pos}, going {beam_dir}")

        # Handle object
        obj = grid[pos.y][pos.x]

        if obj == ".":
            # Empty space, continue
            pos += beam_dir

        elif obj == "\\":
            if abs(beam_dir.y):
                beam_dir = beam_dir.rotate_ccw()
            elif abs(beam_dir.x):
                beam_dir = beam_dir.rotate_cw()
            print(f"Rotated at {pos}, new dir: {beam_dir}")
            pos += beam_dir

        elif obj == "/":
            if abs(beam_dir.y):
                beam_dir = beam_dir.rotate_cw()
            elif abs(beam_dir.x):
                beam_dir = beam_dir.rotate_ccw()
            print(f"Rotated at {pos}, new dir: {beam_dir}")
            pos += beam_dir

        elif obj == "-":
            # Same orientation, pass through
            if abs(beam_dir.y) == 0 and abs(beam_dir.x) == 1:
                print(f"Passing through - at {pos}")
                pos += beam_dir
            else:
                # Recurse into splits
                if pos in energize_grid_split_check:
                    print(f"Already split at {pos}, do not recurse again.")
                else:
                    energize_grid_split_check.append(pos)

                    new_dir_a = beam_dir.rotate_cw()
                    energize_grid(pos + new_dir_a, new_dir_a, grid, energy_grid)

                    new_dir_b = beam_dir.rotate_ccw()
                    energize_grid(pos + new_dir_b, new_dir_b, grid, energy_grid)
                break

        elif obj == "|":
            # Same orientation, pass through
            if abs(beam_dir.y) == 1 and abs(beam_dir.x) == 0:
                print(f"Passing through | at {pos}")
                pos += beam_dir
            else:
                # Recurse into splits
                if pos in energize_grid_split_check:
                    print(f"Already split at {pos}, do not recurse again.")
                else:
                    energize_grid_split_check.append(pos)

                    new_dir_a = beam_dir.rotate_cw()
                    energize_grid(pos + new_dir_a, new_dir_a, grid, energy_grid)

                    new_dir_b = beam_dir.rotate_ccw()
                    energize_grid(pos + new_dir_b, new_dir_b, grid, energy_grid)
                break
        else:
            raise RuntimeError("Unknown object")


def filter_energy_grid_energized(energy_grid):
    energized_grid = [["."] * len(energy_grid[0]) for row in energy_grid]
    energized_count = 0
    for row_idx in range(len(energy_grid)):
        for col_idx in range(len(energy_grid[0])):
            if energy_grid[row_idx][col_idx] >= 1:
                energized_grid[row_idx][col_idx] = "#"
                energized_count += 1
    return energized_grid, energized_count


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

grid = all_patterns[0]

## Part 1
print_pattern(grid)
print()

energy_grid = [[0] * len(grid[0]) for row in grid]
energize_grid(vec(0, 0), vec(0, 1), grid, energy_grid)

energized_grid, energized_count = filter_energy_grid_energized(energy_grid)
print_pattern(energized_grid)
print(f"Total of energized tiles: {energized_count}")
