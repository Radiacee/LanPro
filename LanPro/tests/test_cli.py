import unittest
from src.cli.repl import LanProREPL

class TestLanProCLI(unittest.TestCase):

    def setUp(self):
        self.repl = LanProREPL()

    def test_basic_command(self):
        result = self.repl.evaluate("print('Hello, LanPro!')")
        self.assertEqual(result, "Hello, LanPro!")

    def test_invalid_command(self):
        with self.assertRaises(SyntaxError):
            self.repl.evaluate("print('Hello, LanPro!')")  # Missing closing parenthesis

    def test_variable_assignment(self):
        self.repl.evaluate("x = 10")
        result = self.repl.evaluate("x")
        self.assertEqual(result, 10)

    def test_undefined_variable(self):
        with self.assertRaises(NameError):
            self.repl.evaluate("y")  # y is not defined

    def test_control_structure(self):
        result = self.repl.evaluate("if 1 < 2: 'True'")
        self.assertEqual(result, 'True')

    def test_function_definition_and_call(self):
        self.repl.evaluate("def add(a, b): return a + b")
        result = self.repl.evaluate("add(2, 3)")
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()