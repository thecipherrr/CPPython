# Cppython
**PROJECT IS PARTIALLY FINISHED BUT UPDATES MAY STILL COME, USE AT YOUR OWN RISK!!!**

Cppython is a Python to C++ [Transcompiler](https://en.wikipedia.org/wiki/Source-to-source_compiler) that can translate and compile source codes from [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) to [C++](https://en.wikipedia.org/wiki/C%2B%2B)
*(This project requires gcc to compile the translated C++ code in to an executable)*

## Quick Start
```console
$ git clone https://github.com/EdwardMatthew/CPPython.git
```

## How to Use the Program
To translate a Python source code to C++
```console
$ python cppython.py translate <FILE_PATH>
```

To compile a Python or an existing C++ code into an executable
```console
$ python cppython.py compile <FILE_PATH> 
```

## Examples
Hello, World:
1. Make a "Hello, World" program in Python named hello.py:
2. To translate program:
```console
$ python cppython translate hello.py 
```
3. To compile program:
```console
$ python cppython compile hello.py
```
4. Screenshots:
![alt text](https://github.com/EdwardMatthew/CPPython/blob/main/images/HelloWorld.jpg)

## FEATURES SO FAR
## 1. Lexer:
- [x] Basic operators and delimiters
- [x] String literals
- [x] Numeric tokens 
- [x] Reserved keywords and identifiers
- [x] Error class
- [x] Implement indentation token lexing
- [ ] Implemented more reserved keywords (needed more keywords in the future)

## 2. Parser:
- [x] Implementing regular grammar (still limited cases)
- [x] Generating basic AST using recursive descent
- [x] Grammar for numeric expression
- [x] Grammar for statements
- [x] Grammar for function definition
- [x] Grammar for function call
- [x] Grammar for string
- [x] Grammar for if else

## 3. Translator (Generate C++ code)
- [x] Translating a simple print statement
- [x] Translating simple arithmetic operations
- [ ] Translating conditionals, for loops, and while loops
- [x] Translating a simple Python function

## THINGS TO FIX
- [x] Python function AST generation

## Source:
### 1. How a Programming Language Works:
http://www2.hawaii.edu/~takebaya/ics111/process_of_programming/process_of_programming.html 
### 2. How A Compiler Works:
https://www.baeldung.com/cs/how-compilers-work1
### 3. How A Transcompiler Works:
https://en.wikipedia.org/wiki/Source-to-source_compiler
