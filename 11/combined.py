from pathlib import Path
from collections import namedtuple


# Prepare point type
point = namedtuple("point", "y x")


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

# Load original grid
original_grid = []
for y in range(0, len(input)):
    original_grid.insert(y, list(input[y]))


# Expand grid
def grid_expand(orig_grid):
    new_grid = []
    new_y = 0
    # Expand in Y direction
    for orig_y in range(0, len(orig_grid)):
        # use list() to copy the row - otherwise we'll modify the original on X expansion
        new_grid.append(list(orig_grid[orig_y]))
        new_y += 1
        if input[orig_y].count("#") == 0:
            new_grid.append(list(orig_grid[orig_y]))  # again: copy using list()
            new_y += 1

    # Expand in X direction
    new_x = 0
    for orig_x in range(len(orig_grid[0])):
        # Check column
        column_empty = True
        for orig_y in range(len(orig_grid)):
            if orig_grid[orig_y][orig_x] == "#":
                column_empty = False
                break

        if column_empty:
            print(f"inserting new col for original col {orig_x} at {new_x}")
            for new_y in range(len(new_grid)):
                new_grid[new_y].insert(new_x, ".")
            new_x += 1

        new_x += 1

    return new_grid


def print_grid(grid):
    for line in grid:
        print("".join(line))


expanded_grid = grid_expand(original_grid)

print("Original:")
print_grid(original_grid)
print()

print("Expanded:")
print_grid(expanded_grid)


def find_galaxies(grid) -> list[point]:
    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                galaxies.append(point(y, x))
    return galaxies


all_galaxies = find_galaxies(expanded_grid)
print(f"found {len(all_galaxies)} galaxies")
# for galaxy in all_galaxies:
#    print(f"  galaxy at {galaxy}")


def find_all_pairs(input_list) -> [(point, point)]:
    pairs = []
    for left_idx in range(len(input_list)):
        for right_idx in range(left_idx + 1, len(input_list)):
            pair = (input_list[left_idx], input_list[right_idx])
            pairs.append(pair)
    return pairs


all_pairs = find_all_pairs(all_galaxies)
print(f"found {len(all_pairs)} galaxy pairs")
# for pair in all_pairs:
#    print(f"  pair {pair[0]} - {pair[1]}")

## Part 1
# sum of distances between each pair
sum = 0
for left, right in all_pairs:
    distance_x = abs(left.x - right.x)
    distance_y = abs(left.y - right.y)
    distance = distance_x + distance_y
    print(f"  {left} to {right}: {distance}")
    sum += distance

print(f"p1 sum: {sum}")
