from pathlib import Path
import re


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

match_digits = re.compile(r"[0-9]+")
match_symbols = re.compile(r"[^0-9.]")
match_gear = re.compile(r"\*")
sum = 0

gears = {}

for line_no in range(0, len(input)):
    line = input[line_no]
    print(f"line: {line}")

    potential_part_no_iter = match_digits.finditer(line)
    for potential_part_no in potential_part_no_iter:
        num = int(potential_part_no.group(0))
        print(f"potential part no: {num} at {line_no}:{potential_part_no.start()}-{potential_part_no.end()}")
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

            print(f"  valid part number: {num}")
            sum += num

        for bbox_line_no in range(0, len(bounding_box)):
            for gear in match_gear.finditer(bounding_box[bbox_line_no]):
                gear_x = bounding_box_upper + bbox_line_no
                gear_y = bounding_box_left + gear.start()
                gear_pos = (gear_x, gear_y)
                if gear_pos not in gears:
                    gears[gear_pos] = [num]
                else:
                    gears[gear_pos].append(num)

                print(f"    found gear at {gear_pos}")

        print()

print(f"sum: {sum}")

gear_ratio_sum = 0

for gear_pos in gears:
    if len(gears[gear_pos]) != 2:
        print(f"gear at {gear_pos} invalid: has {len(gears[gear_pos])} adjacent parts")
    else:
        gear_ratio = gears[gear_pos][0] * gears[gear_pos][1]
        print(f"gear at {gear_pos} has ratio {gear_ratio}")
        gear_ratio_sum += gear_ratio

print(f"gear ratio sum: {gear_ratio_sum}")
