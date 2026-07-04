from lexer.lexer import Lexer

with open("test.erfan", "r", encoding="utf8") as f:
    code = f.read()

lexer = Lexer(code)

for token in lexer.tokenize():
    print(token)