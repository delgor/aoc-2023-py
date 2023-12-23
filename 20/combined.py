import math
from pathlib import Path
from collections import namedtuple, deque


global_pulse_low_counter = 0
global_pulse_high_counter = 0


class BasicModule:
    def __init__(self):
        self.known_inputs = []
        self.low_pulse_counter = 0
        self.high_pulse_counter = 0

    def reset(self):
        self.low_pulse_counter = 0
        self.high_pulse_counter = 0

    def handle_pulse(self, input, pulse):
        global global_pulse_low_counter
        global global_pulse_high_counter
        if pulse == False:
            global_pulse_low_counter += 1
            self.low_pulse_counter += 1
        elif pulse == True:
            global_pulse_high_counter += 1
            self.high_pulse_counter += 1
        return None


class FlipFlopModule(BasicModule):
    def __init__(self):
        super().__init__()
        self.flipflop_state = False

    def reset(self):
        super().reset()
        self.flipflop_state = False

    def handle_pulse(self, input, pulse):
        super().handle_pulse(input, pulse)
        if pulse:
            return None
        elif not pulse:
            self.flipflop_state = not self.flipflop_state
            return self.flipflop_state


class ConjunctionModule(BasicModule):
    def __init__(self):
        super().__init__()
        self.previous_inputs = dict()

    def reset(self):
        super().reset()
        self.previous_inputs.clear()

    def handle_pulse(self, input, pulse):
        super().handle_pulse(input, pulse)
        self.previous_inputs[input] = pulse
        # Inverted versus description
        # Send True (high) if any previous input is False (low)
        for check_input in self.known_inputs:
            if not self.previous_inputs.get(check_input, False):
                return True
        # Otherwise send False (low)
        return False


class BroadcastModule(BasicModule):
    def __init__(self):
        super().__init__()

    def handle_pulse(self, input, pulse):
        super().handle_pulse(input, pulse)
        return pulse


p = Path("input.real.txt")
input_lines = p.read_text().splitlines(keepends=False)

all_modules = {}
# all_modules["output"] = (BasicModule(), [])

for line in input_lines:
    if line:
        module_name, outputs = line.split(" -> ")
        outputs = outputs.split(", ")
        if module_name[0] == "%":
            module_name = module_name[1:]
            module = FlipFlopModule()
        elif module_name[0] == "&":
            module_name = module_name[1:]
            module = ConjunctionModule()
        elif module_name == "broadcaster":
            module = BroadcastModule()
        else:
            module = BasicModule()
        all_modules[module_name] = (module, outputs)

# Find unknown output/debug modules and add them
missing_modules = []
for module_name in all_modules:
    outputs = all_modules[module_name][1]
    for output in outputs:
        if output not in all_modules:
            print(f"Found unknown module: {output}")
            missing_modules.append(output)

rx_module = BasicModule()

for module_name in missing_modules:
    if module_name == "rx":
        all_modules[module_name] = (rx_module, [])
    else:
        all_modules[module_name] = (BasicModule(), [])

# Mark known inputs
for module_name in all_modules:
    outputs = all_modules[module_name][1]
    for output in outputs:
        if output not in all_modules:
            print(f"Found unknown module: {output}")
            all_modules[output] = (BasicModule(), [])
        all_modules[output][0].known_inputs.append(module_name)

lowhigh = {False: "-low-", True: "-high-"}


def reset_all():
    for module, outputs in all_modules.values():
        module.reset()


def click_button():
    queue = deque()
    queue.append(("button", "broadcaster", False))
    while queue:
        source, module_name, pulse = queue.popleft()
        module, outputs = all_modules[module_name]
        out = module.handle_pulse(source, pulse)
        if out is not None:
            for output in outputs:
                queue.append((module_name, output, out))

        # Debug output
        # print(f"{source} {lowhigh[pulse]}> {module_name}")
    # print()


# Part 1: click 1000x
global_pulse_low_counter = 0
global_pulse_high_counter = 0
reset_all()
for _ in range(1000):
    click_button()
print(f"low*high: {global_pulse_low_counter * global_pulse_high_counter}")

# Part 2: how many clicks to rx low pulse == 1?
global_pulse_low_counter = 0
global_pulse_high_counter = 0
ctr = 0
reset_all()

# rx depends on !ft
# ft depends on NAND(vz, bq, qh, lt)
# so, we need to find the cycles on all of these.
# their LCM will be the first time ft and thus rx trigger.
search_cycles = {
    "vz": [None, 0],
    "bq": [None, 0],
    "qh": [None, 0],
    "lt": [None, 0],
}

# Run enough iterations to find all cycles
for _ in range(100000):
    ctr += 1
    click_button()

    for cycle_module in search_cycles.keys():
        if all_modules[cycle_module][0].low_pulse_counter:
            # print(f"{cycle_module} low on {ctr}")
            if search_cycles[cycle_module][0] == None:
                search_cycles[cycle_module][0] = ctr
                search_cycles[cycle_module][1] = 1
            elif search_cycles[cycle_module][1] < 2:
                search_cycles[cycle_module][1] += 1
                if search_cycles[cycle_module][0] * search_cycles[cycle_module][1] == ctr:
                    print(f"Cycle confirmed: {cycle_module} at {search_cycles[cycle_module][0]}")
                else:
                    print(f"Cycle error {cycle_module}")
            all_modules[cycle_module][0].low_pulse_counter = 0
            # search_cycles.remove(cycle_module)
    # print(f"round {ctr}: {rx_module.low_pulse_counter} low, {rx_module.high_pulse_counter} high")

min_clicks = math.lcm(*[cycle[0] for cycle in search_cycles.values()])
print(f"min clicks: {min_clicks}")
