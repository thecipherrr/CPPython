import src.lexer as lex
import src.py_parser as yacc
import src.translate as trans
import os
import sys
import string
import subprocess

def translate(filename, data):
    lexer = lex.Lexer(filename, data)
    tokens = lexer.generate_tokens()
    parser = yacc.Parser(tokens)
    ast = parser.parse()
    translator = trans.Translate(ast, filename)
    translator.translate_program()
    
def compile_program(filename, data):
    lexer = lex.Lexer(filename, data)
    tokens = lexer.generate_tokens()
    parser = yacc.Parser(tokens)
    ast = parser.parse()
    translator = trans.Translate(ast, filename)

    # if cpp file does not exist, make one using the translate function
    file_basename = os.path.splitext(filename)[0]
    file_cpp = file_basename + ".cpp"
    if not os.path.exists(file_cpp):
        print("C++ source code doesn't exist. Translating from provided Python file")
        translate(filename, data)
    subprocess.run(["build.sh", file_basename, file_cpp], shell=True)

def usage():
    print("Usage: python cppython.py <SUBCOMMAND> <FILENAME>")
    print("SUBCOMMANDS:")
    print("     translate       Translate the program")
    print("     compile         Compile the program (Translates from .py file if .cpp not present)")

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        usage()
        print("ERROR: Subcommand/file is not provided")
        exit(1)
   
    filename = sys.argv[-1]  
    subcommand = sys.argv[1] 

    with open(filename) as data:
        program = data.read()

    if subcommand == "translate":
        translate(filename, program) 
    elif subcommand == "compile":
        compile_program(filename, program)
    else:
        usage()
        print("ERROR: Unknown subcommand %s" % (subcommand))
        exit(1)
