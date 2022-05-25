import lexer as lex
import py_parser as yacc

class Translate:
    def __init__(self, ast_input, file_output):
        self.ast_input = ast_input
        self.file_output = file_output
    
    def compile(self):
        with open(self.file_output, "w") as out:
            out.write("#include<iostream>")
            out.write("\n\n")
            out.write("using namespace std;")
            out.write("\n\n")
        
            for syntax in self.ast_input:
                if isinstance(syntax, yacc.PythonFunction):
                    if syntax.t_identifier.t_value == "print":
                        print(syntax.t_args.token.t_value)
                        out.write("int main(void)")
                        out.write("\n")
                        out.write("{")
                        out.write("\n")
                        out.write("\t cout << " + syntax.t_args.token.t_value + " << endl;")
                        out.write("\n \t return 0;")
                        out.write("\n}")
                        print("Compilation succesful")
                        return 0
                if isinstance(syntax, yacc.VariableCreation):
                    if syntax.t_identifier.t_value == ""
                
                

def main():
    with open("test.py") as data:
        program = data.read()

    lexer = lex.Lexer("test.py", program)
    tokens = lexer.generate_tokens()
    
    parser = yacc.Parser("test.py", tokens, program)
    ast = parser.parse()

    trans = Translate(ast, "test.cpp")
    out = trans.compile()


main() 
