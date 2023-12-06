from pathlib import Path
from collections import namedtuple
from pprint import pprint

MapRange = namedtuple("MapRange", "destination source length")
InRange = namedtuple("InRange", "start length")


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
        yield InRange(start=seeds[i], length=seeds[i + 1])
        i += 2


def map_range(in_range: InRange, map_ranges: [MapRange]) -> [InRange]:
    # If we need to split a InRange, we still need to map other partial ranges. ranges_to_map contains the list of
    # remaining splits/ranges to map.
    ranges_to_map = [in_range]
    ranges_out = []
    while len(ranges_to_map) > 0:
        in_range = ranges_to_map.pop()

        # Match range against all map ranges, and register when we find a match
        found_match = False
        for map_range in map_ranges:
            # Fully contained in map range
            if (
                in_range.start >= map_range.source
                and in_range.start + in_range.length <= map_range.source + map_range.length
            ):
                new_range_start = in_range.start - map_range.source + map_range.destination
                ranges_out.append(InRange(start=new_range_start, length=in_range.length))
                found_match = True
            # Beginning of in_range in map_range, but end outside, because length
            elif (
                map_range.source <= in_range.start < map_range.source + map_range.length
                and in_range.start + in_range.length > map_range.source + map_range.length
            ):
                # Calculate last element of in_range in map_range for splitting
                map_range_source_end = map_range.source + map_range.length
                overlap_length = map_range_source_end - in_range.start
                inner_range = InRange(
                    start=in_range.start - map_range.source + map_range.destination, length=overlap_length
                )
                ranges_out.append(inner_range)

                # Reinsert remaining range into stack for further mapping
                remaining_range = InRange(start=map_range_source_end, length=in_range.length - overlap_length)
                ranges_to_map.append(remaining_range)
                found_match = True
            # Beginning of in_range out of map_range, but end (-1!) inside
            elif (
                in_range.start < map_range.source
                and map_range.source <= (in_range.start + in_range.length - 1) < map_range.source + map_range.length
            ):
                overlap_length = in_range.start + in_range.length - map_range.source
                assert overlap_length != 0
                overlap_range = InRange(start=map_range.destination, length=overlap_length)
                ranges_out.append(overlap_range)

                remaining_range = InRange(start=in_range.start, length=in_range.length - overlap_length)
                ranges_to_map.append(remaining_range)

                found_match = True

            if found_match:
                # No need to check other MapRanges
                break

        # found no match in any of map ranges, use direct mapping
        if not found_match:
            ranges_out.append(in_range)

    return ranges_out


def apply_maps_ranges(in_ranges: [InRange], input_type: str) -> [InRange]:
    """Run input ranges of input_type through all remaining mappings"""
    out_ranges = []
    while input_type:
        if input_type in maps:
            # fetch mappings for current round
            next_type = maps[input_type]["target"]
            map_ranges = maps[input_type]["ranges"]
            out_ranges = []

            print(f"Running mappings for {input_type} -> {next_type}")

            # apply to all ranges
            for in_range in in_ranges:
                print(f"..mapping {in_range}")
                mapped = map_range(in_range, map_ranges)
                sum_mapped_length = 0
                for _ in mapped:
                    print(f"....to {_}")
                    sum_mapped_length += _.length
                assert in_range.length == sum_mapped_length
                out_ranges.extend(mapped)

            # prepare for next mapping round
            in_ranges = out_ranges
            input_type = next_type
        else:
            break
    return out_ranges


# Crunch data
in_ranges = list(seed_iter(seeds))
location_ranges = apply_maps_ranges(in_ranges, "seed")

# Find minimum from result set
for loc_range in location_ranges:
    # print(f"  loc_range: {loc_range}")
    if min_location is None or loc_range.start < min_location:
        min_location = loc_range.start

print(f"min location: {min_location}")
