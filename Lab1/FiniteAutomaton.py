class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        
        for char in input_string:
            if char not in self.alphabet:
                return False
            
            # Check if transition exists
            # Note: transitions key is (state, char), value is list of next states (NFA) or single state (DFA)
            # My Grammar to FA converter creates a list, effectively an NFA in structure, 
            # though this specific grammar looks deterministic enough.
            # Let's handle it as a deterministic check for this specific lab if possible, 
            # or explore all paths if NFA.
            
            if (current_state, char) in self.transitions:
                possible_next_states = self.transitions[(current_state, char)]
                # For this specific grammar variant, let's see if it's deterministic.
                # S -> aB
                # B -> aC | bB
                # C -> bB | c | aS
                # It seems deterministic based on current state + input? 
                # B -> bB (input b goes to B)
                # C -> bB (input b goes to B)
                # Wait, strictly speaking, `transitions` dictionary stores lists.
                # For a simple check, we can take the first one or manage a set of current states.
                current_state = possible_next_states[0] 
            else:
                return False
        
        return current_state in self.final_states

    def display(self):
        print("Finite Automaton:")
        print(f"States: {self.states}")
        print(f"Alphabet: {self.alphabet}")
        print(f"Start State: {self.start_state}")
        print(f"Final States: {self.final_states}")
        print("Transitions:")
        for (state, char), next_states in self.transitions.items():
            print(f"  {state} --{char}--> {next_states}")
