# Python Logic Parser

A very simple logical expression parser written in python. Give it a propositional
expression and it prints the full truth table for every combination of its variables.

## Running

Make sure python is installed and run:

```console
python main.py
```

The program loops: type an expression, get a truth table, type the next one.
Press `Ctrl+C` to quit.

## Usage

Variables are any word that isn't an operator — `p`, `q`, `r`, or longer names like
`rain`. Parentheses group subexpressions and don't need surrounding spaces.

```console
$ python main.py
Expression: p and q
p q
0 0 False
0 1 False
1 0 False
1 1 True
```

The first line lists the variables in the order they first appear; the last column is
the value of the whole expression for that row.

Checking a tautology — one of De Morgan's laws, where every row comes out `True`:

```console
Expression: not (p or q) iff (not p and not q)
p q
0 0 True
0 1 True
1 0 True
1 1 True
```

### Operators

Operator names are case-insensitive (`and`, `AND` and `And` all work).

| Operator | Meaning | Symbol |
| --- | --- | --- |
| `not` | negation | ¬ |
| `and` | conjunction | ∧ |
| `or` | disjunction | ∨ |
| `imp` | implication | → |
| `if` | converse implication | ← |
| `iff` | biconditional | ↔ |
| `nand` | negated conjunction | ⊼ |
| `nor` | negated disjunction | ⊽ |
| `xor` | exclusive or | ⊕ |

### Precedence

Operators bind in the order listed above: `not` binds tightest, then `and`, `or`,
`imp`, `if`, `iff`, `nand`, `nor`, and finally `xor`. So `p or q and r` is read as
`p or (q and r)`, and `p and q xor r` as `(p and q) xor r`.

`imp`, `if` and `iff` are right-associative, so `p imp q imp r` means
`p imp (q imp r)`. Everything else is left-associative. When in doubt, parenthesise.

## Why I made this

I made this to help me in the Discrete math subject. Writing truth tables out by hand
for every exercise got tedious and error-prone, so I wrote something that would do the
bookkeeping for me and let me check my own answers. Also, it turned out 
to be a lot of fun :)

## How it works

| File | What it does |
| --- | --- |
| [`logic.py`](logic.py) | The truth functions themselves, one plain function per operator. |
| [`expressions.py`](expressions.py) | The expression tree: `AtomicExp` holds a variable's value, while `UnaryExp` and `BinaryExp` wrap an operator and its operands. |
| [`main.py`](main.py) | Tokenises the input, recurses into each parenthesised group, then binds operators one precedence level at a time to build the tree. |

Evaluating that tree once per row of the truth table produces the output.
