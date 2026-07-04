import os
import sys

MAGIC = b"ERFAN\x00"


def project_root():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read_embedded_source():
    with open(sys.executable, "rb") as handle:
        data = handle.read()

    marker = data.rfind(MAGIC)
    if marker == -1:
        raise RuntimeError("No embedded Erfan program found in this executable")

    length = int.from_bytes(data[marker + 6 : marker + 10], "little")
    start = marker + 10
    return data[start : start + length].decode("utf-8")


def main():
    root = project_root()
    if root not in sys.path:
        sys.path.insert(0, root)

    from lexer.lexer import Lexer
    from parser.parser import Parser
    from interpreter.interpreter import Interpreter

    source = read_embedded_source()
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    tree = parser.parse()
    interpreter = Interpreter()
    interpreter.visit(tree)


if __name__ == "__main__":
    main()
