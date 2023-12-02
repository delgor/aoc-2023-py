from pathlib import Path
import re

p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

translation = {
    #    'zero': 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

match_digits = re.compile(f"[0-9]|{'|'.join(translation.keys())}")

# Remember: range(start, end) returns start <= x < end
for i in range(1, 10):
    translation[str(i)] = i

sum = 0

for line in input:
    print(f"line: {line}")

    # re.findall is insufficient for this case
    # we need overlapping matches, e.g. 'oneight' needs to be read as '18'
    digits = list()
    for i in range(0, len(line)):
        match = match_digits.match(line, i)
        if match:
            digits.append(match.group(0))

    line_number = translation[digits[0]] * 10 + translation[digits[-1]]
    print(f"line number: {line_number}")

    sum += int(line_number)

print(f"sum: {sum}")
