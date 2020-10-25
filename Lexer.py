import re
import functional
from Token import Token


class Lexer:
    """Лексер для языка Python"""

    def __init__(self):
        self.text = ""
        self.pos_space = 0
        self.num_line = 0
        self.num_token = 0
        self.lines = list()
        self.patterns = [r"^[0-9]+\.[0-9]*$", r"^[0-9]+$", r"^[A-Za-z_][A-Za-z0-9_]*$", r"^[\"\"].*[\"\"]$",
                         r"^0x[A-Fa-f0-9]+$", r"^0o[0-7]+$", r"^0b[0-1]+$"]
        self.template_tokens = {
            "if": "Keyword_IF",
            "else": "Keyword_ELSE",
            "elif": "Keyword_ELIF",
            "for": "Keyword_FOR",
            "while": "Keyword_WHILE",
            "try": "Keyword_TRY",
            "except": "Keyword_EXCEPT",
            "as": "Keyword_AS",
            "pass": "Keyword_PASS",
            "in": "Keyword_IN",
            "return": "Keyword_RETURN",
            "break": "Keyword_BREAK",
            "continue": "Keyword_CONTINUE",
            "or": "Keyword_OR",
            "and": "Keyword_AND",
            "not": "Keyword_NOT",
            "None": "Keyword_NONE",
            ";": "Semicolon",
            ".": "Point",
            ",": "Comma",
            "+": "Plus",
            "-": "Minus",
            "*": "Multiplication",
            "**": "Exponentiation",
            "/": "Division",
            "//": "Integer_Division",
            "%": "Residual_Division",
            "=": "Assignment",
            "+=": "Plus_Assignment",
            "-=": "Minus_Assignment",
            "*=": "Multi_Assignment",
            "/=": "Div_Assignment",
            "//=": "Int_Div_Assignment",
            "%=": "Residual_Assignment",
            "**=": "Exp_Assignment",
            "==": "Comparison",
            ":": "Colon",
            "!": "Exclamation_Mark",
            "(": "L_Paren_Bracket",
            ")": "R_Paren_Bracket",
            "[": "L_Sq_Bracket",
            "]": "R_Sq_Bracket",
            "{": "L_Brace",
            "}": "R_Brace",
            "is": "Keyword_IS",
            "\t": "Tabulation",
            ">": "More",
            "<": "Less",
            "import": "Keyword_IMPORT",
            "from": "Keyword_FROM",
            "def": "Keyword_DEF",
            "\\": "Carryover",
            "\n": "\\n",
            "!=": "Not_Comparison",
            ">=": "More_Comparison",
            "<=": "Less_Comparison"
        }

    def readFile(self, filename):
        try:
            with open(filename) as file_object:
                self.text = file_object.read()
        except FileNotFoundError:
            return None
        else:
            return True

    def conversionText(self):  # "[,.]+-/{}|*^$!~&()%|?=<>!;"
        """ Форматирование текста для лексера """
        symbols = [["+=", "-=", "*=", "/=", "//=", "%=", "**=", "<=", ">=", "!=", "[", ",", "]", "+", "-", "//", "{", "}", "**", "*", "^", "!", "==", "=", "<", ">", ":", "\t",
                    "(", ")", "/", "\n"],
                   [" += ", " -= ", " *= ", " /= ", " //= ", " %= ", " **= ", " <= ", " >= ", " != ", " [ ", " , ", " ] ", " + ", " - ", " // ", " { ", " } ", " ** ", " * ",  " ^ ", " ! ",  " == ",
                    " = ", " < ", " > ", " : ", " \t ", " ( ", " ) ", " / ", " \n "]]

        """ Нахождение и удаление комментариев """
        temp = ""
        is_comment = 0
        for i in range(len(self.text)):
            if self.text[i] == "#":
                is_comment = 1
            elif self.text[i] == "\n" and is_comment == 1:
                is_comment = 0
                temp += self.text[i]
            elif is_comment == 0:
                temp += self.text[i]
        self.text = temp

        """ Нахождение и удаление многострочных комментариев """
        temp = ""
        is_ml_comment = 0
        i = 0
        while i < len(self.text):
            if self.text[i: i+3] == "\"\"\"":
                is_ml_comment = 1 if is_ml_comment == 0 else 0
                i += 3
            if self.text[i] == "\n":
                temp += self.text[i]
            elif is_ml_comment == 0:
                temp += self.text[i]
            i += 1
        self.text = temp

        """ Нахождение и обработка строк """
        temp = ""
        is_string = 0
        j = 0
        while j < len(self.text):
            if self.text[j] == "\"":
                is_string = 1 if is_string == 0 else 0
            i = 0
            while i < len(symbols[0]):
                if self.text[j:j+len(symbols[0][i])] == symbols[0][i] and is_string == 0:
                    temp += symbols[1][i]
                    j += len(symbols[0][i]) - 1
                    break
                i += 1
            if self.text[j] == "\n":
                is_string = 0
            if i == len(symbols[0]):
                temp += self.text[j]
            j += 1

        """ Определение числа с точкой и методов классов """
        self.text = temp
        temp = ""
        for i in range(len(self.text)):
            if self.text[i] == "." and not re.findall(self.patterns[0], self.text[i-1:i+2]):
                temp += " " + self.text[i] + " "
            else:
                temp += self.text[i]

        self.text = temp
        self.text = self.text.replace("    ", " \t ")

        self.text = functional.del_duplic_chars(self.text, " ")
        # self.text = self.text.replace(" \n", "\n")

    def lexer(self):
        """ Лексер """
        i = self.pos_space
        len_str = len(self.text)
        if self.pos_space == len_str:
            return None
        str_token = ""

        is_string = 0
        while i < len_str-1:
            if self.text[i] == "\"":
                is_string = 1 if is_string == 0 else 0
            # if not is_string and (self.text[i] == " " or self.text[i] == "\n"):
            if not is_string and (self.text[i] == " "):
                break
            elif is_string and self.text[i] == "\n":
                is_string = 0
                break
            str_token += self.text[i]
            i += 1

        self.pos_space = i + 1
        self.num_token += 1
        discription_token = self.template_tokens.setdefault(str_token)
        if discription_token is None:
            if re.findall(self.patterns[0], str_token):
                discription_token = "Real_Num"
            elif re.findall(self.patterns[1], str_token):
                discription_token = "Num"
            elif re.findall(self.patterns[2], str_token):
                discription_token = "Id"
            elif re.findall(self.patterns[3], str_token):
                discription_token = "String"
                str_token = str_token[1: -1]
            elif re.findall(self.patterns[4], str_token):
                discription_token = "Num_Hex"
            elif re.findall(self.patterns[5], str_token):
                discription_token = "Num_Oct"
            elif re.findall(self.patterns[6], str_token):
                discription_token = "Num_Bin"
            else:
                discription_token = "Unknown"
                print("Встречен неизвестный токен в строке " + str(self.num_line + 1))
                exit(0)
        struct_output = Token(discription_token, str_token, self.num_line + 1, self.num_token)
        # if self.text[i] == "\n":
        if str_token == "\n":
            self.num_line += 1
            self.num_token = 0
        return struct_output
