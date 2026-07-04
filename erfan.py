import sys

from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter


def run(filename):
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    interpreter = Interpreter()
    interpreter.visit(tree)


def main():

    if len(sys.argv) < 3:
        print("Usage:")
        print("    erfan run file.erfan")
        return

    command = sys.argv[1]

    if command == "run":
        run(sys.argv[2])

    else:
        print("Unknown command")


if __name__ == "__main__":
    main()