from pathlib import Path
import re


p = Path("input.real.txt")
input = p.read_text().splitlines(keepends=False)

match_digits = re.compile(r"[0-9]")
sum = 0

for line in input:
    print(f"line: {line}")
    digits = match_digits.findall(line)
    print(f"digits: {digits}")

    line_number = digits[0] + digits[-1]
    print(f"line number: {line_number}")

    sum += int(line_number)

print(f"sum: {sum}")
