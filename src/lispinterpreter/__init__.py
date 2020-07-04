from typing import Iterable


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
