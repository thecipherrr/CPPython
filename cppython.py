import src.lexer as lex
import src.py_parser as yacc
import src.translate_new as trans
import os
import sys

def usage():
    print("Usage: python main.py <SOURCE CODE> <SUBCOMMAND>")
    print("SUBCOMMANDS:")
    print(" translate       Translate the program")
    print(" compile         Compile the program (Not implemented yet)")

if __name__ == "__main__":
    if (len(sys.argv < 2)):
        usage()
        print("ERROR: Subcommand is not provided")
        exit(1)
