# Topic: Regular expressions

### Course: Formal Languages & Finite Automata
### Author: Soimu Ionut 

----

## Theory
Regular expressions (regex) are a powerful formal language concept used to describe target string patterns. They originated in mathematical theory but eventually emerged into computer science as an essential tool for string manipulation, data validation, lexical analysis and search-and-replace strategies. 

At a base level, regular expressions consist of constants, literal characters, and operators that dictate relationships such as alternation (`|`), concatenation, and repetition (`*`, `+`, `?`). In compiler design, these expressions provide a simplified way to generate sets of strings dynamically and construct finite automata capable of executing those tokens dynamically without hardcoded limits.

## Objectives:

1. Write a good report covering what regular expressions are and what they are used for.
2. Given a list of regular expressions per variant (Variant 3):
    - `O(P|Q|R)^+2(3|4)`
    - `A*B(C|D|E)F(G|H|I)^2`
    - `J^+K(L|M|N)*O?(P|Q)^3`
3. Write a code that dynamically generates valid combinations of symbols that conform to the given regular expressions. Ensure that it doesn't hardcode rules.
4. Bound unbounded repetitions (`*`, `+`) to 5 times.
5. **Bonus point**: include a debugging feature (trace) that outputs the sequence of processing the regular expression (showing concatenation, repetitions, and alternations in sequence).

## Implementation description

The script is developed in Python. Its architecture splits the processing array into a Lexer/Tokenizer, a Parser for Abstract Syntax Tree (AST) creation, and a Generator mechanism that recursively evaluates the structure.

### 1. Tokenizing the Regex
The process begins by parsing the string input. The `tokenize(regex_str)` function detects meta-characters (`(`, `|`, `*`) and explicitly identifies powers specified logically like `^+` and `^5`. It yields a linear array of literal values.
```python
def tokenize(regex_str):
    # Iterates over characters and groups things like `^+` or `^2`
    # ...
    elif c == '^':
        if i + 1 < len(regex_str) and regex_str[i+1].isdigit():
            # fetch full number to group repetition ranges
```

### 2. The Abstract Syntax Tree
Using the recursive descent mechanism, the lexer connects into the `Parser` class handling operation priority. I implemented node classes:
* `Literal`: Contains absolute individual characters.
* `Concatenation`: Links two successive sequences.
* `Alternation`: Represents an `OR` junction spanning an expression branch.
* `Repetition`: Takes bounds like `0 to 5` for `*`, and fixed bounds `3 to 3` for `^3`.
The grouping parenthesis automatically adjusts bounds by grouping parsing streams locally.

### 3. Dynamic Combination Generator
The `Generator` continuously runs `generate_random` using the root of the AST tree. It generates symbols randomly depending on the bounds defined by the parser. For example, the operator `|` yields a random 50/50 traversal of left/right branches. For `*`, a random `1` to `5` iterations multiplier applies recursively on its target sequence.
```python
elif isinstance(node, Repetition):
    repeats = random.randint(node.min_repeats, node.max_repeats)
    result = ""
    for _ in range(repeats):
        result += self.generate_random(node.node, step_counter)
    return result
```

This ensures we easily print fully random permutations every execution without hardcoding them strings!

### 4. Code Execution and Bonus Rule
The `Generator` class houses a boolean flag `debug`. When checked positive initially, it initiates a sequential counter algorithm `[1], [2], [3]...` and cascades console prints matching exactly what operator or repetition is being rolled or bypassed down the hierarchy. 

## Conclusions / Results

In this laboratory work, I successfully implemented a modular Regular Expression pattern interpreter from scratch. Rather than matching strings like traditional Regex engines do natively, the generator inverses the logic by traversing down an execution AST structure and randomly evaluating operators to construct combinations from scratch. It effortlessly bounded infinity loops like the recursive Kleene star using a safe capped `5` limit and satisfied all properties expected within dynamic generation scripts, all while logging sequential steps as a nice bonus component to explain program behavior directly to the user dynamically.