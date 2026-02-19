import random

class Grammar:
    def __init__(self):
        self.VN = {'S', 'B', 'C'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aB'],
            'B': ['aC', 'bB'],
            'C': ['bB', 'c', 'aS']
        }
        self.S = 'S'

    def generate_string(self):
        # Start with the start symbol
        current_string = self.S
        
        # While there are non-terminals in the string
        while any(char in self.VN for char in current_string):
            # Find the first non-terminal (for leftmost derivation)
            # Or just any non-terminal. Let's do leftmost for simplicity.
            for i, char in enumerate(current_string):
                if char in self.VN:
                    # substitutions
                    options = self.P[char]
                    substitution = random.choice(options)
                    current_string = current_string[:i] + substitution + current_string[i+1:]
                    break
            
            # Safety break to avoid infinite loops during random generation if unlucky
            if len(current_string) > 20: 
                # Restart if it gets too long to ensure we get short valid strings too
                current_string = self.S 
                
        return current_string

    def to_finite_automaton(self):
        from FiniteAutomaton import FiniteAutomaton
        
        # States are Non-terminals + a specific Final state 'X' (convention often used)
        # If the grammar is regular (Right Linear), productions are like A -> aB or A -> a
        
        states = self.VN.union({'X'})
        alphabet = self.VT
        start_state = self.S
        final_states = {'X'}
        transitions = {}

        for non_terminal, productions in self.P.items():
            for production in productions:
                # Assuming Right Regular Grammar: A -> tB or A -> t
                
                # Check if production is A -> tB (terminal followed by non-terminal)
                if len(production) == 2 and production[0] in self.VT and production[1] in self.VN:
                    term = production[0]
                    next_state = production[1]
                    if (non_terminal, term) not in transitions:
                        transitions[(non_terminal, term)] = []
                    transitions[(non_terminal, term)].append(next_state)
                
                # Check if production is A -> t (terminal only) -> transitions to Final State
                elif len(production) == 1 and production[0] in self.VT:
                    term = production[0]
                    next_state = 'X' # Terminal state
                    if (non_terminal, term) not in transitions:
                        transitions[(non_terminal, term)] = []
                    transitions[(non_terminal, term)].append(next_state)

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)
