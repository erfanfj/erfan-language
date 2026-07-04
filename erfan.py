import os
import sys

from lexer.lexer import Lexer
from parser.parser import Parser
from interpreter.interpreter import Interpreter
from compiler.compiler import Compiler


def parse_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        code = f.read()

    lexer = Lexer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    return parser.parse()


def rundev(filename):
    tree = parse_file(filename)
    interpreter = Interpreter()
    interpreter.visit(tree)


def runbuild(filename):
    tree = parse_file(filename)

    source_dir = os.path.dirname(os.path.abspath(filename))
    base_name = os.path.splitext(os.path.basename(filename))[0]
    build_dir = os.path.join(source_dir, "build")
    output = os.path.join(build_dir, f"{base_name}.exe")

    compiler = Compiler()
    built_path = compiler.compile(tree, output=output)

    print(f"Build saved to: {built_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("    erfan rundev file.erfan")
        print("    erfan runbuild file.erfan")
        return

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "rundev":
        rundev(filename)
    elif command == "runbuild":
        runbuild(filename)
    else:
        print("Unknown command")
        print("Available commands: rundev, runbuild")


if __name__ == "__main__":
    main()
