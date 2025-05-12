# filepath: LanPro/LanPro/src/semantic/semantic_analyzer.py

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.current_scope = {}

    def enter_scope(self):
        self.current_scope = {}

    def exit_scope(self):
        self.symbol_table.update(self.current_scope)
        self.current_scope = {}

    def define_variable(self, name, var_type):
        if name in self.current_scope:
            raise Exception(f"Variable '{name}' already defined in the current scope.")
        self.current_scope[name] = var_type

    def lookup_variable(self, name):
        if name in self.current_scope:
            return self.current_scope[name]
        elif name in self.symbol_table:
            return self.symbol_table[name]
        else:
            raise Exception(f"Undefined variable '{name}'.")

    def check_type(self, var_name, expected_type):
        actual_type = self.lookup_variable(var_name)
        if actual_type != expected_type:
            raise Exception(f"Type mismatch: expected '{expected_type}', but got '{actual_type}'.")

    def analyze(self, ast):
        # Implement AST traversal and semantic checks here
        pass

    def report_errors(self):
        # Implement error reporting for semantic issues
        pass