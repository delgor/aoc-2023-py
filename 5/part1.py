from pathlib import Path
from collections import namedtuple
from pprint import pprint

Range = namedtuple("Range", "destination source length")

p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)


def load_integer_list(input: str) -> [int]:
    # Discard empty elements, e.g. between multiple space when used for block indentation
    filter_func = lambda x: len(x) > 0

    numbers = list(map(int, filter(filter_func, input.split(" "))))
    return numbers


seeds = []
maps = {}
from_ = None
to_ = None

# Load input file
for line in input:
    # print(f"line: {line}")
    if "seeds: " in line:
        seeds = load_integer_list(line[7:])
        print(f"seeds: {seeds}")

    if "map:" in line:
        map_name, _ = line.split(" ", 1)
        from_, to_ = map_name.split("-to-")
        maps[from_] = {"target": to_, "ranges": []}
    elif line != "" and from_ and to_:
        new_range = load_integer_list(line)
        new_range = Range(destination=new_range[0], source=new_range[1], length=new_range[2])
        maps[from_]["ranges"].append(new_range)
    elif line == "" and from_ and to_:
        print(f"Loaded map: {from_} to {to_}: ")
        for range in maps[from_]["ranges"]:
            print(f"  range: {range}")
        print()
        from_ = None
        to_ = None

pprint(maps)


def map_value(value, ranges: [Range]):
    # Check if any range applies
    for range in ranges:
        if range.source <= value < range.source + range.length:
            return value - range.source + range.destination
    # If not, return value
    return value


def apply_maps(input_value, input_type):
    applied_mappings = {input_type: input_value}
    while input_type:
        if input_type in maps:
            input_value = map_value(input_value, maps[input_type]["ranges"])
            input_type = maps[input_type]["target"]
            applied_mappings[input_type] = input_value
        else:
            break
    return applied_mappings


min_location = None

for seed in seeds:
    seeds_mapped = apply_maps(seed, "seed")
    print(f"applied mapping: {seeds_mapped}")
    min_location = min(min_location, seeds_mapped["location"]) if min_location else seeds_mapped["location"]

print(f"min location: {min_location}")
