import unittest
from src.runtime.evaluator import Evaluator
from src.runtime.memory_manager import MemoryManager

class TestRuntime(unittest.TestCase):

    def setUp(self):
        self.evaluator = Evaluator()
        self.memory_manager = MemoryManager()

    def test_expression_evaluation(self):
        self.assertEqual(self.evaluator.evaluate_expression("3 + 4"), 7)
        self.assertEqual(self.evaluator.evaluate_expression("10 - 2 * 3"), 4)
        self.assertEqual(self.evaluator.evaluate_expression("(1 + 2) * 3"), 9)

    def test_control_structures(self):
        self.assertEqual(self.evaluator.evaluate_if_statement("if (3 > 2) { return 1; } else { return 0; }"), 1)
        self.assertEqual(self.evaluator.evaluate_while_loop("while (i < 5) { i = i + 1; }", initial_i=0), 5)

    def test_function_execution(self):
        self.evaluator.execute_function("def add(a, b) { return a + b; }")
        result = self.evaluator.call_function("add", [5, 7])
        self.assertEqual(result, 12)

    def test_variable_lifecycle(self):
        self.memory_manager.initialize_variable("x", 10)
        self.assertEqual(self.memory_manager.get_variable("x"), 10)
        self.memory_manager.update_variable("x", 20)
        self.assertEqual(self.memory_manager.get_variable("x"), 20)
        self.memory_manager.delete_variable("x")
        with self.assertRaises(KeyError):
            self.memory_manager.get_variable("x")

if __name__ == '__main__':
    unittest.main()