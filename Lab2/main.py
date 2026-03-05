from Grammar import Grammar
from FiniteAutomaton import FiniteAutomaton

def main():
    # 1. Grammar Classification (Using previous lab variant)
    print("--- 1. Chomsky Hierarchy Classification ---")
    grammar = Grammar()
    print("Grammar from Lab 1:")
    classification = grammar.classify_chomsky()
    print(f"Classification: {classification}\n")

    # 2. Variant FA Definition
    # Variant 23
    # Q = {q0,q1,q2},
    # ∑ = {a,b},
    # F = {q2},
    # δ(q0,a) = q0, δ(q0,a) = q1, δ(q1,b) = q2, 
    # δ(q0,b) = q0, δ(q2,b) = q2, δ(q1,a) = q0.

    states = {'q0', 'q1', 'q2'}
    alphabet = {'a', 'b'}
    final_states = {'q2'}
    start_state = 'q0'
    transitions = {
        ('q0', 'a'): ['q0', 'q1'],
        ('q0', 'b'): ['q0'],
        ('q1', 'b'): ['q2'],
        ('q1', 'a'): ['q0'],
        ('q2', 'b'): ['q2']
    }

    fa = FiniteAutomaton(states, alphabet, transitions, start_state, final_states)

    print("--- 2. Finite Automaton (Variant 23) ---")
    fa.display()

    print(f"\nIs the automaton deterministic? : {fa.is_deterministic()}")

    # 3. Conversion to Regular Grammar
    print("\n--- 3. Conversion to Regular Grammar ---")
    new_grammar = fa.to_grammar()
    print(new_grammar)

    # 4. Convert NDFA to DFA
    print("\n--- 4. Conversion NDFA to DFA ---")
    dfa = fa.to_dfa()
    dfa.display()
    print(f"Is the new automaton deterministic? : {dfa.is_deterministic()}")

    # 5. Graphical representation (System Graphviz)
    print("\n--- 5. Graphical Representation (System Graphviz backend) ---")
    print("Original NFA graph (DOT):")
    print(fa.to_dot())
    fa.generate_image("nfa.png")

    print("\nConverted DFA graph (DOT):")
    print(dfa.to_dot())
    dfa.generate_image("dfa.png")

if __name__ == "__main__":
    main()
