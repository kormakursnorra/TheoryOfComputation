import json
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
    trans_table: dict[ str, dict[ str, str ] ] = nfa.get('transition')
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


    marked_pairs     = set() # all marked pairs
    unmarked_pairs   = set() # all unmarked pairs
    reachable_states = set() # all reachable states

    # retrieve the DFAs states, transition table, start- and accept states
    all_states: set = dfa.get('states')
    start_state: str = dfa.get('start')

    # special cases: need to build a deep copy of accept states and transition
    trans_table: dict[ str, dict[ str, str ] ] = {
        state : {
            symbol : next_state for symbol, next_state in transition.items()
        }
        for state, transition in dfa.get('transition').items()
    }

    accept_states: set = dfa.get('accept').copy()

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

    # remove all instances of the unreachable state from the set of
    # accept states and transition table for the new DFA
    unreachable_states = all_states.difference( reachable_states )
    for state in unreachable_states:
        _ = trans_table.pop( state )
       
    accept_states.difference_update( unreachable_states )

    # step 2. initialize pairs of all the states (p, q)
    for state_a in reachable_states:
        for state_b in reachable_states:
            if state_a != state_b:
                # create pair and sort it's contents to collapse
                # duplicate pairs into the same key
                pair = frozenset( { state_a, state_b } )

                # step 3. mark all pairs where Qa is an accepting state and Qb isn't
                if (state_a in accept_states) != (state_b in accept_states):
                    marked_pairs.add( pair )
                else:
                    unmarked_pairs.add( pair )

    changed = True
    while changed:
        changed = False
        newly_marked = set()

        # step 4. loop through all unmarked pairs (p, q). For every symbol a ∈ Σ:
        for pair in unmarked_pairs:
            state_a, state_b = pair
            state_a_transitions: dict = trans_table.get( state_a )
            state_b_transitions: dict = trans_table.get( state_b )

            for symbol in symbols:
                next_state_a = state_a_transitions.get(symbol)
                next_state_b = state_b_transitions.get(symbol)
                # check the pair of destination states: (δ(p, a), δ(q, a)).
                destination_pair = frozenset( { next_state_a, next_state_b } )

                # if the destination pair is already marked, then mark (p, q).
                if destination_pair in marked_pairs:
                    newly_marked.add( pair )
                    changed = True
                    break

        # step 5. repeat step 4 until a full pass yields no new marks. Unmarked pairs are equivalent.
        marked_pairs.update( newly_marked )
        unmarked_pairs.difference_update( newly_marked )


    # step 6. process the unmarked pairs and update the DFA's key-values

    # build an adjacency list of all states as singleton sets
    adjacency = {}
    for state in reachable_states:
        adjacency[ state ] = set()

    # for each state p and q, make a self-loop edge
    for (state_a, state_b) in unmarked_pairs:
        adjacency[ state_a ].add( state_b )
        adjacency[ state_b ].add( state_a )

    visited = set()
    equivalence_classes = [] # initialize an empty list of combined components

    # for each state, find it's connected components if it has one
    # and group them together into a larger set
    for state in reachable_states:
        if state in visited:
            continue

        component = set()
        queue = [ state ]
        visited.add( state )

        while queue:
            current = queue.pop(0)
            component.add(current)
            for neighbor in adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        equivalence_classes.append(component)

    minimized_states  = reachable_states
    new_start_state   = start_state
    new_accept_states = accept_states
    new_trans_table   = trans_table

    for component in equivalence_classes:
        # iterate all combined componets of the minimized set of states
        # subsitute all instances of component states in the DFA with the combined set
        minimized_states.difference_update( component )
        minimized_states.add( frozenset( component ) )

        # update start- and accept states if required
        if start_state in component:
            new_start_state = frozenset( component )

        if not accept_states.isdisjoint( component ):
            new_accept_states.difference_update( component )
            new_accept_states.add( frozenset( component ) )

        for state, transition in new_trans_table.items():
            for symbol in symbols:
                next_state = transition.get( symbol )
                if next_state in component:
                    transition.update( { symbol : frozenset( component ) } )

        merged_transition = None
        for member in component:
            member_transition = new_trans_table.pop(member)
            if merged_transition is None:
                merged_transition = member_transition

        new_trans_table[frozenset(component)] = merged_transition

    minimized_dfa = {
        'states': minimized_states,
        'start': new_start_state,
        'accept': new_accept_states,
        'transition': new_trans_table
    }

    # step 7. construct the minimized dfa and return it
    return minimized_dfa
    


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

#     dfa_to_minimize = {
#         'states': {'A', 'B', 'C', 'D', 'E'},
#         'start': 'A',
#         'accept': {'C'},
#         'transition': {
#             'A': {'0': 'B', '1': 'C'},
#             'B': {'0': 'A', '1': 'C'},
#             'C': {'0': 'D', '1': 'D'},
#             'D': {'0': 'D', '1': 'D'},
#             'E': {'0': 'E', '1': 'E'}
#         }
#     }

#     determinize(nfa)
#     minimize(dfa_to_minimize)
    

# if __name__ == "__main__":
#     main()

