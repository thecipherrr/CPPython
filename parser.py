from lexer import Lexer

class BinaryOperation:
    def __init__(self, t_left, t_op, t_right):
        self.t_left = t_left 
        self.t_op = t_op 
        self.t_right = t_right 

    def __repr__(self):
        return f"BOP|{self.t_left}, {self.t_op}, {self.t_right}"

class UnaryOperation:
    def __init__(self, t_op, t_right):
        self.t_op = t_op 
        self.t_right = t_right
    
    def __repr__(self):
        return f"U|{self.t_op}, {self.t_right}"

class VariableCreation:
    def __init__(self, t_id, t_value):
        self.t_id = t_id 
        self.t_value = t_value

    def __repr__(self):
        return f"V|{self.t_id}, {self.t_value}"

class Parser():
    def __init__(self, filename, tokens):
        self.filename = filename
        self.tokens = tokens 

    def parse(self):
        ast = {"BinaryOperation" : []}
        for token in self.tokens:
            print(token)
            if token.t_type == "NUMERIC":
                ast["BinaryOperation"].append({"type":token.t_value})                
            elif token.t_type == "OPERATOR":
                ast["BinaryOperation"].append({"type":token.t_value})
        return ast 


parser = Parser("test.py", tokens)
ast = parser.parse()
print(ast)
