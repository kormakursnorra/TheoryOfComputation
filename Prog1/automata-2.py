# A template file for your solution. 
# You are not allowed to use python libraries.
# Make sure to give good comments that explain your solution.

# You must define: 
# a function called determinize that receives an NFA as input and returns an equivalent DFA, i.e. it determinizes the input NFA; and 
# a function called minimize that receives a DFA as input and returns an equivalent smallest DFA, i.e. one that has as few states as possible.
# We assume that the NFAs have no epsilon transitions.


# You can use maps to encode DFAs and NFAs.
# Here is an example DFA:
# dfa = {
#   'states': {'A','B','C'},
#   'start': 'A',
#   'accept': {'C'},
#   'transition': {
#     'A': {'0': 'B', '1': 'C'},
#     'B': {'0': 'A', '1': 'C'},
#     'C': {'0': 'B', '1': 'A'}
#   }
# }

# Here is an example NFA:
# nfa = {
#   'states': {'A','B','C'},
#   'start': 'A',
#   'accept': {'A','C'},
#   'transition': {
#     'A': {'0': {'B','C'}, '1': {'C'}},
#     'B': {'0': {'A','B'}, '1': set()},
#     'C': {'0': {'B'}, '1': {'A','B','C'}}
#   }
# }

symbols = ['0','1']

## the following are the required functions:

def determinize( nfa: dict ):
    """This function takes as input an NFA and returns a DFA that accepts the same language.
    
    Args:
        nfa ( dict[str, Any] ): A dictionary representation of an NFA 

    Returns:
        dict[str, Any]: An equivalent DFA to the input NFA
    """

    if not nfa:
        return

 
    states_prime = set() # initialize DFA states
    delta_prime = set()  # initialize DFA transitions
    final_prime = set()  # initialize DFA accept
    states_Q = []  # initialize "queue" to hold the states


    # retrieve the nfas transition table, start, accept and states
    trans_table = nfa.get('transition')
    start_state = frozenset({nfa.get('start')})
    final_state = frozenset({nfa.get('accept')})
    states = nfa.get('states')

    # build dfa
    dfa = {'states': {}, 'start': start_state, 'accept': {}, 'transition': {} }

    # add start state
    states_prime.add(start_state)
    states_Q.append(start_state)

    while( len( states_Q ) != 0 ):

        # retrieve first state/s, if already visited continue
        states = states_Q.pop( 0 )

        for symbol in symbols:
            next_states = set()
            # iterate current states and their next states for input symbol
            for state in states:
                next_states = trans_table.get( state ).get( symbol )

                if not states_prime.isdisjoint( next_states ):
                    trans = { symbol: next_states }
                    delta_prime.update( trans )

                else:
                    states_Q.append( next_states )
                    states_prime.update( next_states )

        if states in final_state:
            final_prime.update( state )

    dfa['states'] = states_prime
    dfa['accept'] = final_prime
    dfa['transition'] = delta_prime
    return dfa

def minimize(dfa):
    """This function takes as input a DFA and returns a DFA that accepts the same language
    and has the fewest possible states.

    Args:
        dfa ( dict[str, Any] ): A dictionary representation of a DFA

    Returns:
        dict[str, Any]: A dictionary representation of a DFA with fewer possible states
    """

    return True 


def main():
    dfa = {
        'states': {'A','B','C'},
        'start': 'A',
        'accept': {'C'},
        'transition': {
            'A': {'0': 'B', '1': 'C'},
            'B': {'0': 'A', '1': 'C'},
            'C': {'0': 'B', '1': 'A'}
        }
    }
    nfa = {
        'states': {'A','B','C'},
        'start': 'A',
        'accept': {'A','C'},
        'transition': {
            'A': {'0': {'B','C'}, '1': {'C'}},
            'B': {'0': {'A','B'}, '1': set()},
            'C': {'0': {'B'}, '1': {'A','B','C'}}
        }
    }

    det_dfa = determinize(nfa)
    min_dfa = minimize(dfa)

    print(det_dfa)

if __name__ == "__main__":
    main()

