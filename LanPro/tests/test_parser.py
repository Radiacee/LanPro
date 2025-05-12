import unittest
from src.parser.syntax_analyzer import Parser
from src.lexer.tokenizer import Tokenizer

class TestParser(unittest.TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()
        self.parser = Parser()

    def test_valid_syntax(self):
        code = "let x = 5;"
        tokens = self.tokenizer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.assertIsNotNone(ast)

    def test_invalid_syntax(self):
        code = "let x = ;"
        tokens = self.tokenizer.tokenize(code)
        with self.assertRaises(SyntaxError):
            self.parser.parse(tokens)

    def test_ast_generation(self):
        code = "let x = 5; let y = x + 2;"
        tokens = self.tokenizer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.assertEqual(ast.root.value, 'let')

    def test_nested_statements(self):
        code = "if (x > 0) { let y = x; }"
        tokens = self.tokenizer.tokenize(code)
        ast = self.parser.parse(tokens)
        self.assertIsNotNone(ast)

    def test_error_handling(self):
        code = "let x = 5 let y = 10;"
        tokens = self.tokenizer.tokenize(code)
        with self.assertRaises(SyntaxError):
            self.parser.parse(tokens)

if __name__ == '__main__':
    unittest.main()