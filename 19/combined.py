from pathlib import Path
from collections import namedtuple, deque


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

mode = 0
workflows = {}
rejected = []
accepted = []
for line in input_lines:
    if not line:
        mode += 1

    elif mode == 0:
        # Load ruleset: px{a<2006:qkq,m>2090:A,rfg}
        chain, rules = line.split("{", 1)
        rules = rules[:-1]
        rules_arr = rules.split(",")
        workflow = []
        for rule_elem in rules_arr[:-1]:
            var = rule_elem[0]
            op = rule_elem[1]
            val, target = rule_elem[2:].split(":")
            # Add to struct
            rule = (var, op, int(val), target)
            workflow.append(rule)
        default_target = rules_arr[-1]
        workflow.append((None, None, None, default_target))
        workflows[chain] = workflow
        print(f"Workflow {chain} is: {workflow}")

    elif mode == 1:
        for var in "xmas":
            line = line.replace(var, f"'{var}'")
        line = line.replace("=", ":")
        elem = eval(line)
        print(elem)

        op_funcs = {
            "<": lambda val, comp: val < comp,
            ">": lambda val, comp: val > comp,
        }

        chain = "in"
        while chain not in ["R", "A"]:
            workflow = workflows[chain]
            print(f"  workflow {chain}: {workflow}")
            for var, op, val, target in workflow:
                if var == None or op == None or val == None:
                    chain = target
                    print(f"  -> {chain}")
                    break
                elif op_funcs[op](elem[var], val):
                    chain = target
                    print(f"  -> {chain}")
                    break

        if chain == "R":
            rejected.append(elem)
        elif chain == "A":
            accepted.append(elem)

accepted_rating_sum = 0
for elem in accepted:
    accepted_rating_sum += sum(elem.values())
print(f"part1 accepted rating sum: {accepted_rating_sum}")


# part2
# This was heavily inspired (or copied) from @jonathanpaulson
# see his solution at https://github.com/jonathanpaulson/AdventOfCode/blob/master/2023/19.py
def limit_range(op, val, bound_low, bound_high):
    # bounds are inclusive their limits, so we must account for non-equality via off-by-one on < & >
    if op == ">":
        bound_low = max(bound_low, val + 1)
    elif op == "<":
        bound_high = min(bound_high, val - 1)
    # These cases are generated when inverting the op
    elif op == ">=":
        bound_low = max(bound_low, val)
    elif op == "<=":
        bound_high = min(bound_high, val)
    return bound_low, bound_high


def new_ranges(var, op, val, x_bounds, m_bounds, a_bounds, s_bounds):
    x_low, x_high = x_bounds
    m_low, m_high = m_bounds
    a_low, a_high = a_bounds
    s_low, s_high = s_bounds
    if var == "x":
        x_low, x_high = limit_range(op, val, x_low, x_high)
    elif var == "m":
        m_low, m_high = limit_range(op, val, m_low, m_high)
    elif var == "a":
        a_low, a_high = limit_range(op, val, a_low, a_high)
    elif var == "s":
        s_low, s_high = limit_range(op, val, s_low, s_high)

    return (x_low, x_high), (m_low, m_high), (a_low, a_high), (s_low, s_high)


accepted_combinations = 0

check_list = deque([("in", (1, 4000), (1, 4000), (1, 4000), (1, 4000))])
while len(check_list):
    chain, (x_low, x_high), (m_low, m_high), (a_low, a_high), (s_low, s_high) = check_list.pop()
    if x_low >= x_high or m_low >= m_high or a_low >= a_high or s_low >= s_high:
        continue
    elif chain == "A":
        combinations = (x_high - x_low + 1) * (m_high - m_low + 1) * (a_high - a_low + 1) * (s_high - s_low + 1)
        accepted_combinations += combinations
        continue
    elif chain == "R":
        continue
    else:
        workflow = workflows[chain]
        for var, op, val, target in workflow:
            if op is None:
                check_list.append((target, (x_low, x_high), (m_low, m_high), (a_low, a_high), (s_low, s_high)))
            else:
                # Recurse into two variants:
                # 1. rule applies: range was limited, chain changed. enqueue this case
                check_list.append(
                    (
                        target,
                        *new_ranges(var, op, val, (x_low, x_high), (m_low, m_high), (a_low, a_high), (s_low, s_high)),
                    )
                )

                # 2. rule did not apply: stay in loop, invert range limiter
                op = "<=" if op == ">" else ">="
                (x_low, x_high), (m_low, m_high), (a_low, a_high), (s_low, s_high) = new_ranges(
                    var, op, val, (x_low, x_high), (m_low, m_high), (a_low, a_high), (s_low, s_high)
                )


print(f"combinations: {accepted_combinations}")
