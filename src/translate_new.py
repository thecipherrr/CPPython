class Translate:
    def __init__(self, ast_input, file_input):  
        self.ast_input = ast_input 
        self.file_input = file_input
        self.statement_list = []
        self.operation_list = []

    def write_header(self, out):
        out.write("#include<iostream>")
        out.write("\n")
        out.write("using namespace std;")
        out.write("\n\n")

    def write_main(self, out):
        out.write("int main(void)") 
        out.write("\n")
        out.write("{")
        out.write("\n")

    def write_print(self, out, print_args):
        # for print statements
        out.write("\tcout << " + print_args + " << endl;")

    def write_assign(self, out, var_type, var_name, var_value): 
        out.write("\t" + var_type + " " + var_name + " = " + var_value + ";")

    def write_bin_op(self, out, left, op, right):
        out.write(left, op, right)

    def write_function_declaration(self, out, func_name, func_params, func_block_list):
        out.write("void " + func_name + "(" + "auto " + func_params + ")")
        out.write("\n")
        out.write("{")
        out.write("\n")
       
        statements_in_block = []
        for op in func_block_list:
            for i in range(len(op.children)):
                if i % 2 == 0:
                    statements_in_block.append(op.children[i])
        
        for op in statements_in_block:
            if op.root == "function_call":
                f_call = op.children[0].root.root.t_value 
                f_params = op.children[1].children[0].children[0].root.t_value
                if f_call == "print":
                    self.write_print(out, f_params)
                    out.write("\n")
            elif op.root == "var_assign":
                identifier = op.children[1].root.t_value
                var_type = op.children[2].children[0].root.t_type.lower() 
                var_value = str(op.children[2].children[0].root.t_value)
                self.write_assign(out, var_type, identifier, var_value) 
                out.write("\n")
        
        out.write("}")
        out.write("\n")

    def translate(self): 
        filename = os.path.splitext(self.file_input)[0]
        filename_out = filename + ".cpp"
        out = open(filename_out, "w+")

        check_statements = self.ast_input.root
        statement = self.ast_input.children

        # populate list with children
        for i in range(len(statement)):
            if i % 2 != 0:
                self.statement_list.append(statement[i]) 
                
       
        # check for children root types
        for statement in self.statement_list:
            for i in range(len(statement.children)):
                if i % 2 == 0:
                   self.operation_list.append(statement.children[i]) 
      

        # writing the start of the program
        self.write_header(out)

        # for function declaration
        for op in self.operation_list:
            if op.root == "function_declaration":
                func_name = op.children[0].root.t_value
                func_params = op.children[1].children[0].root.t_value
                func_block_list = []
                func_block = op.children[2].children[0].children
                for i in range(len(func_block)):
                    func_block_list.append(func_block[i])
            
                # writing the function
                self.write_function_declaration(out, func_name, func_params, func_block_list)

        # writing out int main(void)
        self.write_main(out)
 
        if check_statements != "statements":
            raise SyntaxError("invalid parse")

        # main logic of program
        for op in self.operation_list:
            # checks for function call
            if op.root == "function_call":
                f_call = op.children[0].root.root.t_value
                f_params = op.children[1].children[0].children[0].root.t_value
                if f_call == "print":
                    self.write_print(out, f_params)
                    out.write("\n")
            
            # translates variable definition
            elif op.root == "var_assign":
                identifier = op.children[1].root.t_value
                var_type = op.children[2].children[0].root.t_type.lower() 
                var_value = str(op.children[2].children[0].root.t_value)
                self.write_assign(out, var_type, identifier, var_value) 
                out.write("\n") 


        out.write("\treturn 0;")
        out.write("\n") 
        out.write("}")
        out.write("\n")
        out.close()
