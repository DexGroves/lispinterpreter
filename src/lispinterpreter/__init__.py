from typing import Iterable, Tuple, List, Union, Any, Optional


Symbol = str
Number = int
Atom = Union[Symbol, Number]
Expression = Union[Atom, List["Expression"]]  # type: ignore


def interpret(expr: str) -> int:
    return eval_ast(gen_ast(tokenise(expr)))


class Env:
    """Scope for current vars. Lookups will fall back to parents before throwing."""
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def __setitem__(self, key, value):
        self.vars[key] = value

    def __getitem__(self, key):
        try:
            return self.vars[key]
        except KeyError as e:
            if self.parent:
                return self.parent[key]
            else:
                raise e

    def new(self):
        return Env(parent=self)


def tokenise(expr: str) -> List[str]:
    """
    Convert input expression to list of distinct symbols.
    (mult 3 (add 2 3)) -> (, mult, 3, (, add, 2, 3, ), )
    """
    def _tokenise(expr: str) -> Iterable[str]:
        try:
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
        except IndexError:
            raise SyntaxError(f"Parsing failed at position {i}.")

    return list(_tokenise(expr))


def gen_ast(tokens: List[str]):
    """
    Manipulate tokenised list of symbols into an abstract syntax tree.
    (let x 2 (add, x, (mult 2, 1))) -> [let, x, 2, [add, x, [mult, 2, 1]]]
    """
    def _gen_ast(tokens: List[str], i: int = 0) -> Tuple[List[Expression], int]:
        ast: List[Expression] = []
        while i < len(tokens):
            token = tokens[i]
            if token == ")":
                return ast, i + 1
            elif token == "(":
                sub_ast, i = _gen_ast(tokens, i + 1)
                ast.append(sub_ast)
            else:
                if _is_numeric(token):
                    token = int(token)  # type: ignore
                ast.append(token)
                i += 1
        return ast, i

    return _gen_ast(tokens)[0]


def eval_ast(ast: List[Expression], env: Optional[Env] = None):
    """
    Evaluate abstract syntax tree recursively.
    Each recursive level gets a new child env.
    """
    if env is None:
        env = Env()

    if len(ast) == 1:
        if isinstance(ast[0], int):
            return ast[0]
        elif isinstance(ast[0], str):
            return env[ast[0]]
        else:
            return eval_ast(ast[0], env.new())

    else:
        op = ast[0]
        if op == "add":
            lhs = eval_ast([ast[1]], env.new())
            rhs = eval_ast([ast[2]], env.new())
            return lhs + rhs
        elif op == "mult":
            lhs = eval_ast([ast[1]], env.new())
            rhs = eval_ast([ast[2]], env.new())
            return lhs * rhs
        elif op == "let":
            for symbol, expr in _chunk(ast[1:], 2):
                rv = eval_ast([expr], env.new())
                env[symbol] = rv
            if len(ast[1:]) % 2 == 1:
                return eval_ast([ast[-1]], env.new())
            else:
                return rv
        else:
            raise SyntaxError(f"Unrecognised operator {op}.")


def _is_numeric(s: str):
    try:
        int(s)
        return True
    except ValueError:
        return False


def _chunk(xs: List[Any], into: int) -> Iterable[List[Any]]:
    i = 0
    while i < len(xs) - into:
        yield xs[i : (i + into)]
        i += 2
