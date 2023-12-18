from pathlib import Path
from collections import namedtuple
from copy import deepcopy, copy
import sys
import heapq


sys.path.append(Path("../"))
from common.vec import *

p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

GRID = [[int(c) for c in row] for row in input_lines]
ROWS = len(GRID)
COLS = len(GRID[0])


visited_node = namedtuple("node", "pos dir dir_length")


def pos_in_grid(pos: vec):
    if 0 <= pos.y < ROWS and 0 <= pos.x < COLS:
        return True
    return False


def shortest_way_length(start: vec, dest: vec, grid):
    # pos, prev_dir, prev_dir_len, total_distance (so far), path
    current_nodes = [(0, start, None, 0, [])]
    shortest_distance = None
    loop = 0
    seen = {}
    while True:
        # No more nodes to check - abort
        if not current_nodes:
            break

        # Do not do this. heapq guarantees that the first element is the lowest,
        # and is way faster at this than sorting could ever be.
        #current_nodes.sort(key=lambda x: x[3], reverse=True)

        check_node = heapq.heappop(current_nodes)

        # Otherwise, check paths for all current nodes
        total_distance, pos, prev_dir, dir_length, path = check_node
        assert pos_in_grid(pos) == True  # nodes outside the grid should never be queued

        #print(f"  working at length {total_distance}, check_list {len(current_nodes)}")

        # Make sure we're not running circles.
        # If you were doing BFS, this would require a check on the distance.
        # Since we're using the heapqueue which ensures that shortest paths are visited first,
        # we can be sure that the first entry into seen actually is the shortest route.
        seen_key = (pos.y, pos.x, prev_dir, dir_length)
        if seen_key in seen:
            assert total_distance >= seen[seen_key]
            continue
        else:
            seen[seen_key] = total_distance

        # Do not search further if we're at destination. Just update distance
        if pos == dest:
            #print(f"  found path at length {total_distance}")
            if not shortest_distance:
                shortest_distance = total_distance
                shortest_path = path
            else:
                shortest_distance = min(shortest_distance, total_distance)
                shortest_path = path
            break

        # Search in all directions possible
        valid_directions = copy(DIRS_ALL)

        # Remove backwards
        if prev_dir != None:
            valid_directions.remove(prev_dir*-1)

        # Remove same direction after 3 tiles
        if dir_length == 3:
            valid_directions.remove(prev_dir)

        for next_dir in valid_directions:
            next_dir_length = 1
            if next_dir == prev_dir:
                next_dir_length = dir_length + 1
            next_pos = pos + next_dir

            # Do not leave the grid
            if not pos_in_grid(next_pos):
                continue

            next_distance = total_distance + grid[next_pos.y][next_pos.x]
            new_path = []
            new_path = copy(path)
            new_path.append(next_pos)
            new_next = (next_distance, next_pos, next_dir, next_dir_length, new_path)
            #print(f"  Check next: {new_next}")
            heapq.heappush(current_nodes, new_next)

    #for path_elem in shortest_path:
    #    print(f"  {path_elem}")
    #print(f"Shortest distance: {shortest_distance}")
    return shortest_distance

# 961 is too high
print(f"Grid of {ROWS-1}x{COLS-1}")
part1 = shortest_way_length(vec(0,0), vec(ROWS-1, COLS-1), GRID)
print(f"part1 shortest path: {part1}")