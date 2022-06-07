import lexer as lex
import py_parser as yacc
import os

class Translate:
    def __init__(self, ast_input, file_input):  
        self.ast_input = ast_input 
        self.file_input = file_input

    def write_header(self, out):
        out.write("#include<iostream>")
        out.write("\n")
        out.write("using namespace std;")
        out.write("\n\n")

    def write_main(self, out):
        out.write("int main(void)") 
        out.write("\n")
        out.write("{")
        out.write("\n")

    def write_print(self, out, print_args):
        # for print statements
        out.write("\tcout << " + print_args + " << endl;")
    
    

    def compile(self): 
        filename = os.path.splitext(self.file_input)[0]
        filename_out = filename + ".cpp"
        out = open(filename_out, "w+")

        root_type = self.ast_input.root.root.t_type
        root_value = self.ast_input.root.root.t_value
        child_value = self.ast_input.children[0].root.root.t_value
        print(root_type)
        print('\n')
        print(child_value)

        # writing the start of the program
        self.write_header(out)
        # writing out int main(void)
        self.write_main(out)
 
        if root_type == "KEYWORD":
            if root_value == "print":
                self.write_print(out, child_value)
       
        out.write("\n") 
        out.write("}")
        out.close()

def main():

    cwd = os.path.dirname(__file__)
    parentwd = os.path.split(cwd)[0]
    file_path = os.path.join(parentwd, "tests", "test_translate.py")

    with open(file_path) as data:
        program = data.read()

    lexer = lex.Lexer("test_translate.py", program)
    tokens = lexer.generate_tokens()
    
    parser = yacc.Parser(tokens)
    ast = parser.parse()

    trans = Translate(ast, "test_translate.py")
    out = trans.compile()

main()
