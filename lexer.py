import string

## -> personal confusion note by Leon, lmao
# clear -> confusion is cleared
# Token Classes
OP = ['+', '-', '*', '/', '**', '<', '>']
DEL = ['(', ')', '[', ']', ':', ';']
RES = ['print', 'for', 'while', 'if', 'else', 'False', 'True', 'not', 'or', 'and'
       'except', 'break', 'def', 'lambda', 'class']

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
        ## what is indent and dedent for lol
        ## oh shit, right, indent is for new block, dedent is to return to previous block, how stupid
        ## clear
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
        ## what is this for, why append 0 at the beginning
        self.indent_stack.append(0)

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
                ## why continue is here, but not in other conditions (OP and DEL)?
                ## hypothesis 1: continue is to skip self.next() at the end of the top level while
                ## but then why need to skip self.next() at some conditions? hmm
                # continue
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
                ## what is this for
                ## why not start from 0 instead?
                ## hmm????????????????????
                decimal_count = 1
                while str(self.current) in ".0123456789":
                    if str(self.current) == ".":
                        ## why error if decimal_count is 2
                        ## clear
                        if decimal_count == 2:
                            # TODO implement error class later 
                            return Error("Float error", "invalid float")
                        decimal_count += 1
                    num += self.current 
                    self.next()
                if "." not in num:
                    tokens.append(Token("INT", int(num), self.pos))
                else:
                    tokens.append(Token("FLOAT", float(num), self.pos))
                ## refer above case
                ## clear?
                # continue
            elif self.current == "\n":
                self.lineno += 1
                self.curr_indent_level = 0
                tokens.append(Token("NEWLINE", self.current, self.pos))  
                self.next()
                ######## holy shit i don't understand this whole part
                ## clear
                ## hmm, i'm not really sure, but my intuition tells me this might bug
                ## example test case: what if all the lines only have one white space in the beginning of each?
                ## right, the only flaw is because we haven't tested for equal indent levels, right? or am i wrong?
                ## shit, this is confusing lmao
                ## nvm, if all of the whitespaces are of equal level, then there would be no indent at all
                ## so stupid, fuck
                ## edo, you're so smart dammit, just gimme your brain for a month dammit
                ## clear
                ## shouldn't this be four spaces multiplicities instead for the indent? but then,
                ## it is hard to check for four spaces, hmm, what is the solution
                ## hey, it might not be needed to check for four indentations in some interpreters right?
                ## technically, we're creating our own interpreter, our own rules, noice, lol
                ## clear
                if self.current == " ": # indentation token
                    ## why not make this a four times loop to check if it is a valid indent instead?
                    ## hmmmmm
                    ## not needed, because of the reason above
                    ## clear
                    while self.current == " ":
                        self.curr_indent_level += 1 
                        self.next()
                ## what why where how when???? lmao
                ## if current indent level is more than the last element of the indent stack, then
                if self.curr_indent_level > self.indent_stack[-1]:
                    ## why append the indent stack with current indent level? hmmm? what is the purpose?
                    ## clear
                    self.indent_stack.append(self.curr_indent_level)
                    tokens.append(Token("INDENT", None, self.pos))
                elif self.curr_indent_level < self.indent_stack[-1]:
                    for i in range(0, len(self.indent_stack)):
                        if self.indent_stack[-i] > self.curr_indent_level:
                            self.indent_stack.pop(i)
                            tokens.append(Token("DEDENT", None, self.pos))
                ## refer above cases, tried dabbling with this continue, doesn't seem to be code breaking if I remove
                ## this one
                # continue
            elif self.current == "=":
                tokens.append(Token("ASSIGN", self.current, self.pos))
            self.next() 
        return tokens


#with open("test.py") as data:
    #program = data.read()

#lexer = Lexer("test.py", program)
#tokens = lexer.generate_tokens()

#print(tokens)
