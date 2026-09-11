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

    states_prime = set() # initialize DFA states
    accept_prime = set() # initialize DFA accept state/s
    delta_prime = {}     # initialize DFA transitions


    # retrieve the nfas transition table, start, accept and states
    trans_table: dict = nfa.get('transition')
    start_state = frozenset( { nfa.get('start') } )
    accept_states = frozenset( nfa.get('accept') )

    states_queue = []  # initialize "queue" to hold the states

    # add start state
    states_queue.append(start_state)
    states_prime.add(start_state)

    while( states_queue ):

        # retrieve the current state/s and initialize it's new transition
        states: frozenset = states_queue.pop( 0 )
        transition_prime = { states: { '0': {}, '1': {} } }

        # if the DFAs   intersects with the NFAs accept states
        # add it to the DFAs accept_prime; making it the accept state
        accept_intersect = states.intersection( accept_states )
        if accept_intersect:
            accept_prime.add( states )

        for symbol in symbols:
            # for each input symbol iterate the current subset of NFA states
            next_states = frozenset()
            for state in states:
                # retrieve the current states transitions-to states and
                # unionize them with every other transition-to state
                transition_to = trans_table.get( state ).get( symbol )
                next_states = next_states.union( frozenset( transition_to ) )

            # if the union is a new DFA state, add it
            if next_states not in states_prime:
                states_queue.append( next_states )
                states_prime.add( next_states )

            # retrieve the current states transition and for the current
            # symbol update the transition to the union of next states
            state_transition = transition_prime.get( states )
            state_transition.update( { symbol : next_states } )
            transition_prime.update( { states : state_transition } )

            # add the updated transition pair to the DFAs transitions set
            delta_prime.update( transition_prime )

    # assemble the new dfa and return it
    return {
        'states': states_prime, 
        'start': start_state, 
        'accept': accept_prime, 
        'transition': delta_prime 
    }

def minimize(dfa):
    """This function takes as input a DFA and returns a DFA that accepts the same language
    and has the fewest possible states.

    Args:
        dfa ( dict[str, Any] ): A dictionary representation of a DFA

    Returns:
        dict[str, Any]: A dictionary representation of a DFA with fewer possible states
    """

    # D - - - 0
    # C - - 0 -
    # B 0 0 - -
    # A 0 0 - -
    #   A B C D 

    # D          - 0
    # C          0 -
    # {A,B} 0    - -
    #      {A,B} C D 
    
    


    return True


# def main():
#     dfa = {
#         'states': {'A','B','C'},
#         'start': 'A',
#         'accept': {'C'},
#         'transition': {
#             'A': {'0': 'B', '1': 'C'},
#             'B': {'0': 'A', '1': 'C'},
#             'C': {'0': 'B', '1': 'A'}
#         }
#     }
#     nfa = {
#         'states': {'A','B','C'},
#         'start': 'A',
#         'accept': {'A','C'},
#         'transition': {
#             'A': {'0': {'B','C'}, '1': {'C'}},
#             'B': {'0': {'A','B'}, '1': set()},
#             'C': {'0': {'B'}, '1': {'A','B','C'}}
#         }
#     }

#     det_dfa = determinize(nfa)
#     min_dfa = minimize(dfa)

# if __name__ == "__main__":
#     main()

