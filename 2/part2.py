from pathlib import Path
import re


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

sum = 0

for line in input:
    print(f"line: {line}")
    # line example: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    game_id, drawings = line.split(": ", 1)
    game_id = int(game_id[5:])

    game_min_counts = {}

    # parse each drawing from the game
    for drawing_str in drawings.split("; "):
        colorpairs = drawing_str.split(", ")
        print(f"{game_id}: {colorpairs}")

        # parse counts from single drawing
        drawing_dict = {}
        for pair in colorpairs:
            pair = pair.split(" ")
            assert len(pair) == 2
            drawing_dict[pair[1]] = int(pair[0])

        # calculate minimum
        for color in drawing_dict.keys():
            game_min_counts[color] = max(
                game_min_counts.get(color, 0), drawing_dict.get(color, 0)
            )

    game_power = 1
    for color_count in game_min_counts.values():
        game_power *= color_count

    print(f"game {game_id}: minimum {game_min_counts} -> power {game_power}")

    sum += game_power

print(f"sum: {sum}")
