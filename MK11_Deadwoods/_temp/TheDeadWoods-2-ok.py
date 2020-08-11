import itertools

"""
The drum wheel is split into three parts: Head, Torso, Legs aka H, T, L with respective indices 0, 1, 2

"""

DRUM_WHEEL_CONTENTS  = (
    'SRH', # 0 Head : Skeleton, Robot, Human
    'HRS', # 1 Torso: Human, Robot, Skeleton
    'SRH') # 2 Leg  : Skeleton, Robot, Human
"""The contents of each of the drum wheel parts"""

BUTTONS = { 'A': 0, 'B': 1, 'C': 2}
"""The button names to their index. The index is used with the buttons data"""

BUTTONS_DATA = (
    # Head  Torso  Leg
     (-1,   +1,    -1),   # Input button A
     (+1,   -1,     0),   # Input button B
     (0,    -1,    +1))   # Input button C
"""The buttons and how they affect the drum wheel rotations"""


TEST_DATA = (
    # State, Button, New state
     ('SRH', 'B', 'RHH'), 
     ('RHH', 'C', 'RSS'), 
     ('RSS', 'C', 'RRR'),
     ('HRR', 'B', 'SHR') )
"""Test data with initial state, button and final state"""


def is_final(data):
    return data[0] == data[1] and data[1] == data[2]


def compute_graph():
    seq = itertools.product('SHR', repeat=3)
    graph = {}
    for i, p in enumerate(seq):
        if is_final(p): continue
        state = p[0] + p[1] + p[2]
        for button in BUTTONS.keys():
            graph[(state, button)] = advance_state(state, button)

    return graph


def graph_to_dot(graph, outfile):
    with open(outfile, 'w') as f:
        f.write('digraph DeadWoods {\n')
        # Give final state a distinctive color
        for data in DRUM_WHEEL_CONTENTS[0]:
            f.write("    %s[color=red];\n" % (data * 3))
        f.write("\n")
        for (state, input), new_state in graph.items():
            extra = ['label=%s' % input]
            if is_final(new_state):
                extra.append('color=blue')
            f.write("    %s -> %s [%s];\n" % (state, new_state, ','.join(extra)))
        f.write('}')


def advance_state(state, button):
    """Advances the state of the drum wheel parts given an input button"""

    # Copy the state to a list (for mutability)
    new_state = [s for s in state]
    for i, button_data in enumerate(BUTTONS_DATA[BUTTONS[button]]):
        # Get the current state's index in the current drum part
        drum_part = DRUM_WHEEL_CONTENTS[i]
        data_index = drum_part.find(state[i])
        # Advance / rotate
        new_state[i] = drum_part[(data_index + button_data) % len(drum_part)]
    return ''.join(new_state)


def test_advance_state():
    for (state, button, verif) in TEST_DATA:
        new_state = advance_state(state, button)
        print("%s + %s -> %s -> %s" % (state, button, new_state, "PASSED" if new_state == verif else "ERROR"))


def find_path(graph, state, end_state, route = [], visited=set(), routes=[]):
    for button in BUTTONS.keys():
        new_state = graph.get((state, button), None)
        if new_state is None or (new_state in visited):
            return

        new_route = list(route)
        new_route.append('%s + %s' % (state, button))

        new_visited = set(visited)
        new_visited.add(new_state)

        if new_state == end_state:
            routes.append(new_route)
            return

        if is_final(new_state):
            return

        find_path(graph, new_state, end_state, new_route, new_visited, routes)


#test_advance_state()
#dump_states()
graph = compute_graph()
#graph_to_dot(graph, r'C:\Users\eliasb\Projects\github\GraphViz\dot2pic\dw.dot')
routes = []
find_path(graph, 'HHH', 'SSS', routes=routes)
if routes:
    routes.sort(key=lambda x: len(x))
    for i, route in enumerate(routes):
        if i > 10: break
        print("Sol #%-2d with path len %-3d: %s" % (i, len(route), ', '.join(route)))