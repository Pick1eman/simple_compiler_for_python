from Lexer import Lexer
from Parser import Parser
import AST
from Token import Token
import re
import os
import sys


if __name__ == "__main__":
    if sys.argv[0] != "./main.py":
        print("Для запуска компилятора, зайдите в корень проекта и введите ./main.py")
    elif len(sys.argv) == 3:
        if sys.argv[1] == "--dump-tokens":
            program = Lexer()
            program.readFile(sys.argv[2])
            program.conversionText()
            lexeme_struct = None
            while True:
                lexeme_struct = program.lexer()
                if lexeme_struct is not None:
                    lexeme = None
                    if lexeme_struct.lexeme == "\n":
                        lexeme = "\\n"
                    elif lexeme_struct.lexeme == "\t":
                        lexeme = "\\t"
                    else:
                        lexeme = lexeme_struct.lexeme
                    print("<" + str(lexeme_struct.line) + "; " + str(lexeme_struct.token_id) + ">  " + lexeme + "\t" + lexeme_struct.token_class)
                else:
                    break
        elif sys.argv[1] == "--dump-ast":
            program = Parser(sys.argv[2])
            program.create_AST()
            program.print_AST()
        elif sys.argv[1] == "--dump-asm":
            program = Parser(sys.argv[2])
            program.create_AST()
            program.symbols_table()
            print(AST.code_assembler)
        else:
            print("Неверный ключ. Шаблон запуска <путь_к_main.py> <Ключ> <Файл_для_компиляции>")
    elif 2 > len(sys.argv) > 3:
        print("Неверное количество аргументов. Шаблон запуска <путь_к_main.py> <Ключ> <Файл_для_компиляции>")
    elif len(sys.argv) == 2 and not os.path.exists(sys.argv[1]):
        print("По данному пути отсутствует файл для компиляции")
    else:
        program = Parser(sys.argv[1])
        program.create_AST()
        program.symbols_table()
        output_filename = sys.argv[1].split(".")
        output_filename = output_filename[1].split("/")
        exe_file = output_filename[-1]
        output_filename = exe_file + ".s"
        os.system("mkdir -p compiled_asm")
        os.system("mkdir -p executable")
        with open("./compiled_asm/" + output_filename, "w") as file:
            file.write(AST.code_assembler)
            file.close()
        os.system("gcc -Wall -no-pie ./compiled_asm/" + output_filename + " -o ./executable/" + output_filename[:-2])


