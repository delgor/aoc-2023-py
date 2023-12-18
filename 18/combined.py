from pathlib import Path
from collections import namedtuple


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

grid = [["#"]]


def resize_grid(rows, cols, dy, dx):
    global grid
    new_grid = [["."]*cols for row in range(rows)]

    for row_idx, row in enumerate(grid):
        for col_idx, col in enumerate(row):
            new_grid[row_idx+dy][col_idx+dx] = col

    grid = new_grid


def print_grid():
    global grid
    for row in grid:
        print("".join(row))


def count_hole():
    global grid
    sum = 0
    for row in grid:
        sum += row.count("#")
    return sum


def floodfill(y, x, old_symbol, new_symbol):
    global grid
    queue = [(y, x)]
    while len(queue) > 0:
        y, x = queue.pop()
        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            if grid[y][x] == old_symbol:
                grid[y][x] = new_symbol

                queue.append((y, x-1))
                queue.append((y, x+1))
                queue.append((y-1, x))
                queue.append((y+1, x))


y = 0
x = 0
part2 = False
for line in input_lines:
    direction, distance, color = line.split(" ")
    distance = int(distance)

    if part2:
        distance = int(color[2:7], 16)
        direction = {0: "R", 1: "D", 2: "L", 3: "U"}[int(color[7])]


    if direction == "R":
        sx = 1
        sy = 1
        nx = x + distance
        ny = y
    elif direction == "L":
        sx = -1
        sy = 1
        nx = x - distance
        ny = y
    elif direction == "U":
        sx = 1
        sy = -1
        nx = x
        ny = y - distance
    elif direction == "D":
        sx = 1
        sy = 1
        nx = x
        ny = y + distance

    rows = len(grid)
    cols = len(grid[0])

    print(f"move from ({y}, {x}) dir {direction} dist {distance} to ({nx}, {ny})")

    # Calculate offset if we move left out of the grid
    dx = 0
    dy = 0
    if nx < 0:
        dx = -nx
    if ny < 0:
        dy = -ny

    # Apply offsets
    if dx:
        nx += dx
        x += dx
    if dy:
        ny += dy
        y += dy

    resize_grid(max(rows+dy, ny+dy+1), max(cols+dx, nx+dx+1), dy, dx)

    for y in range(y, ny+sy, sy):
        for x in range(x, nx+sx, sx):
            grid[y][x] = "#"
    #print_grid()
    #print()

    x, y = nx, ny

    if not line:
        continue

# Dirty hack for floodfill. There has to be a border on the topmost row. And below that, is inside.
for col_idx, col in enumerate(grid[0]):
    if col == "#":
        floodfill(1, col_idx, ".", "#")
print_grid()

print(f"holes: {count_hole()}")
