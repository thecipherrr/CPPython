import lexer as lex
import py_parser as yacc
import os

class Translate:
    def __init__(self, ast_input, file_input):
        self.ast_input = ast_input
        self.file_input = file_input

    def write_header(self, out):
        out.write("#include<iostream>")
        out.write("\n\n")
        out.write("using namespace std;")
        out.write("\n\n")

    def write_print(self, out, print_args):
        out.write("cout << " + print_args + "<< endl;")

    def compile(self):
        filename = os.path.splitext(self.file_input)[0]
        filename_out = filename + ".cpp"
        out = open(filename_out, "w+")
       
        self.write_header(out)
        out.write("int main(void)")        
        out.write("\n\n")
        out.write("{") 
        out.write("\n")

        for syntax in self.ast_input:
            # if function declaration, write outside of int main(void)
            if isinstance(syntax, yacc.FunctionDeclaration):
                # TODO: implement translation for function declaratin later
                # write outside of int main(void)
                out.write("foo in the line outside int main")
                out.write("foo")

            else:
                if isinstance(syntax, yacc.PythonFunction):
                   if syntax.t_identifier.t_value == "print":
                        out.write("\t")
                        self.write_print(out, syntax.t_args.token.t_value) 
                        
                elif isinstance(syntax, yacc.VariableCreation):
                    if syntax.t_identifier.t_value == "":
                        # TODO: implement variable creation later
                        print("foo")
               
                elif syntax==None:
                    out.write("\n")
                    print("Compilation Successful!")
                    return 0;

                out.write("\n")
                out.write("\treturn 0;")
                out.write("\n}")
        
        out.close()

def main():
    with open("test.py") as data:
        program = data.read()

    lexer = lex.Lexer("test.py", program)
    tokens = lexer.generate_tokens()
    
    parser = yacc.Parser("test.py", tokens, program)
    ast = parser.parse()

    trans = Translate(ast, "test.py")
    out = trans.compile()


main() 
