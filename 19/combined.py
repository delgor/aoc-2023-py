from pathlib import Path
from collections import namedtuple


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
