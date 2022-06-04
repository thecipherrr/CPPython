import string

# # -> personal note by Leon
# clear -> confusion is cleared
# --- -> do not change, already tested and code is working properly
# Token Classes
OP = ['+', '-', '*', '/', '%', '<', '>']
DEL = ['(', ')', '[', ']', ':', ';']
RES = ['print', 'for', 'while', 'if', 'else', 'False', 'True', 'not', 'or', 'and'
       'except', 'break', 'def', 'lambda', 'class']


# # ---? still can be improved
# Error class, has line number, position, type, and message
class Error:
    def __init__(self, e_line, e_pos, e_type, e_message):
        self.e_line = e_line
        self.e_pos = e_pos
        self.e_type = e_type
        self.e_message = e_message

    def __repr__(self):
        return f"Error({self.e_type, self.e_message}) at line {self.e_line} position {self.e_pos}"


# ---
# Token class, has type, value, and starting position
class Token:
    def __init__(self, t_type, t_value, start):
        self.t_type = t_type
        self.t_value = t_value
        self.start = start

    # return type only if there is no value
    def __repr__(self):
        return f"({self.t_type}, {self.t_value})" if {self.t_value} is not None else f"Token({self.t_type})"


class Lexer:
    # ---
    def __init__(self, filename, data:str):
        self.filename = filename
        self.data = data
        self.lineno = 1
        self.pos = -1
        self.current = None
        # initialize stack for INDENT and DEDENT tokens
        self.indent_stack = []
        # initialize current indentation level, because initially there is no indent
        # , but we need some value to increment later if there are any indents
        self.curr_indent_level = 0
        self.next()

    # ---
    # get next character, increment position
    def next(self):
        self.pos += 1
        self.current = (
            self.data[self.pos] if self.pos < len(self.data) else None
        )

    def lookahead(self):
        return self.data[self.pos+1] if self.pos+1 < len(self.data) else None
    # ---
    # main function to generate the tokens
    def generate_tokens(self):
        tokens = []
        # need to have at least one element initially
        self.indent_stack.append(0)

        # ---
        while self.current is not None:
            # check for exponent token
            # if self.current == "*":
            #     op = "*"
            #     self.next()
            #     if self.current == "*":
            #         op += "*"
            #         tokens.append(Token("OPERATOR", self.current, self.pos))
            #         continue
            # ---
            # check for operator token
            if self.current in OP:
                if self.current == "*":
                    if self.lookahead() == "*":
                        tokens.append(Token("OPERATOR", "**", self.pos))
                        self.next()
                        self.next()
                        continue
                tokens.append(Token("OPERATOR", self.current, self.pos))
            # ---
            # check for assignment token
            elif self.current == "=":
                tokens.append(Token("ASSIGN", self.current, self.pos))
            # ---
            # check for delimiter token
            elif self.current in DEL:
               tokens.append(Token("DELIMITER", self.current, self.pos))
            # ---
            # check for either identifier or reserved keyword
            elif self.current in string.ascii_letters:
                identifier = ""
                # loop till there is no characters left
                while str(self.current) in string.ascii_letters:
                   identifier += self.current
                   self.next()
                if identifier in RES:
                    tokens.append(Token("KEYWORD", identifier, self.pos)) # keyword token
                else:
                    tokens.append(Token("IDENTIFIER", identifier, self.pos)) # identifier token
                # continue is necessary here to avoid double next, so it does not skip the next possible token
                continue
            # ---
            # check for string
            elif self.current == '"':
                identifier = '"'
                self.next()
                # loop till find the next closing ", concatenate all the characters
                while str(self.current) != '"':
                    identifier += self.current
                    self.next()
                identifier += '"'
                tokens.append(Token("STRING", identifier, self.pos)) # string literal token
                # continue is not necessary here because we actually want the double next to skip the last "
            # ---
            # check for either integer or float
            elif str(self.current).isnumeric():
                num = ""
                # initially there are no '.'
                decimal_count = 0
                while str(self.current) in ".0123456789":
                    if str(self.current) == ".":
                        # if there is more than one ".", error
                        if decimal_count == 1:
                            # TODO implement error class later
                            return Error(self.lineno, self.pos, "Float error", "invalid float, more than one '.'")
                        decimal_count += 1
                    num += self.current
                    self.next()
                if "." not in num:
                    tokens.append(Token("INT", int(num), self.pos))
                else:
                    tokens.append(Token("FLOAT", float(num), self.pos))
                # continue is necessary here to avoid double next, so it does not skip the next possible token
                continue
            # ---
            # check for newline, after that check for indent and dedent
            elif self.current == "\n":
                self.lineno += 1
                self.curr_indent_level = 0
                tokens.append(Token("NEWLINE", self.current, self.pos))
                self.next()
                # indentation token
                # if whitespace found after newline, take it as indentation
                if self.current == " ":
                    # get indentation level by counting the whitespaces in while loop
                    # in this case, no need to check for multiplicities of 4
                    # since we are creating our own compiler
                    while self.current == " ":
                        self.curr_indent_level += 1
                        self.next()
                # if the current indentation level is more than the last indentation level,
                # then append the current indent level to the stack and
                # append token of type indent
                if self.curr_indent_level > self.indent_stack[-1]:
                    self.indent_stack.append(self.curr_indent_level)
                    tokens.append(Token("INDENT", None, self.pos))
                # if the current indentation level is less than the last indentation level
                # pop last indent and append current indent
                elif self.curr_indent_level < self.indent_stack[-1]:
                    self.indent_stack.pop(-1)
                    self.indent_stack.append(self.curr_indent_level)
                    # # this is not needed, i simplified and corrected the logic
                    # for i in range(0, len(self.indent_stack)):
                    #     if self.curr_indent_level < self.indent_stack[-i]:
                    #         self.indent_stack.pop(i)
                    tokens.append(Token("DEDENT", None, self.pos))
                continue
            # ---
            self.next()
        return tokens


# with open("test.py") as data:
#     program = data.read()
#
# lexer = Lexer("test.py", program)
# tokens = lexer.generate_tokens()
#
# print(tokens)
# with open("test_lexer.py") as data:
#     program = data.read()
#
# lexer = Lexer("test_lexer.py", program)
# tokens = lexer.generate_tokens()
#
# print(tokens)
