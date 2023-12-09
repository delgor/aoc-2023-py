from pathlib import Path
from collections import namedtuple
from pprint import pprint
from enum import IntEnum


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)


def row_all_zero(row):
    for elem in row:
        if elem != 0:
            return False
    return True


sum_p1 = 0

for line in input:
    print(line)
    depth = 0
    rows = {depth: list(map(int, line.split(" ")))}

    # Calculate differences
    while not row_all_zero(rows[depth]):
        rows[depth + 1] = list()
        for idx in range(0, len(rows[depth]) - 1):
            diff = rows[depth][idx + 1] - rows[depth][idx]
            rows[depth + 1].append(diff)

        depth += 1

    # p1: extrapolate forward
    while depth > 0:
        next_elem = rows[depth - 1][-1] + rows[depth][-1]
        rows[depth - 1].append(next_elem)
        depth -= 1

    for row in rows.values():
        print(row)

    sum_p1 += rows[0][-1]

print(f"sum_p1: {sum_p1}")
