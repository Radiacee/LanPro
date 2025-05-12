import unittest
from src.semantic.semantic_analyzer import SemanticAnalyzer

class TestSemanticAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SemanticAnalyzer()

    def test_variable_declaration(self):
        self.analyzer.declare_variable('x', 'int')
        self.assertIn('x', self.analyzer.symbol_table)
        self.assertEqual(self.analyzer.symbol_table['x'], 'int')

    def test_type_checking(self):
        self.analyzer.declare_variable('y', 'float')
        self.analyzer.assign_variable('y', 3.14)
        with self.assertRaises(TypeError):
            self.analyzer.assign_variable('y', 'string')

    def test_undefined_variable(self):
        with self.assertRaises(NameError):
            self.analyzer.assign_variable('undefined_var', 10)

    def test_scope_management(self):
        self.analyzer.enter_scope()
        self.analyzer.declare_variable('a', 'int')
        self.analyzer.exit_scope()
        with self.assertRaises(NameError):
            self.analyzer.assign_variable('a', 5)

    def test_function_declaration(self):
        self.analyzer.declare_function('my_func', ['arg1', 'arg2'], 'int')
        self.assertIn('my_func', self.analyzer.function_table)

    def test_function_call(self):
        self.analyzer.declare_function('add', ['a', 'b'], 'int')
        self.analyzer.declare_variable('result', 'int')
        self.analyzer.call_function('add', [1, 2])
        self.assertEqual(self.analyzer.symbol_table['result'], 3)

if __name__ == '__main__':
    unittest.main()