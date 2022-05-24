import lexer as lex
import parser as yacc

class Translate:
    def __init__(self, ast_input, file_output):
        self.ast_input = ast_input
        self.file_output = file_output
    
    def translate(self):
        for syntax in self.ast_input:
            print("Hello World")

def main():
    with open("test.py") as data:
        program = data.read()

    lexer = lex.Lexer("test.py", program)
    tokens = lexer.generate_tokens()

    parser = yacc.Parser()
    ast = parser.parse()
    trans = Translate(ast, None)

main()
