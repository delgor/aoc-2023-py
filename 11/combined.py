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


def row_empty(grid, row):
    for elem in grid[row]:
        if elem == "#":
            return False
    return True


def col_empty(grid, col):
    for idx in range(len(grid[0])):
        if grid[idx][col] == "#":
            return False
    return True


# Expand grid
def grid_expanded_costs(orig_grid, cost=2):
    cost_grid = [[1] * len(orig_grid[0]) for _ in range(len(orig_grid))]

    # Expand in Y direction
    for orig_y in range(0, len(orig_grid)):
        if row_empty(orig_grid, orig_y):
            for orig_x in range(len(orig_grid[orig_y])):
                cost_grid[orig_y][orig_x] = cost

    # Expand in X direction
    for orig_x in range(0, len(orig_grid[0])):
        if col_empty(orig_grid, orig_x):
            for orig_y in range(len(orig_grid)):
                cost_grid[orig_y][orig_x] = cost

    return cost_grid


def print_grid(grid):
    for line in grid:
        print("".join(line))


print("Grid:")
print_grid(original_grid)
print()


def find_galaxies(grid) -> list[point]:
    galaxies = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "#":
                galaxies.append(point(y, x))
    return galaxies


all_galaxies = find_galaxies(original_grid)
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


def distance(left: point, right: point, cost_grid) -> int:
    current_point = point(*left)
    dir_x = right.x - left.x
    if dir_x != 0:
        dir_x = int(dir_x / abs(dir_x))
    dir_y = right.y - left.y
    if dir_y != 0:
        dir_y = int(dir_y / abs(dir_y))
    current_distance = 0

    while current_point != right:
        # We can still choose which direction to go first
        cost_move_x = 1
        if 0 <= current_point.x + dir_x < len(cost_grid[0]):
            cost_move_x = cost_grid[current_point.y][current_point.x + dir_x]
        cost_move_y = 1
        if 0 <= current_point.y + dir_y < len(cost_grid):
            cost_move_y = cost_grid[current_point.y + dir_y][current_point.x]
        if current_point.x != right.x and current_point.y != right.y:
            if cost_move_y <= cost_move_x:
                # Move in Y direction
                current_distance += cost_move_y
                current_point = point(current_point.y + dir_y, current_point.x)
            else:
                current_distance += cost_move_x
                current_point = point(current_point.y, current_point.x + dir_x)

        elif current_point.x != right.x:
            current_distance += cost_move_x
            current_point = point(current_point.y, current_point.x + dir_x)
        elif current_point.y != right.y:
            current_distance += cost_move_y
            current_point = point(current_point.y + dir_y, current_point.x)
        else:
            print(f"Something bad is happening")

    # current_distance -= 1  # Last hop is always the target galaxy, with a guaranteed cost of 1

    return current_distance


## Part 1
# sum of distances between each pair
sum = 0
cost_grid_p1 = grid_expanded_costs(original_grid, 2)
for left, right in all_pairs:
    dist = distance(left, right, cost_grid_p1)
    print(f"  {left} to {right}: {dist}")
    sum += dist

print(f"p1 sum: {sum}")


## Part 2
# sum of distances between each pair with much bigger expansion
sum = 0
cost_grid_p1 = grid_expanded_costs(original_grid, 1000000)
for left, right in all_pairs:
    dist = distance(left, right, cost_grid_p1)
    print(f"  {left} to {right}: {dist}")
    sum += dist

print(f"p1 sum: {sum}")
