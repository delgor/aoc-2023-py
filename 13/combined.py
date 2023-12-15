from pathlib import Path
from collections import namedtuple


p = Path("input.real.txt")
file_lines = p.read_text().splitlines(keepends=False)


def print_pattern(grid):
    for row in grid:
        row_str = "".join(row)
        print(f"'{row_str}'")


def list_is_equal(a_list, b_list):
    for a, b in zip(a_list, b_list):
        if a != b:
            return False
    # print(f"Equal lists:")
    # print(f"  a: {a_list}")
    # print(f"  b: {a_list}")
    return True


def find_horizontal_mirror(grid, print=print):
    print(f"grid is {len(grid)} rows, {len(grid[0])} cols")
    # We need to start searching from the middle to find the biggest match
    mid_to_end = list(range(int(len(grid) / 2), len(grid)))
    mid_to_start = list(range(int(len(grid) / 2), 0, -1))
    mirror_search_rows = [None] * (len(mid_to_end) + len(mid_to_start))
    mirror_search_rows[::2] = mid_to_end
    mirror_search_rows[1::2] = mid_to_start
    # range(1, len(grid)-1)
    for mirror_row in mirror_search_rows:
        max_rows = min(mirror_row, len(grid) - mirror_row)
        print(f"Checking horizontal mirror at row {mirror_row}, maximum of {max_rows} to check.")
        is_mirror = True
        for offset in range(max_rows):
            if not list_is_equal(grid[mirror_row - offset - 1], grid[mirror_row + offset]):
                is_mirror = False
                break

        if is_mirror:
            return mirror_row
    return False


def find_vertical_mirror(grid):
    print(f"grid is {len(grid)} rows, {len(grid[0])} cols")
    for mirror_col in range(1, len(grid[0])):
        max_cols = min(mirror_col, len(grid[0]) - mirror_col)
        print(f"Checking vertical mirror at col {mirror_col}, maximum of {max_cols} cols to check")
        is_mirror = True
        for offset in range(max_cols):
            print(f"  checking at offset {offset}")
            left = [row[mirror_col - offset - 1] for row in grid]
            right = [row[mirror_col + offset] for row in grid]
            print(f"    left : {left}")
            print(f"    right: {right}")
            if not list_is_equal(left, right):
                is_mirror = False
                break

        if is_mirror:
            return mirror_col
    return False


# Load patterns
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


## Part 1
sum = 0
for idx, pattern in enumerate(all_patterns):
    print(f"Pattern {idx}")
    print_pattern(pattern)

    vertical = find_vertical_mirror(pattern)
    horizontal = find_horizontal_mirror(pattern)
    if vertical:
        print(f"Found vertical: {vertical}")
        sum += vertical
    if horizontal:
        print(f"Found horizontal: {horizontal}")
        sum += 100 * horizontal
    print()

    if not vertical and not horizontal:
        input("Found no mirrors. Please check.")

print(f"p1 sum: {sum}")
