import unittest
from src.lexer.tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = Tokenizer()

    def test_valid_tokens(self):
        valid_code = "let x = 10; if (x > 5) { x = x + 1; }"
        tokens = self.tokenizer.tokenize(valid_code)
        expected_tokens = [
            ('LET', 'let'),
            ('IDENTIFIER', 'x'),
            ('ASSIGN', '='),
            ('NUMBER', '10'),
            ('IF', 'if'),
            ('LPAREN', '('),
            ('IDENTIFIER', 'x'),
            ('GT', '>'),
            ('NUMBER', '5'),
            ('RPAREN', ')'),
            ('LBRACE', '{'),
            ('IDENTIFIER', 'x'),
            ('ASSIGN', '='),
            ('IDENTIFIER', 'x'),
            ('PLUS', '+'),
            ('NUMBER', '1'),
            ('SEMICOLON', ';'),
            ('RBRACE', '}'),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_invalid_token(self):
        invalid_code = "let x = @;"
        with self.assertRaises(ValueError) as context:
            self.tokenizer.tokenize(invalid_code)
        self.assertEqual(str(context.exception), "Invalid token: '@'")

    def test_skip_comments(self):
        code_with_comments = "let x = 10; // This is a comment\nlet y = 20;"
        tokens = self.tokenizer.tokenize(code_with_comments)
        expected_tokens = [
            ('LET', 'let'),
            ('IDENTIFIER', 'x'),
            ('ASSIGN', '='),
            ('NUMBER', '10'),
            ('SEMICOLON', ';'),
            ('LET', 'let'),
            ('IDENTIFIER', 'y'),
            ('ASSIGN', '='),
            ('NUMBER', '20'),
            ('SEMICOLON', ';'),
        ]
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()