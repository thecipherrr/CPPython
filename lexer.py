import string

# Token Classes
OP = ['+', '-', '*', '/', '**', '<', '>']
DEL = ['(', ')', '[', ']', ':', ';']
RES = ['print', 'for', 'while', 'if', 'else', 'False', 'True', 'not', 'or', 'and'
       'except', 'break', 'def', 'lambda']


class Error:
    def __init__(self, e_type, e_message):
        self.e_type = e_type 
        self.e_message = e_message 

    def __repr__(self):
        return f"Error({self.e_type, self.e_message})"

class Token:
    def __init__(self, t_type, t_value, start):
        self.start = start
        self.t_type = t_type 
        self.t_value = t_value
    
    def __repr__(self):
        return f"Token({self.t_type}, {self.t_value})" if {self.t_value} != None else f"Token({self.t_type})"

class Lexer:
    def __init__(self, filename, data:str):
        self.filename = filename 
        self.data = data
        self.lineno = 1
        self.pos = -1
        self.current = None  
        self.indent_stack = [] # initialize stack for INDENT and DEDENT tokens 
        self.curr_indent_level = 0 # initialize current indentation level
        self.next()

    def next(self):
        self.pos += 1
        self.current = (
            self.data[self.pos] if self.pos < len(self.data) else None
        )

    def generate_tokens(self):
        tokens = []
        self.indent_stack.append(0)

        while self.current != None: 
            if self.current in OP:
                tokens.append(Token("OPERATOR", self.current, self.pos)) # operator token
            elif self.current in DEL:
                # indentation token implementation 
               tokens.append(Token("DELIMITER", self.current, self.pos)) # delimiter token 
            elif self.current in string.ascii_letters:
                identifier = ""
                while str(self.current) in string.ascii_letters:
                   identifier += self.current
                   self.next()
                if identifier in RES:
                    tokens.append(Token("KEYWORD", identifier, self.pos)) # keyword token
                else:
                    tokens.append(Token("IDENTIFIER", identifier, self.pos)) # identifier token
                continue
            elif self.current == '"':
                identifier = '"'
                self.next()
                while str(self.current) != '"':
                    identifier += self.current
                    self.next()
                identifier += '"'
                tokens.append(Token("STRING", identifier, self.pos)) # string literal token 
            elif str(self.current).isnumeric():
                num = ""
                decimal_count = 1 
                while str(self.current) in ".0123456789":
                    if str(self.current) == ".":
                        if decimal_count == 2:
                            # TODO implement error class later 
                            return "error"
                        decimal_count += 1
                    num += self.current 
                    self.next()
                tokens.append(Token("NUMERIC", float(num), self.pos))
                continue  
            elif self.current == "\n":
                self.lineno += 1
                self.curr_indent_level = 0
                tokens.append(Token("NEWLINE", self.current, self.pos))  
                self.next() 
                if self.current == " ":
                    while self.current == " ":
                        self.curr_indent_level += 1 
                        self.next()
                if self.curr_indent_level > self.indent_stack[-1]:
                    self.indent_stack.append(self.curr_indent_level)
                    tokens.append(Token("INDENT", None, self.pos))
                elif self.curr_indent_level < self.indent_stack[-1]:
                    for i in range(0, len(self.indent_stack)):
                        if self.indent_stack[-i] > self.curr_indent_level:
                            self.indent_stack.pop(i)
                            tokens.append(Token("DEDENT", None, self.pos)) 
                continue 
            elif self.current == "=":
                tokens.append(Token("ASSIGN", self.current, self.pos))
            self.next() 
        return tokens


with open("test.py") as data:
    program = data.read()

lexer = Lexer("test.py", program)
tokens = lexer.generate_tokens()

print(tokens)
