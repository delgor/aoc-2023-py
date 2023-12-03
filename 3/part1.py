from pathlib import Path
import re


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

match_digits = re.compile(r"[0-9]+")
match_symbols = re.compile(r"[^0-9.]")
sum = 0

for line_no in range(0, len(input)):
    line = input[line_no]
    print(f"line: {line}")

    potential_part_no_iter = match_digits.finditer(line)
    for potential_part_no in potential_part_no_iter:
        print(
            f"potential part no: {potential_part_no.group(0)} at {line_no}:{potential_part_no.start()}-{potential_part_no.end()}"
        )
        bounding_box_upper = max(0, line_no - 1)
        bounding_box_lower = min(line_no + 1, len(input))
        bounding_box_left = max(0, potential_part_no.start() - 1)
        bounding_box_right = min(potential_part_no.end(), len(line))

        print(
            f"  bounding box from lines {bounding_box_upper}-{bounding_box_lower} cols {bounding_box_left}-{bounding_box_right}"
        )

        bounding_box = [
            # +1 because of start <= x < end semantics
            _[bounding_box_left : bounding_box_right + 1]
            for _ in input[bounding_box_upper : bounding_box_lower + 1]
        ]

        print(f"  bounding box: ")
        for bbox_line in bounding_box:
            print(f"    {bbox_line}")

        flattened_box = "".join(bounding_box)
        found_symbol = match_symbols.search(flattened_box)
        if found_symbol:
            # has symbol, so it is a valid part number
            num = int(potential_part_no.group(0))
            print(f"  valid part number: {num}")
            sum += num

        print()

print(f"sum: {sum}")
