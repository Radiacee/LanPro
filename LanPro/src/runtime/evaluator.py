class Evaluator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager

    def evaluate(self, node):
        if isinstance(node, int):  # Handle integer literals
            return node
        elif isinstance(node, str):  # Handle variable names
            return self.memory_manager.get(node)
        elif isinstance(node, dict):  # Handle AST nodes
            if node['type'] == 'Literal':  # Handle Literal nodes
                # Convert string literals to their actual value if needed
                value = node['value']
                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                    return value[1:-1]  # Strip quotes from string literals
                return value
            elif node['type'] == 'Identifier':  # Handle Identifier nodes
                return self.memory_manager.get(node['name'])
            elif node['type'] == 'BinaryOperation':  # Handle BinaryOperation nodes
                left = self.evaluate(node['left'])
                right = self.evaluate(node['right'])
                operator = node['operator']
                if operator == '+':
                    return left + right
                elif operator == '-':
                    return left - right
                elif operator == '*':
                    return left * right
                elif operator == '/':
                    return left / right
                elif operator == '<':
                    return left < right
                elif operator == '>':
                    return left > right
                elif operator == '<=':
                    return left <= right
                elif operator == '>=':
                    return left >= right
                elif operator == '==':
                    return left == right
                elif operator == '!=':
                    return left != right
                else:
                    raise ValueError(f"Unknown operator: {operator}")
            elif node['type'] == 'AssignmentStatement':
                self.memory_manager.allocate(node['identifier'], self.evaluate(node['value']))
            elif node['type'] == 'FunctionCall':
                return self.evaluate_function(node['name'], node['arguments'])
            elif node['type'] == 'Block':
                for statement in node['body']:
                    self.evaluate(statement)
            else:
                return self.evaluate_control_structure(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def evaluate_control_structure(self, node):
        if node['type'] == 'IfStatement':
            condition = self.evaluate(node['condition'])
            if condition:
                return self.evaluate(node['thenBranch'])
            elif node['elseBranch'] is not None:
                return self.evaluate(node['elseBranch'])
        elif node['type'] == 'WhileStatement':
            while self.evaluate(node['condition']):
                self.evaluate(node['body'])
        elif node['type'] == 'ForStatement':
            iterable = self.evaluate(node['iterable'])
            for value in iterable:
                self.memory_manager.allocate(node['identifier'], value)
                self.evaluate(node['body'])
        else:
            raise ValueError(f"Unknown control structure type: {node['type']}")

    def evaluate_function(self, function_name, arguments):
        if function_name == "print":
            evaluated_args = [self.evaluate(arg) for arg in arguments]
            print(*evaluated_args)
        else:
            raise ValueError(f"Unknown function: {function_name}")

    def run(self, program):
        for statement in program['body']:
            self.evaluate(statement)