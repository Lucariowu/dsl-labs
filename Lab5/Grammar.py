import itertools
import copy

class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = set(VN)
        self.VT = set(VT)
        self.P = {k: set(v) for k, v in P.items()}
        self.S = S
        self.new_vars_count = 1

    def generate_new_var(self):
        while f"X{self.new_vars_count}" in self.VN:
            self.new_vars_count += 1
        var = f"X{self.new_vars_count}"
        self.VN.add(var)
        self.new_vars_count += 1
        return var

    def eliminate_epsilon_productions(self):
        nullable = set()
        for nt, prods in self.P.items():
            if 'epsilon' in prods:
                nullable.add(nt)

        changed = True
        while changed:
            changed = False
            for nt, prods in self.P.items():
                if nt not in nullable:
                    for prod in prods:
                        if all(char in nullable for char in prod):
                            nullable.add(nt)
                            changed = True

        new_P = {nt: set() for nt in self.VN}
        for nt, prods in self.P.items():
            for prod in prods:
                if prod == 'epsilon':
                    continue
                nullable_indices = [i for i, char in enumerate(prod) if char in nullable]
                for r in range(len(nullable_indices) + 1):
                    for combo in itertools.combinations(nullable_indices, r):
                        new_prod = "".join([char for i, char in enumerate(prod) if i not in combo])
                        if new_prod:
                            new_P[nt].add(new_prod)

        self.P = {nt: prods for nt, prods in new_P.items() if prods}

    def eliminate_renaming(self):
        unit_pairs = set()
        for nt in self.VN:
            unit_pairs.add((nt, nt))

        changed = True
        while changed:
            changed = False
            for A, B in list(unit_pairs):
                if B in self.P:
                    for prod in self.P[B]:
                        if len(prod) == 1 and prod in self.VN:
                            if (A, prod) not in unit_pairs:
                                unit_pairs.add((A, prod))
                                changed = True

        new_P = {nt: set() for nt in self.VN}
        for A, B in unit_pairs:
            if B in self.P:
                for prod in self.P[B]:
                    if not (len(prod) == 1 and prod in self.VN):
                        new_P[A].add(prod)

        self.P = {nt: prods for nt, prods in new_P.items() if prods}

    def eliminate_inaccessible_symbols(self):
        accessible = {self.S}
        changed = True
        while changed:
            changed = False
            for nt in list(accessible):
                if nt in self.P:
                    for prod in self.P[nt]:
                        for char in prod:
                            if char in self.VN and char not in accessible:
                                accessible.add(char)
                                changed = True
        
        self.VN = self.VN.intersection(accessible)
        self.P = {nt: prods for nt, prods in self.P.items() if nt in accessible}

    def eliminate_non_productive_symbols(self):
        productive = set()
        changed = True
        while changed:
            changed = False
            for nt, prods in list(self.P.items()):
                if nt not in productive:
                    for prod in prods:
                        if all(char in self.VT or char in productive for char in prod):
                            productive.add(nt)
                            changed = True

        self.VN = self.VN.intersection(productive)
        self.P = {nt: prods for nt, prods in self.P.items() if nt in productive}
        new_P = {}
        for nt, prods in self.P.items():
            valid_prods = set()
            for prod in prods:
                if all(char in self.VT or char in self.VN for char in prod):
                    valid_prods.add(prod)
            if valid_prods:
                new_P[nt] = valid_prods
        self.P = new_P

    def obtain_chomsky_normal_form(self):
        new_P = {nt: set() for nt in self.VN}
        terminal_vars = {}

        for nt, prods in self.P.items():
            for prod in prods:
                if len(prod) == 1 and prod in self.VT:
                    new_P[nt].add(prod)
                elif len(prod) >= 2:
                    new_prod = []
                    for char in prod:
                        if char in self.VT:
                            if char not in terminal_vars:
                                var = self.generate_new_var()
                                terminal_vars[char] = var
                                new_P[var] = {char}
                            new_prod.append(terminal_vars[char])
                        else:
                            new_prod.append(char)
                    new_P[nt].add(tuple(new_prod))

        final_P = {nt: set() for nt in self.VN}

        for nt, prods in new_P.items():
            for prod in prods:
                if isinstance(prod, str): 
                    final_P[nt].add(prod)
                elif len(prod) == 2:
                    final_P[nt].add("".join(prod))
                else:
                    curr_nt = nt
                    for i in range(len(prod) - 2):
                        new_var = self.generate_new_var()
                        final_P[curr_nt].add(f"{prod[i]}{new_var}")
                        curr_nt = new_var
                        if curr_nt not in final_P:
                            final_P[curr_nt] = set()
                    final_P[curr_nt].add(f"{prod[-2]}{prod[-1]}")

        self.P = final_P

    def to_chomsky_normal_form(self):
        print("1. Eliminating ε-productions...")
        self.eliminate_epsilon_productions()
        print(self)
        
        print("\n2. Eliminating unit productions (renaming)...")
        self.eliminate_renaming()
        print(self)
        
        print("\n3. Eliminating inaccessible symbols...")
        self.eliminate_inaccessible_symbols()
        print(self)
        
        print("\n4. Eliminating non-productive symbols...")
        self.eliminate_non_productive_symbols()
        print(self)
        
        print("\n5. Obtaining Chomsky Normal Form...")
        self.obtain_chomsky_normal_form()
        return self

    def __str__(self):
        p_str = ",\n  ".join([f"{k} -> {' | '.join(v)}" for k, v in self.P.items()])
        return f"VN: {self.VN}\nVT: {self.VT}\nP: {{\n  {p_str}\n}}\nS: {self.S}"

