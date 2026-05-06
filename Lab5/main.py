from Grammar import Grammar

def main():
    VN = {'S', 'A', 'B', 'C', 'D'}
    VT = {'a', 'b', 'd'}
    P = {
        'S': ['dB', 'AC'],
        'A': ['d', 'dS', 'aBdB'],
        'B': ['a', 'aA', 'AC'],
        'C': ['bC', 'epsilon'],
        'D': ['ab']
    }
    S = 'S'

    grammar = Grammar(VN, VT, P, S)
    print("Original Grammar:")
    print(grammar)

    print("\nStarting Normalization Process to Chomsky Normal Form (CNF):")
    cnf_grammar = grammar.to_chomsky_normal_form()
    print("\nFinal Grammar in Chomsky Normal Form:")
    print(cnf_grammar)


if __name__ == "__main__":
    main()
