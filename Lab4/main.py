import random

class RegexNode:
    pass

class Literal(RegexNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self): return f"Literal('{self.value}')"

class Concatenation(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self): return f"Concat({self.left}, {self.right})"

class Alternation(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self): return f"Alt({self.left}, {self.right})"

class Repetition(RegexNode):
    def __init__(self, node, min_repeats, max_repeats):
        self.node = node
        self.min_repeats = min_repeats
        self.max_repeats = max_repeats
    def __repr__(self): return f"Rep({self.node}, {self.min_repeats}-{self.max_repeats})"

def tokenize(regex_str):
    tokens = []
    i = 0
    while i < len(regex_str):
        c = regex_str[i]
        if c in '()|*+?':
            tokens.append(c)
            i += 1
        elif c == '^':
            if i + 1 < len(regex_str) and regex_str[i+1] == '+':
                tokens.append('+')
                i += 2
            elif i + 1 < len(regex_str) and regex_str[i+1].isdigit():
                num = ''
                i += 1
                while i < len(regex_str) and regex_str[i].isdigit():
                    num += regex_str[i]
                    i += 1
                tokens.append(('^', int(num)))
            else:
                tokens.append(c)
                i += 1
        else:
            tokens.append(c)
            i += 1
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        return self.parse_alt()

    def parse_alt(self):
        node = self.parse_concat()
        while self.pos < len(self.tokens) and self.tokens[self.pos] == '|':
            self.pos += 1
            right = self.parse_concat()
            node = Alternation(node, right)
        return node

    def parse_concat(self):
        node = self.parse_rep()
        while self.pos < len(self.tokens) and self.tokens[self.pos] not in ('|', ')'):
            right = self.parse_rep()
            if right is None:
                break
            node = Concatenation(node, right)
        return node

    def parse_rep(self):
        node = self.parse_primary()
        if node is None:
            return None
            
        while self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            if t == '*':
                node = Repetition(node, 0, 5)
                self.pos += 1
            elif t == '+':
                node = Repetition(node, 1, 5)
                self.pos += 1
            elif t == '?':
                node = Repetition(node, 0, 1)
                self.pos += 1
            elif isinstance(t, tuple) and t[0] == '^':
                node = Repetition(node, t[1], t[1])
                self.pos += 1
            else:
                break
        return node

    def parse_primary(self):
        if self.pos >= len(self.tokens):
            return None
        t = self.tokens[self.pos]
        if t == '(':
            self.pos += 1
            node = self.parse_alt()
            if self.pos < len(self.tokens) and self.tokens[self.pos] == ')':
                self.pos += 1
            return node
        else:
            self.pos += 1
            return Literal(t)

class Generator:
    def __init__(self, debug=False):
        self.debug = debug

    def generate_random(self, node, step_counter=[1]):
        if isinstance(node, Literal):
            if self.debug: print(f"[{step_counter[0]}] Matched Literal '{node.value}'")
            step_counter[0] += 1
            return node.value
        elif isinstance(node, Concatenation):
            if self.debug: print(f"[{step_counter[0]}] Evaluating Concatenation")
            step_counter[0] += 1
            left = self.generate_random(node.left, step_counter)
            right = self.generate_random(node.right, step_counter)
            return left + right
        elif isinstance(node, Alternation):
            if self.debug: print(f"[{step_counter[0]}] Evaluating Alternation")
            step_counter[0] += 1
            # Handle multiple chained alternations accurately by randomly picking left or right
            if random.choice([True, False]):
                if self.debug: print("  -> Chose Left Branch")
                return self.generate_random(node.left, step_counter)
            else:
                if self.debug: print("  -> Chose Right Branch")
                return self.generate_random(node.right, step_counter)
        elif isinstance(node, Repetition):
            if self.debug: print(f"[{step_counter[0]}] Evaluating Repetition ({node.min_repeats} to {node.max_repeats} times)")
            step_counter[0] += 1
            repeats = random.randint(node.min_repeats, node.max_repeats)
            if self.debug: print(f"  -> Repeating {repeats} times")
            result = ""
            for _ in range(repeats):
                result += self.generate_random(node.node, step_counter)
            return result
        return ""

def process_regex(regex, debug=False, generate_count=5):
    print(f"\n--- Processing Regex: {regex} ---")
    tokens = tokenize(regex)
    parser = Parser(tokens)
    ast = parser.parse()
    
    generator = Generator(debug=debug)
    
    results = set()
    for _ in range(generate_count):
        # Only print debug trace for the first generation
        first_run = (_ == 0 and debug)
        generator.debug = first_run
        
        word = generator.generate_random(ast, [1])
        results.add(word)
        if first_run:
            print("\nGenerated combinations:")
            
    print(f"Result set: {results}")


if __name__ == '__main__':
    # Variant 3
    print("=== VARIANT 3 ===")
    regexes_v3 = [
        "O(P|Q|R)^+2(3|4)",
        "A*B(C|D|E)F(G|H|I)^2",
        "J^+K(L|M|N)*O?(P|Q)^3"
    ]
    
    for r in regexes_v3:
        process_regex(r, debug=True, generate_count=5)
    
