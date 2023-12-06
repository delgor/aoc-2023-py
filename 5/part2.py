from pathlib import Path
from collections import namedtuple
from pprint import pprint

MapRange = namedtuple("Range", "destination source length")

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
        new_range = MapRange(destination=new_range[0], source=new_range[1], length=new_range[2])
        maps[from_]["ranges"].append(new_range)
    elif line == "" and from_ and to_:
        print(f"Loaded map: {from_} to {to_}: ")
        for range_ in maps[from_]["ranges"]:
            print(f"  range: {range_}")
        print()
        from_ = None
        to_ = None

pprint(maps)


def map_value(value, ranges: [MapRange]):
    # Check if any range applies
    for range_ in ranges:
        if range_.source <= value < range_.source + range_.length:
            return value - range_.source + range_.destination
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

def seed_iter(seeds):
    assert len(seeds) % 2 == 0
    i = 0
    while i < len(seeds):
        yield seeds[i], seeds[i + 1]
        i += 2

# This works, but bruteforce every seed is painfully slow. Rework this.
for seed_start, seed_cnt in seed_iter(seeds):
    print(f"got {seed_cnt} seeds starting at {seed_start}")
    for seed in range(seed_start, seed_start + seed_cnt):
        seeds_mapped = apply_maps(seed, "seed")
        #print(f"applied mapping: {seeds_mapped}")
        min_location = min(min_location, seeds_mapped["location"]) if min_location else seeds_mapped["location"]

print(f"min location: {min_location}")
