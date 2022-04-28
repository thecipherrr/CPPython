import lexer as lex

class Number:
    def __init__(self, token):
        self.token = token
    
    def __repr__(self):
        return f"N|{self.token}"

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

class PythonFunction:
    def __init__(self, t_def, t_id):
        self.t_def = t_def 
        self.t_id = t_id
        
    def __repr__(self):
        return f"F|{self.t_def}, {self.t_id}"

class Newline:
    def __init__(self, token):
       self.token = token 
    
    def __repr__(self):
        return f"LINE|{self.token}"

class Parser():
    def __init__(self, filename, tokens, text):
        self.filename = filename
        self.tokens = tokens 
        self.text = text 
        self.pos = -1 
        self.current = None 
        self.error = None 
        self.next()

    def next(self):
        self.pos += 1 
        self.current = (
            self.tokens[self.pos] if self.pos < len(self.tokens) else None
        )
    
    def binary_operation(self, func, op_token): 
        left = func()
        while (
            self.current.t_value if self.current != None else None
        ) in op_token:
            current_op_token = self.current
            self.next() 
            right = func()
            if right == None:
                # TODO implement error class later here
                return "error" 
            left = BinaryOperation(left, current_op_token, right)
        if self.current.t_type == "LPAREN":
            # TODO implement error class later too
            return "error"
        return left

    def level_1(self):
        temp_token = self.current 
        if temp_token.t_type == "NUMERIC":
            self.next()
            return Number(temp_token)
        elif temp_token.t_type == "OPERATOR":
            if temp_token.t_value == "+" or temp_token.t_value == "-":
                temp_token = self.current 
                self.next()
                num = self.level_1()
                return UnaryOperation(temp_token, num)


    def level_2(self):
        return self.binary_operation(self.level_1, ("*", "/"))

    def level_3(self):
        # for variable creation 
        if self.current.t_type == "IDENTIFIER":
            name = self.current 
            self.next()
            if self.current.t_type == "ASSIGN":
                self.next()
                data = self.level_3()
                return VariableCreation(name, data)
        
        # for addition and subtraction
        return self.binary_operation(self.level_2, ("+", "-"))

    def parse(self):
        result = self.level_3()
        return (result, None) if self.error == None else (None, self.error)


with open("test.py") as text:
    program = text.read()

lexer = lex.Lexer("test.py", program)
tokens = lexer.generate_tokens() 

parser = Parser("test.py", tokens, program)
ast = parser.parse()
print(ast)
