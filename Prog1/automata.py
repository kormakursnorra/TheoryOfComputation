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


    # retrieve the NFAs transition table, start- and accept states
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

        # if the DFAs intersects with the NFAs accept states add
        # it to the DFAs accept_prime; making it the accept state
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

def minimize( dfa: dict ):
    """This function takes as input a DFA and returns a DFA that accepts the same language
    and has the fewest possible states.

    Args:
        dfa ( dict[str, Any] ): A dictionary representation of a DFA

    Returns:
        dict[str, Any]: A dictionary representation of a DFA with fewer possible states
    """

    # C     0
    # B   0
    # A 0
    #   A B C

    #  C   0
    # AB 0 -
    #   AB C

    # B
    # C 0 0
    # D 1 1 0
    #   A B C

    # ---- From slides ----:
    # 1. Remove Unreachable States: Eliminate any states that cannot be reached from the start state.
    #
    # 2. Initialize Table: Create a lower-triangular table for all pairs of states (p, q).
    #
    # 3. Base Case (Pass 0): Mark all pairs where one state is an accepting state (F ) and the other is a non-accepting state
    #    (Q \ F ). These are distinguishable by the empty string ε.
    #
    # 4. Recursive Step: Loop through all unmarked pairs (p, q). For every symbol a ∈ Σ:
    #    - Check the pair of destination states: (δ(p, a), δ(q, a)).
    #    - If the destination pair is already marked, then mark (p, q).
    #
    # 5. Termination: Repeat Step 4 until a full pass yields no new marks. Unmarked pairs are equivalent.

    pairs_of_states = {}  # all pairs of states (p, q)
    reachable_states = set() # all reachable states

    # retrieve the DFAs transition table, start- and accept states
    trans_table: dict = dfa.get('transition')
    start_state: str = dfa.get('start')
    accept_states: set = dfa.get('accept')

    states_queue = []  # initialize "queue" to hold the states

    # add start state to queue and reachable states
    reachable_states.add( start_state )
    states_queue.append( start_state )

    # step 1. create the set of reachable states
    while( states_queue ):
        state = states_queue.pop( 0 )

        # retrieve it's reachable states
        transition_states: dict = trans_table.get( state )

        # add state to reachable set and queue if not visited
        for next_state in transition_states.values():
            if next_state not in reachable_states:
                reachable_states.add( next_state )
                states_queue.append( next_state )


    # step 2. initialize pairs of all the states (p, q)
    for state_a in reachable_states:
        for state_b in reachable_states:
            if state_a != state_b:
                # create pair and sort it's contents to collapse
                # duplicate pairs into the same key
                pair = tuple( sorted(( state_a, state_b)) )

                # step 3. mark all pairs where Qa is an accepting state and Qb isn't
                if state_a in accept_states and state_b not in accept_states:
                    pairs_of_states.update( { pair : 1 } ) # marked
                else:
                    pairs_of_states.update( { pair : 0 } ) # not-marked


    # step 4. Recursive Step: Loop through all unmarked pairs (p, q). For every symbol a ∈ Σ:
    #    - Check the pair of destination states: (δ(p, a), δ(q, a)).
    #    - If the destination pair is already marked, then mark (p, q).

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

    dfa_to_minimize = {
        'states': {'A', 'B', 'C', 'D', 'E'},
        'start': 'A',
        'accept': {'C'},
        'transition': {
            'A': {'0': 'B', '1': 'C'},
            'B': {'0': 'A', '1': 'C'},
            'C': {'0': 'D', '1': 'D'},
            'D': {'0': 'D', '1': 'D'},
            'E': {'0': 'E', '1': 'E'}
        }
    }

    determinize(nfa)
    minimize(dfa_to_minimize)

if __name__ == "__main__":
    main()

