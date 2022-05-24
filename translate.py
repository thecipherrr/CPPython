import parser


class Translate:
    def __init__(self, ast_input, file_output):
        self.ast_input = ast_input
        self.file_output = file_output
    

    def translate(self):
        for syntax in self.ast_input:
            print("hello World")


def main():
    trans = Translate(parser.ast, test.cpp)

main()
