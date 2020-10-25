import unittest
from Lexer import Lexer
from Token import Token
from Parser import Parser
import AST


class Tests(unittest.TestCase):
    """Тесты для компилятора"""

    def test_lexer1(self):
        text = Lexer()
        text.text = "while b < 4:"
        result = text.lexer()
        result_str = result.token_class + " " + result.lexeme + " " + str(result.line) + " " + str(result.token_id)
        template = Token("Keyword_WHILE", "while", 1, 1)
        template_str = template.token_class + " " + template.lexeme + " " + str(template.line) + " " + \
                       str(template.token_id)
        self.assertEqual(result_str, template_str)

    def test_lexer2(self):
        text = Lexer()
        text.text = "_b  =5"
        template = Token("Id", "_b", 1, 1)
        template_str = template.token_class + " " + template.lexeme + " " + str(template.line) + " " + \
                       str(template.token_id)
        result = text.lexer()
        result_str = result.token_class + " " + result.lexeme + " " + str(result.line) + " " + str(result.token_id)
        self.assertEqual(result_str, template_str)

    def test_parser(self):
        filename = "resources/temp.py"
        text = "a = 0\n" \
               "b = f(-3, 3)\n" \
               "if a > b:\n" \
               "\tprint(\"a > b\")\n" \
               "else:\n" \
               "\tc = a**b\n"
        with open(filename, "w") as file:
            file.write(text)
            file.close()
        parser = Parser(filename)
        parser.create_AST()
        expect = 3
        self.assertEqual(expect, parser.root.nodes[1].second.first[1].value)
        expect = "print"
        self.assertEqual(expect, parser.root.nodes[2].body.nodes[0].name)

    def test_parser2(self):
        filename = "resources/temp.py"
        text = "a = 0\n" \
               "b = f(-3, 3)\n" \
               "if a > b:\n" \
               "\tprint(\"a > b\")\n" \
               "else:\n" \
               "\tc = a**b\n"
        with open(filename, "w") as file:
            file.write(text)
            file.close()
        parser = Parser(filename)
        parser.create_AST()
        expect = "+"
        self.assertIsNot(expect, parser.root.nodes[1].second.first[0].operation)

    def test_sema(self):
        filename = "resources/temp.py"
        text = "a = 0\n" \
               "b = 5\n" \
               "if a > b:\n" \
               "\tprint(\"a + b\")\n" \
               "else:\n" \
               "\tc = a**b\n"
        with open(filename, "w") as file:
            file.write(text)
            file.close()
        parser = Parser(filename)
        parser.create_AST()
        expect = False
        self.assertEqual(expect, parser.symbols_table())


unittest.main()
