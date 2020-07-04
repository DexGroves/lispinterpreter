from typing import Iterable, Tuple, List, Union


Symbol = str
Number = Union[int, float]
Atom = Union[Symbol, Number]
Expression = Union[Atom, List]


def tokenise(expr: str) -> Iterable[str]:
    i = 0
    while i < len(expr):
        if expr[i] in {"(", ")"}:
            yield expr[i]
            i += 1
        elif expr[i] == " ":
            i += 1
        else:
            term = []
            while expr[i] not in {"(", ")", " "}:
                term.append(expr[i])
                i += 1
            yield "".join(term)


def gen_ast(tokens: Iterable[str], i: int = 0) -> Tuple[List[Expression], int]:
    ast = []
    while i < len(tokens):
        # print(i, tokens[i], ast)
        token = tokens[i]
        if token == ")":
            return ast, i + 1
        elif token == "(":
            sub_ast, i = gen_ast(tokens, i + 1)
            ast.append(sub_ast)
        else:
            ast.append(token)
            i += 1
    return ast
