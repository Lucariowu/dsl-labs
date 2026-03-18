from Lexer import Lexer

def main():
    print("--- Formal Languages & Finite Automata ---")
    print("--- Lab 3: Lexer / Scanner Implementation ---\n")

    test_source_code = """
    let x = 10;
    let y = 20.5;
    
    let result = sin(x) + cos(y) * 3.14;
    
    if (result == 0) {
        print("Trigonometry is amazing!");
    } else {
        print("Math goes wrong here:");
        print(result);
    }
    """

    print("Source Code to Tokenize:")
    print("-" * 40)
    print(test_source_code)
    print("-" * 40)

    print("\nStarting Lexical Analysis...\n")
    lexer = Lexer(test_source_code)
    
    tokens = lexer.tokenize()

    print(f"{'Token Type':<15} | {'Value':<20} | {'Line':<5} | {'Col':<5}")
    print("-" * 55)
    
    for token in tokens:
        # Ignore EOF for cleaner output, but it IS produced by Lexer
        if token.type.name == "EOF":
            continue
            
        print(f"{token.type.name:<15} | {token.value:<20} | {token.line:<5} | {token.column:<5}")

    print("\nTokens successfully generated!")

if __name__ == "__main__":
    main()
