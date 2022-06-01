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
        # for print statements
        out.write("cout << " + print_args + " << endl;")

    def write_var_assignment(self, out, var_type, var_name, var_value):
        out.write(var_type + " " + var_name + " = " + var_value + ";")

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
                    out.write("\t")
                    if syntax.t_value.token.t_type == "INT":
                        self.write_var_assignment(out, "int", syntax.t_id.t_value, str(syntax.t_value.token.t_value))
                    elif syntax.t_value.token.t_type == "FLOAT":
                        self.write_var_assignment(out, "float", syntax.t_id.t_value, str(syntax.t_value.token.t_value))
               
                elif syntax==None:
                    out.write("\n")
                    continue
                else:
                    print("Compilation Success!") 
                    return 0; 

            out.write("\n")
            out.write("\treturn 0;")
            out.write("\n}")
        
        out.close()

def main():
    with open("test_translate.py") as data:
        program = data.read()

    lexer = lex.Lexer("test_translate.py", program)
    tokens = lexer.generate_tokens()
    
    parser = yacc.Parser("test_translate.py", tokens, program)
    ast = parser.parse()

    trans = Translate(ast, "test_translate.py")
    out = trans.compile()

main() 
