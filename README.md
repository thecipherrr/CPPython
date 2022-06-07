# Transcompiler from Python to C++ (kinda like Cython but not)

## PROGRESS SO FAR
## 1. Lexer:
- [x] Basic operators and delimiters
- [x] String literals
- [x] Numeric tokens 
- [x] Reserved keywords and identifiers
- [x] Error class
- [x] Implement indentation token lexing
- [ ] Implemented more reserved keywords 


## 2. Parser:
- [x] Implementing regular grammar (still limited cases)
- [x] Generating basic AST using recursive descent
- [x] Grammar for numeric expression
- [x] Grammar for statements
- [ ] Grammar for function definition
- [x] Grammar for function call
- [x] Grammar for string
- [ ] Grammar for if else

## 3. Translator (Generate C++ code)
- [ ] Translating a simple print statement
- [ ] Translating simple arithmetic operations
- [ ] Translating conditionals, for loops, and while loops
- [ ] Translating a simple Python function

## THINGS TO FIX
- [ ] Python function AST generation

## Source:
### 1. How a Programming Language Works:
http://www2.hawaii.edu/~takebaya/ics111/process_of_programming/process_of_programming.html 
### 2. How A Compiler Works:
https://www.baeldung.com/cs/how-compilers-work1
### 3. How Transcompiler Works:
TBD

## WORK IN PROGRESS, NOT FINISHED YET!!
