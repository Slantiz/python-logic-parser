from expressions import Exp, AtomicExp, UnaryExp, BinaryExp
import logic

OPERATORS: dict[str, Exp] = {
    "not": UnaryExp(logic.lnot),
    "and": BinaryExp(logic.land),
    "or": BinaryExp(logic.lor),
    "imp": BinaryExp(logic.limplies)
}


def is_operator(s: str):
    return s.casefold() in OPERATORS


def create_expression(s: str):
    # split variables with parenthesis
    new_s = ""
    for l in s:
        if l == "(" or l == ")": new_s += f" {l} "
        else: new_s += l

    tokens = new_s.strip().split()

    variables: dict[str, AtomicExp] = {}

    # identify variables
    for t in tokens:
        if is_operator(t): continue
        if t == "(" or t == ")": continue
        if t in variables: continue
        variables[t] = AtomicExp()

    return create_expression_level(tokens, variables), variables


def create_expression_level(tokens: list[str], variables: dict[str, AtomicExp]) -> Exp:
    operators: dict[str, list[list[int]]] = {op: [] for op in OPERATORS}
    expressions: list[Exp | int] = []

    num_expressions = 0
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if is_operator(t):
            if isinstance(OPERATORS[t], UnaryExp): operators[t].append([num_expressions])
            elif isinstance(OPERATORS[t], BinaryExp): operators[t].append([num_expressions - 1, num_expressions])
            i += 1
            continue

        if t == "(":
            depth = 1
            closing_i = i + 1
            while True:
                if tokens[closing_i] == ")":
                    depth -= 1
                    if depth == 0: break
                elif tokens[closing_i] == "(": depth += 1
                closing_i += 1

            expressions.append(create_expression_level(tokens[i + 1:closing_i], variables))
            num_expressions += 1
            i = closing_i + 1
            continue
                
        expressions.append(variables.get(t))
        num_expressions += 1
        i += 1
    
    for op, op_targets in operators.items():
        cls = OPERATORS.get(op)
        for targets in op_targets:
            exp = cls.copy()
            exp.apply(targets, expressions)
    
    return expressions[0]


# input
s = "(P and Q) or C imp (D or Q)"

exp, variables = create_expression(s)

header = ""
for v_name in variables.keys():
    header += f"{v_name} "

print(header)

for i in range(2**len(variables)):
    s = ""
    for n, v in enumerate(variables.values()):
        v.value = not int(i / 2**(len(variables) - n - 1)) % 2 == 0
        s += f"{1 if v.value else 0} "
    
    s += f"{exp.eval()}"
    print(s)
