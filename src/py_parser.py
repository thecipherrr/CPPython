import lexer as lex
import os

# class String:
#     def __init__(self, token):
#         self.token = token
#
#     def __repr__(self):
#         return f"(STR|{self.token})"

# class Number:
#     def __init__(self, token):
#         self.token = token
#
#     def __repr__(self):
#         return f"(N|{self.token})"

# class BinaryOperation:
#     def __init__(self, t_left, t_op, t_right):
#         self.t_left = t_left
#         self.t_op = t_op
#         self.t_right = t_right
#
#     def __repr__(self):
#         return f"(BOP|{self.t_left}, {self.t_op}, {self.t_right})"

# class UnaryOperation:
#     def __init__(self, t_op, t_right):
#         self.t_op = t_op
#         self.t_right = t_right
#
#     def __repr__(self):
#         return f"(U|{self.t_op}, {self.t_right})"

# class VariableCreation:
#     def __init__(self, t_id, t_value):
#         self.t_id = t_id
#         self.t_value = t_value
#
#     def __repr__(self):
#         return f"(V|{self.t_id}, {self.t_value})"

# class PythonFunction:
#     def __init__(self, t_identifier, t_args):
#         self.t_identifier = t_identifier
#         self.t_args = t_args
#
#     def __repr__(self):
#         return f"(F|{self.t_identifier}, {self.t_args})"

# class FunctionDeclaration:
#     def __init__(self, t_func_name, t_args):
#         self.t_func_name = t_func_name
#         self.t_args = t_args
#
#     def __repr__(self):
#         return f"(FDEF|{self.t_identifier}, {self.t_args})"

# class Newline:
#     def __init__(self, token):
#        self.token = token
#
#     def __repr__(self):
#         return f"(LINE|{self.token})"


class TreeNode:
    def __init__(self, root, children=None):
        self.root = root
        self.children = ([] if children is None else list(children))

    def inorder(self):
        res = ""
        total = len(self.children)
        for i in range(total - 1):
            if self.children[i]:
                res += self.children[i].inorder()
        res += self.root
        if total >= 1:
            res += self.children[total-1].inorder()
        return res

    # root, children
    def dfs_prec(self):
        res = "( "
        res += self.root
        total = len(self.children)
        for i in range(total):
            if self.children[i]:
                res += self.children[i].dfs_prec()
        res += " )"
        return res

    def dfs_inorder_prec(self):
        res = "("
        total = len(self.children)
        for i in range(total - 1):
            if self.children[i]:
                res += self.children[i].dfs_inorder_prec()
        res += " " + self.root.__repr__() + " "
        if total >= 1:
            res += self.children[total-1].dfs_inorder_prec()
        res += ")"
        return res

    def __repr__(self):
        return self.dfs_prec()

# a = TreeNode("hello")
# a.children = [TreeNode("there"), TreeNode("hey"), TreeNode("what")]
# a.children[0].children=[TreeNode("a"), TreeNode("bd"), TreeNode("c")]
# print(a)

