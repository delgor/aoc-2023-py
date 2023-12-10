from pathlib import Path
from collections import namedtuple


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)


# Prepare vec(tor) / point type
vec = namedtuple("vec", "y x")


def vec_add(v1: vec, v2: vec) -> vec:
    return vec(v1.y + v2.y, v1.x + v2.x)


vec.__add__ = vec_add

# Prepare directions
possible_directions_by_symbol = {
    # straights
    "-": [vec(0, -1), vec(0, +1)],
    "|": [vec(-1, 0), vec(+1, 0)],
    # turns
    "7": [vec(0, -1), vec(+1, 0)],
    "J": [vec(0, -1), vec(-1, 0)],
    "L": [vec(-1, 0), vec(0, +1)],
    "F": [vec(+1, 0), vec(0, +1)],
    # special
    ".": [],
    "S": [vec(0, -1), vec(0, +1), vec(-1, 0), vec(+1, 0)],
}

# Transform to (y, x) grid, and find starting pos
start = None
grid = {}
for y in range(0, len(input)):
    grid[y] = list(input[y])
    for x in range(0, len(grid[y])):
        if grid[y][x] == "S":
            start = vec(y, x)

print(f"start at {start}")


def symbol_at(pos: vec) -> "str":
    if 0 <= pos.y < len(grid) and 0 <= pos.x < len(grid[0]):
        return grid[pos.y][pos.x]
    else:
        # Everything outside the grid is flat ground
        return "."


def possible_neighbors(pos: vec) -> [vec]:
    """Find possible neighbors of `pos`.
    This does not check if that neighbor has a backwards connection to pos."""
    symbol = symbol_at(pos)
    possible_directions = possible_directions_by_symbol[symbol]
    return [pos + direction for direction in possible_directions]


def actual_neighbors(pos: vec) -> [vec]:
    result = []
    for possible_neighbor in possible_neighbors(pos):
        if pos in possible_neighbors(possible_neighbor):
            result.append(possible_neighbor)
    return result


def are_positions_connected(p1: vec, p2: vec) -> bool:
    p1_possible_neighbors = possible_neighbors(p1)
    p2_possible_neighbors = possible_neighbors(p2)

    if p1 in p2_possible_neighbors and p2 in p1_possible_neighbors:
        return True
    return False


# Tests against example1_clean
if p == Path("input.example1_clean.txt"):
    assert are_positions_connected(vec(0, 0), vec(0, 1)) == False
    assert are_positions_connected(vec(1, 1), vec(2, 1)) == True
    assert are_positions_connected(vec(1, 1), vec(1, 2)) == True
    assert are_positions_connected(vec(1, 1), vec(1, 0)) == False
    assert are_positions_connected(vec(1, 1), vec(0, 1)) == False

## Part 1
# Calculate distances from start:
distance_grid = [[-1] * len(grid[0]) for _ in range(len(grid))]
prev_positions = []
check_positions = [start]
current_distance = 0
while len(check_positions) > 0:
    next_positions = []
    for check_position in check_positions:
        # Check if the check_position already as a distance set - that can only happen if we already visited that
        # position on another route (from the other direction of the loop)
        current_distance_of_target = distance_grid[check_position.y][check_position.x]
        if 0 < current_distance_of_target <= current_distance:
            # This will trigger on maximum distance, because that field will be the first to be visited two times
            # (once from each direction of the loop)
            print(
                f"Found a position for which there is a shorter route: {check_position} min {current_distance_of_target}"
            )
            break
        else:
            distance_grid[check_position.y][check_position.x] = current_distance

        # Any neighbor not previously visited needs to be checked next
        # Because we always check for actual neighbors (connection in both directions), starting from S,
        # we do not see trash connections outside the loop which have (one-sided) connections into the loop.
        # Lucky for us that there are no T pieces.
        for neighbor in actual_neighbors(check_position):
            if neighbor not in prev_positions:
                next_positions.append(neighbor)
    prev_positions = check_positions
    check_positions = next_positions
    current_distance += 1
