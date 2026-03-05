import random

class Grammar:
    def __init__(self, VN=None, VT=None, P=None, S=None):
        # Default initialization for Lab 1 variant, but allow overriding for Lab 2
        self.VN = VN if VN else {'S', 'B', 'C'}
        self.VT = VT if VT else {'a', 'b', 'c'}
        self.P = P if P else {
            'S': ['aB'],
            'B': ['aC', 'bB'],
            'C': ['bB', 'c', 'aS']
        }
        self.S = S if S else 'S'

    def generate_string(self):
        current_string = self.S
        
        while any(char in self.VN for char in current_string):
            for i, char in enumerate(current_string):
                if char in self.VN:
                    options = self.P[char]
                    substitution = random.choice(options)
                    current_string = current_string[:i] + substitution + current_string[i+1:]
                    break
            
            if len(current_string) > 20: 
                current_string = self.S 
                
        return current_string

    def to_finite_automaton(self):
        from FiniteAutomaton import FiniteAutomaton
        
        states = set(self.VN).union({'X'})
        alphabet = set(self.VT)
        start_state = self.S
        final_states = {'X'}
        transitions = {}

        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 2 and production[0] in self.VT and production[1] in self.VN:
                    term = production[0]
                    next_state = production[1]
                    if (non_terminal, term) not in transitions:
                        transitions[(non_terminal, term)] = []
                    transitions[(non_terminal, term)].append(next_state)
                
                elif len(production) == 1 and production[0] in self.VT:
                    term = production[0]
                    next_state = 'X'
                    if (non_terminal, term) not in transitions:
                        transitions[(non_terminal, term)] = []
                    transitions[(non_terminal, term)].append(next_state)

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    def classify_chomsky(self):
        """
        Classify the grammar based on the Chomsky hierarchy.
        Returns the type as an integer (0, 1, 2, or 3) and string representation.
        """
        is_type_3 = True
        is_type_2 = True
        is_type_1 = True
        is_type_0 = True # Every grammar is Type 0

        # Check conditions for each type
        for lhs, rhs_list in self.P.items():
            for rhs in rhs_list:
                # Type 1 check: |LHS| <= |RHS|
                if len(lhs) > len(rhs) and rhs != 'epsilon':
                    is_type_1 = False
                
                # Type 2 check: LHS is exactly one Non-Terminal
                if len(lhs) != 1 or lhs not in self.VN:
                    is_type_1 = False # If not Type 2, it's generally not Type 1 either in standard contexts
                    is_type_2 = False

                if is_type_2:
                    # Type 3 check: Right-Regular (A -> aB or A -> a)
                    # Note: strict regular also allows A -> epsilon (if A is S and S doesn't appear on RHS)
                    if len(rhs) > 2:
                        is_type_3 = False
                    elif len(rhs) == 2:
                        if not (rhs[0] in self.VT and rhs[1] in self.VN):
                            is_type_3 = False
                    elif len(rhs) == 1:
                        if rhs[0] not in self.VT and rhs[0] != 'epsilon':
                            is_type_3 = False

        if is_type_3: return "Type 3 (Regular)"
        if is_type_2: return "Type 2 (Context-Free)"
        if is_type_1: return "Type 1 (Context-Sensitive)"
        if is_type_0: return "Type 0 (Unrestricted)"

    def __str__(self):
        return f"VN: {self.VN}\nVT: {self.VT}\nP: {self.P}\nS: {self.S}"
