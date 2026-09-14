from automata import determinize, minimize

nfa = {
    'states': {'A', 'B', 'C'},
    'start': 'A',
    'accept': {'A', 'C'},
    'transition': {
        'A': {'0': {'B', 'C'}, '1': {'C'}},
        'B': {'0': {'A', 'B'}, '1': set()},
        'C': {'0': {'B'}, '1': {'A', 'B', 'C'}}
    }
}



result = determinize(nfa)
print("accept subset of states?", result['accept'].issubset(result['states']))
print("accept:", result['accept'])
print("states:", result['states'])


dfa = {
    'states': {'A', 'B', 'X'},
    'start': 'A',
    'accept': {'B', 'X'},   # X is unreachable from A
    'transition': {
        'A': {'0': 'B', '1': 'A'},
        'B': {'0': 'B', '1': 'B'},
        'X': {'0': 'X', '1': 'X'},
    }
}

result = minimize(dfa)
print("accept subset of states?", result['accept'].issubset(result['states']))
print("accept:", result['accept'])
print("states:", result['states'])