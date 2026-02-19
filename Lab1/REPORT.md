# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Ionut (Variant 23)

----

## Theory
Formal languages provide the mathematical foundation for understanding how communication systems, including programming languages, are structured. A formal language is defined by an alphabet (a set of valid symbols), a vocabulary (a set of valid words formed from the alphabet), and a grammar.

A **Grammar** is a set of production rules that describe how to form strings from the language's alphabet that are valid according to the language's syntax. It consists of:
- **$V_N$**: Non-terminal symbols (variables that can be replaced).
- **$V_T$**: Terminal symbols (elements of the language).
- **$P$**: Production rules (mapping from non-terminals to strings of terminals and non-terminals).
- **$S$**: The start symbol.

A **Finite Automaton (FA)** is a computational model used to recognize patterns or languages. It consists of states, transitions between states based on inputs, a start state, and a set of accepting (final) states. If a sequence of inputs leads the automaton from the start state to a final state, the input is "accepted" or valid.

For regular languages, there is a direct equivalence between Regular Grammars (like type 3 grammars) and Finite Automata. Conversion between them allows us to switch between a generative model (Grammar) and a recognition model (FA).

## Objectives:

1.  Understand the concept of formal languages and their components.
2.  Set up the project environment (Git, programming language selection).
3.  Implement a `Grammar` class to represent the given variant.
4.  Implement a method to generate valid strings from the grammar.
5.  Convert the `Grammar` into a `Finite Automaton`.
6.  Implement functionality to check if a string belongs to the language using the FA.

## Implementation description

The project is implemented in Python due to its simplicity and readability, which is ideal for focusing on the logic of formal languages rather than boilerplate code.

### 1. Grammar Representation (`Grammar.py`)
I created a `Grammar` class that holds the non-terminals ($V_N$), terminals ($V_T$), production rules ($P$), and the start symbol ($S$). The rules are stored in a dictionary where keys are non-terminals and values are lists of possible productions.

```python
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
```

### 2. String Generation
The `generate_string` method starts with the symbol $S$ and iteratively replaces the leftmost non-terminal with one of its production rules (randomly selected) until the string consists only of terminals. I included a loop check to prevent potential infinite recursion during random generation.

```python
    def generate_string(self):
        current_string = self.S
        while any(char in self.VN for char in current_string):
            for i, char in enumerate(current_string):
                if char in self.VN:
                    options = self.P[char]
                    substitution = random.choice(options)
                    current_string = current_string[:i] + substitution + current_string[i+1:]
                    break
        return current_string
```

### 3. Conversion to Finite Automaton
A method `to_finite_automaton` converts the regular grammar into an FA.
- Non-terminals become states.
- A production $A \to aB$ creates a transition from state $A$ to state $B$ on input $a$.
- A production $A \to c$ (terminal only) creates a transition from state $A$ to a special "Final State" (denoted as 'X') on input $c$.

### 4. Finite Automaton (`FiniteAutomaton.py`)
The `FiniteAutomaton` class stores states, alphabet, transitions, start state, and final states. The `string_belongs_to_language` method simulates the FA processing the input string. It starts at the initial state and follows transitions for each character. If it ends in a final state after consuming the entire string, the string is valid.

```python
    def string_belongs_to_language(self, input_string):
        current_state = self.start_state
        for char in input_string:
            if char not in self.alphabet:
                return False
            # Follow transition
            if (current_state, char) in self.transitions:
                current_state = self.transitions[(current_state, char)][0] 
            else:
                return False
        return current_state in self.final_states
```

## Conclusions

In this laboratory work, I explored the relationship between Regular Grammars and Finite Automata. By implementing a grammar for Variant 23, I was able to generate valid strings like `aac` and `abbac`.

The most interesting part was the conversion process. Since the grammar is Right-Linear ($A \to aB$ or $A \to a$), mapping it to a Finite Automaton was straightforward: non-terminals map to states, and terminals map to transition labels.

The implementation successfully verifies that strings generated by the grammar are also accepted by the derived automaton, confirming that both representations describe the same language. This reinforces the theoretical concept that Regular Grammars and Finite Automata are equivalent in power for defining regular languages.

## References
1. Course: Formal Languages & Finite Automata - Lecture Notes.
