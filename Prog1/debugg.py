import copy
from automata import minimize

# a small DFA, deliberately with an unreachable state and a mergeable pair,
# so both the trans_table.pop() and the merge-loop code paths get exercised
dfa = {
    'states': {'A', 'B', 'C', 'D', 'E'},
    'start': 'A',
    'accept': {'C'},
    'transition': {
        'A': {'0': 'B', '1': 'C'},
        'B': {'0': 'A', '1': 'C'},
        'C': {'0': 'D', '1': 'D'},
        'D': {'0': 'D', '1': 'D'},
        'E': {'0': 'E', '1': 'E'},  # unreachable from A
    }
}

# take a deep snapshot BEFORE calling minimize, so we have something
# untouched to compare against afterwards
before = copy.deepcopy(dfa)


result = minimize(dfa)

# now check: did calling minimize() change the ORIGINAL dfa object at all?
print("states unchanged?     ", dfa['states'] == before['states'])
print("accept unchanged?     ", dfa['accept'] == before['accept'])
print("transition unchanged? ", dfa['transition'] == before['transition'])

if dfa['transition'] != before['transition']:
    print("\ntransition BEFORE:", before['transition'])
    print("transition AFTER: ", dfa['transition'])