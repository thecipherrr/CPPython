import string

# Token Classes
OP = ['+', '-', '*', '/', '**']
DEL = ['(', ')', '[', ']']
RES = ['print', 'for', 'while', 'if', 'else']

class Token:
    def __init__(self, t_type, t_value, start):
        self.start = start
        self.t_type = t_type 
        self.t_value = t_value
    
    def __repr__(self):
        return f"Token({self.t_type}, {self.t_value})"

class Lexer:
    def __init__(self, filename, data:str):
        self.filename = filename 
        self.data = data
        self.lineno = 1
        self.pos = -1
        self.current = None
        self.next()

    def next(self):
        self.pos += 1
        self.current = (
            self.data[self.pos] if self.pos < len(self.data) else None
        )

    def generate_tokens(self):
        tokens = []

        while self.current != None: 
            if self.current in OP:
                tokens.append(Token("OPERATOR", self.current, self.pos)) # operator token
            elif self.current in DEL:
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

            self.next()
        return tokens

program = "0.5"
lexer = Lexer("test.py", program)
tokens = lexer.generate_tokens()

print(tokens)