# TODO fix parsing functions so that it follows polish notation rule
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = -1
        self.current = None
        self.next()
        self.AST = None

    def next(self):
        self.pos += 1
        self.current = (
            self.tokens[self.pos] if self.pos < len(self.tokens) else None
        )

    def lookahead(self):
        return self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None

    # ---
    def accept_token(self, t_type, t_value=None):
        token = self.current
        if token is not None:
            if token.t_type in t_type:
                if t_value is not None and token.t_value in t_value:
                    self.next()
                    return True
        return False

    def accept_type(self, t_type):
        if self.current is not None:
            if self.current.t_type == t_type:
                self.next()
                return True
        return False

    def accept_value(self, t_value):
        if self.current is not None:
            if self.current.t_value in t_value:
                self.next()
                return True
        return False

    # TODO fix expect_token to throw error at lineno and position
    def expect_token(self, t_type, t_value=None):
        if self.accept_token(t_type, t_value):
            return True
        raise SyntaxError(f"Unexpected token type and value, {self.current.t_type}, {self.current.t_value} at position {self.current.start},"+
                          f" expected {t_type}, {t_value}")

    # USING ACCEPT_TYPE
    def expect_type(self, t_type):
        if self.accept_type(t_type):
            return True
        raise SyntaxError(f"Unexpected token type, {self.current.t_type}, expected {t_type}")

    # USING ACCEPT_VALUE
    def expect_value(self, t_value):
        if self.accept_value(t_value):
            return True
        raise SyntaxError(f"Unexpected token type, {self.current.t_value}, expected {t_value}")

    # statements -> statement | statement NEWLINE statements
    def statements(self):
        left = self.statement()
        newline = self.current
        if self.accept_type("NEWLINE"):
            right = self.statements()
            if right is None:
                return None
            return TreeNode(newline, [left, right])
        return left

    # if_stmt:
    # | 'if' named_expression ':' block elif_stmt
    # | 'if' named_expression ':' block[else_block]
    # TODO debug if_statement
    # TODO restructure statements to block
    def if_statement(self):
        root = self.if_kwd()
        if self.accept_token("KEYWORD", "if"):
            left = self.expression()
            if self.expect_token("DELIMITER", ":") and left:
                mid = self.block()
                right = self.elif_statement()
                # if right is None:

    def if_kwd(self):
        left = self.current
        if left.t_type == "KEYWORD" and left.t_value == "if":
            self.next()
            return TreeNode(left)
        return None

    # TODO Debug elif_statement
    # elif_stmt:
    # | 'elif' named_expression ':' block elif_stmt
    # | 'elif' named_expression ':' block[else_block]
    def elif_statement(self):
        if self.accept_token("KEYWORD", "if"):
            left = self.expression()
            if self.expect_token("DELIMITER", ":"):
                mid = self.block()
                right = self.elif_statement()
                if right is None:
                    right = self.else_block()

    # else_block:
    # | 'else' ':' block
    def else_block(self):
        if self.accept_token("KEYWORD", "else") and self.expect_token("DELIMITER", ":"):
            left = self.block()
            return TreeNode(left)

    # TODO not done yet, test for bugs
    # block: NEWLINE INDENT statements DEDENT
    def block(self):
        if self.accept_token("NEWLINE") and self.expect_token("INDENT"):
            start = self.current.start
            left = self.statements()
            if self.expect_token("DEDENT"):
                if left:
                    return TreeNode(lex.Token("block", "hello", start), left)
        return None

    # function_definition -> "def" func_name '(' func_params '):' NEWLINE INDENTATION
    #                           statements
    def function_declaration(self):
        if self.accept_token("KEYWORD", "def"):
            f_name = self.identifier()
            if self.expect_token("DELIMITER", "("):
                params = self.f_params()
                if (self.expect_token("DELIMITER", ")")
                    and self.expect_token("DELIMITER", ":")
                    and self.expect_type("NEWLINE")
                    and self.expect_type("INDENT")):
                        statements = self.statements()
                        return TreeNode(f_name, [params, statements])
        return None

    # f_params -> identifier | identifier "," f_params
    def f_params(self):
        left = self.identifier()
        f_params = []
        while self.accept_token("DELIMITER", ","):
            f_param = self.identifier()
            if f_param:
                f_params.append(f_param)
        return TreeNode(left, f_params)

    # def -> DEF
    def define(self):
        left = self.current
        if left.t_type == "KEYWORD" and left.t_value == "def":
            self.next()
            return TreeNode(left)
        return None

    # ---
    # statement -> function_call | variable_assignment
    def statement(self):
        left = self.function_call()
        if left:
            return TreeNode(left)
        left = self.var_assign()
        if left:
            return TreeNode(left)

    # ---
    # variable_assignment -> identifier "=" expression
    def var_assign(self):
        left = self.identifier()
        assign = self.current
        if self.accept_token("ASSIGN", "="):
            right = self.expression()
            if right is None:
                return None
            return TreeNode(assign, [left, right])
        return None

    # identifier -> IDENTIFIER
    def identifier(self):
        left = self.current
        if left.t_type == "IDENTIFIER":
            self.next()
            return TreeNode(left)
        return None

    # functions -> function | function NEWLINE functions
    def functions(self):
        left = self.function_call()
        newline = self.current
        if self.accept_type("NEWLINE"):
            right = self.functions()
            if right is None:
                return None
            return TreeNode(newline, [left, right])
        return left

    # function_call -> keyword + "(" + function expressions + ")"
    def function_call(self):
        f_name = self.keyword()
        if self.accept_token("DELIMITER", "("):
            f_expressions = self.f_expressions()
            if self.expect_token("DELIMITER", ")"):
                if f_expressions is None:
                    return None
                return TreeNode(f_name, [f_expressions])
        return None

    # ---
    # keyword -> KEYWORD
    def keyword(self):
        left = self.current
        if left.t_type == "KEYWORD":
            self.next()
            return TreeNode(left)
        return None

    # "," removed from AST
    # function expressions -> expression "," function expressions
    def f_expressions(self):
        left = self.expression()
        f_expressions = []
        while self.accept_token("DELIMITER", ","):
            f_expression = self.f_expressions()
            if f_expression:
                f_expressions.append(f_expression)
        return TreeNode(left, f_expressions)

    # TODO remove if unused (later)
    # expressions -> expression | expression NEWLINE expressions
    def expressions(self):
        left = self.expression()
        newline = self.current
        if self.accept_type("NEWLINE"):
            right = self.expressions()
            if right is None:
                return None
            return TreeNode(newline, [left, right])
        # elif not self.accept_type("NEWLINE"):
        #     right = self.expressions()
        #     if right is None:
        #         return None
        #     return TreeNode(None, [left, right])
        return left

    # TODO fix to be able to work with variables
    # ---
    # expression -> strings | sum
    def expression(self):
        left = self.strings()
        if left:
            return TreeNode(left)
        left = self.sum()
        if left:
            return TreeNode(left)
        # left = self.current
        # if self.strings() or self.sum():
        #     return TreeNode(left)
        # return None

    # ---
    # string -> STRING
    def string(self):
        left = self.current
        if left.t_type == "STRING":
            self.next()
            return TreeNode(left)
        return None

    # ---
    # strings -> string | string "+" strings
    def strings(self):
        left = self.string()
        op = self.current
        # if self.accept_type("OPERATOR") and self.accept_value("+"):
        if self.accept_token("OPERATOR", "+"):
            right = self.strings()
            if right is None:
                return None
            return TreeNode(op, [left, right])
        return left

    # ---
    # sum -> term ("+"|"-") sum
    def sum(self):
        left = self.term()
        op = self.current
        if self.accept_value(["+", "-"]):
            right = self.sum()
            if right is None:
                return None
            return TreeNode(op, [left, right])
        return left

    # ---
    # term -> number {'*' | '**' | '/' | '%' | '+' | '-'} term
    #         | number
    def term(self):
        left = self.number()
        op = self.current
        if self.accept_value(["*", "**", "/", "%"]):
            right = self.term()
            if right is None:
                return None
            return TreeNode(op, [left, right])
        return left

    # ---
    # number -> INT | FLOAT
    def number(self):
        left = self.current
        if left.t_type in ["INT", "FLOAT"]:
            self.next()
            return TreeNode(left)
        return None

    def parse(self):
        self.AST = self.function_declaration()
        if self.AST is not None:
            return self.AST
        else:
            print("failed to parse")
            return None

# cwd = os.path.dirname(__file__)
# parentwd = os.path.split(cwd)[0]
# file_path = os.path.join(parentwd, "tests", "test_parser.py")
#
#
# with open(file_path) as data:
#     program = data.read()
#
# lexer = lex.Lexer("test_parser.py", program)
# tokens = lexer.generate_tokens()
# print(tokens)
#
# parser = Parser(tokens)
# ast = parser.parse()
# print(ast)
