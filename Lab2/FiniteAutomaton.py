class FiniteAutomaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = set(final_states) if isinstance(final_states, list) else final_states

    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        
        for char in input_string:
            if char not in self.alphabet:
                return False
            
            if (current_state, char) in self.transitions:
                possible_next_states = self.transitions[(current_state, char)]
                current_state = possible_next_states[0] 
            else:
                return False
        
        return current_state in self.final_states

    def is_deterministic(self):
        """
        Determines whether the finite automaton is deterministic.
        It is deterministic if for every state and input symbol, there is at most one transition.
        Also must not contain epsilon transitions.
        """
        for (state, symbol), destinations in self.transitions.items():
            if len(destinations) > 1:
                return False
        return True

    def to_grammar(self):
        """
        Converts the finite automaton to a regular grammar.
        """
        from Grammar import Grammar

        VN = set(self.states)
        VT = set(self.alphabet)
        P = {}
        S = self.start_state

        for state in self.states:
            P[state] = []

        for (state, symbol), destinations in self.transitions.items():
            for dest in destinations:
                # Production A -> aB
                P[state].append(f"{symbol}{dest}")
                
                # If destination is a final state, also add A -> a
                if dest in self.final_states:
                    P[state].append(f"{symbol}")

        # Clean empty production lists
        P = {k: list(set(v)) for k, v in P.items() if len(v) > 0}

        return Grammar(VN, VT, P, S)

    def to_dfa(self):
        """
        Converts this NFA to a DFA.
        Returns a new FiniteAutomaton object representing the DFA.
        """
        # Start state of DFA is the start state of NFA enclosed in a frozenset
        dfa_start_state = frozenset([self.start_state])
        dfa_states = set([dfa_start_state])
        dfa_transitions = {}
        dfa_final_states = set()

        # Queue for state set processing
        queue = [dfa_start_state]

        while queue:
            current_dfa_state = queue.pop(0)

            # Check if current_dfa_state contains any final states of the NFA
            if any(nfa_state in self.final_states for nfa_state in current_dfa_state):
                dfa_final_states.add(current_dfa_state)

            for char in self.alphabet:
                # Find all reachable NFA states from the states in current_dfa_state on 'char'
                next_nfa_states = set()
                for nfa_state in current_dfa_state:
                    if (nfa_state, char) in self.transitions:
                        for dest in self.transitions[(nfa_state, char)]:
                            next_nfa_states.add(dest)

                if next_nfa_states: # If there's a valid transition
                    next_dfa_state = frozenset(next_nfa_states)

                    # Add new state to queue and states set if not already seen
                    if next_dfa_state not in dfa_states:
                        dfa_states.add(next_dfa_state)
                        queue.append(next_dfa_state)

                    # Add transition
                    # We convert frozenset to tuple for easier formatting/hashing if needed, or string representation
                    str_current = ",".join(sorted(list(current_dfa_state)))
                    str_next = ",".join(sorted(list(next_dfa_state)))

                    if (str_current, char) not in dfa_transitions:
                        dfa_transitions[(str_current, char)] = []
                    dfa_transitions[(str_current, char)].append(str_next)

        # Map back to string states for consistency
        str_dfa_states = {",".join(sorted(list(state))) for state in dfa_states}
        str_dfa_start = ",".join(sorted(list(dfa_start_state)))
        str_dfa_finals = {",".join(sorted(list(state))) for state in dfa_final_states}

        return FiniteAutomaton(str_dfa_states, self.alphabet, dfa_transitions, str_dfa_start, str_dfa_finals)

    def to_dot(self):
        """
        Generates Graphviz DOT string representation of the automaton.
        Useful for visualization.
        """
        dot = ["digraph finite_automaton {", "    rankdir=LR;", "    node [shape = doublecircle];"]
        
        # Add final states
        dot.append("    " + " ".join([f'"{str(f)}"' for f in self.final_states]) + ";")
        
        dot.append("    node [shape = circle];")
        dot.append("    secret_start [shape=none, label=\"\"];")
        dot.append(f"    secret_start -> \"{self.start_state}\";")

        for (state, symbol), destinations in self.transitions.items():
            for dest in destinations:
                dot.append(f"    \"{state}\" -> \"{dest}\" [label=\"{symbol}\"];")

        dot.append("}")
        return "\n".join(dot)

    def generate_image(self, filename="automaton.png"):
        """
        Generates a PNG image of the automaton using the local system's Graphviz installation.
        Requires 'graphviz' to be installed locally (e.g., via pacman or apt).
        """
        import subprocess
        import tempfile
        import os

        dot_str = self.to_dot()
        
        # Create a temporary file to hold the .dot string securely
        fd, temp_path = tempfile.mkstemp(suffix=".dot")
        with os.fdopen(fd, 'w') as f:
            f.write(dot_str)

        try:
            # Run the system 'dot' command to render the image
            subprocess.run(["dot", "-Tpng", temp_path, "-o", filename], check=True, capture_output=True)
            print(f"Graph image successfully generated and saved to: {filename}")
        except FileNotFoundError:
            print("Error: The 'dot' command was not found. Please ensure Graphviz is installed on your system.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to generate graph image: {e.stderr.decode('utf-8')}")
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def display(self):
        print("Finite Automaton:")
        print(f"States: {self.states}")
        print(f"Alphabet: {self.alphabet}")
        print(f"Start State: {self.start_state}")
        print(f"Final States: {self.final_states}")
        print("Transitions:")
        for (state, char), next_states in self.transitions.items():
            print(f"  {state} --{char}--> {next_states}")
