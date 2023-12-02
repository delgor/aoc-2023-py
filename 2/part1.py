from pathlib import Path
import re


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}

sum = 0

for line in input:
    print(f"line: {line}")
    # line example: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    game_id, drawings = line.split(": ", 1)
    game_id = int(game_id[5:])

    # Assume game is valid
    game_valid = True

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

        # check limits
        valid_drawing = True
        for color in limits.keys():
            if drawing_dict.get(color, 0) > limits[color]:
                valid_drawing = False
                print(f"drawing {drawing_dict} is invalid")
                break

        # Invalid drawing means game is invalid
        if not valid_drawing:
            game_valid = False

    if game_valid:
        sum += game_id

print(f"sum: {sum}")
