from Grammar import Grammar

def main():
    # 1. Create Grammar
    print("--- Grammar ---")
    grammar = Grammar()
    
    # 2. Generate 5 valid strings
    print("\nGenerated 5 valid strings:")
    generated_strings = []
    for _ in range(5):
        s = grammar.generate_string()
        generated_strings.append(s)
        print(f" - {s}")

    # 3. Convert to Finite Automaton
    print("\n--- Finite Automaton ---")
    fa = grammar.to_finite_automaton()
    fa.display()

    # 4. Check strings
    print("\n--- String Verification ---")
    test_strings = generated_strings + ["aa", "abc", "bbbb", "aac"]
    for s in test_strings:
        result = fa.string_belongs_to_language(s)
        print(f"String '{s}' belongs to language? {result}")

if __name__ == "__main__":
    main()
