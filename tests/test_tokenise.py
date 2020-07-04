from lispinterpreter import tokenise, interpret


def test_basic_leetcode_cases():
    input_output_pairs = {
        "(add 1 2)": 3,
        "(mult 3 (add 2 3))": 15,
        "(let x 2 (mult x 5))": 10,
        "(let x 2 (mult x (let x 3 y 4 (add x y))))": 14,
        "(let x 3 x 2 x)": 2,
        "(let x 1 y 2 x (add x y) (add x y))": 5,
        "(let x 2 (add (let x 3 (let x 4 x)) x))": 6,
        "(let a1 3 b2 (add a1 1) b2)": 4,
    }
    for expr, expected_output in input_output_pairs.items():
        output = interpret(expr)
        assert output == expected_output


def test_tokenise():
    input_output_pairs = {
        "(mult 3 (add 2 3))": ["(", "mult", "3", "(", "add", "2", "3", ")", ")"],
        "(let x 2 (mult x (let x 3 y 4 (add x y))))": [
            "(",
            "let",
            "x",
            "2",
            "(",
            "mult",
            "x",
            "(",
            "let",
            "x",
            "3",
            "y",
            "4",
            "(",
            "add",
            "x",
            "y",
            ")",
            ")",
            ")",
            ")",
        ],
        "(let x 1 y 2 x (add x y) (add x y))": [
            "(",
            "let",
            "x",
            "1",
            "y",
            "2",
            "x",
            "(",
            "add",
            "x",
            "y",
            ")",
            "(",
            "add",
            "x",
            "y",
            ")",
            ")",
        ],
        "(let x 2 (add (let x 3 (let x 4 x)) x))": [
            "(",
            "let",
            "x",
            "2",
            "(",
            "add",
            "(",
            "let",
            "x",
            "3",
            "(",
            "let",
            "x",
            "4",
            "x",
            ")",
            ")",
            "x",
            ")",
            ")",
        ],
    }
    for expr, expected_output in input_output_pairs.items():
        output = list(tokenise(expr))
        assert expected_output == output
