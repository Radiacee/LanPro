class Evaluator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager

    def evaluate(self, node):
        if isinstance(node, int):  # Assuming node is an integer expression
            return node
        elif isinstance(node, str):  # Assuming node is a variable name
            return self.memory_manager.get(node)  # Use `get` to retrieve variable value
        elif isinstance(node, dict):  # Assuming node is a control structure or function call
            if node['type'] == 'Literal':  # Handle Literal nodes
                return node['value']
            elif node['type'] == 'Identifier':  # Handle Identifier nodes
                return self.memory_manager.get(node['name'])  # Retrieve the variable's value
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
                elif operator == '<':  # Handle comparison operators
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
                self.memory_manager.allocate(node['identifier'], self.evaluate(node['value']))  # Use `allocate`
            elif node['type'] == 'FunctionCall':
                return self.evaluate_function(node['name'], node['arguments'])  # Handle function calls
            else:
                return self.evaluate_control_structure(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)}")

    def evaluate_control_structure(self, node):
        if node['type'] == 'if':
            condition = self.evaluate(node['condition'])
            if condition:
                return self.evaluate(node['thenBranch'])
            elif 'elseBranch' in node:
                return self.evaluate(node['elseBranch'])
        elif node['type'] == 'while':
            while self.evaluate(node['condition']):
                self.evaluate(node['body'])
        elif node['type'] == 'for':
            for var in node['iterator']:
                self.memory_manager.allocate(node['variable'], var)  # Use `allocate` for loop variables
                self.evaluate(node['body'])
        else:
            raise ValueError(f"Unknown control structure type: {node['type']}")

    def evaluate_function(self, function_name, arguments):
        if function_name == "print":
            # Evaluate all arguments and print them
            evaluated_args = [self.evaluate(arg) for arg in arguments]
            print(*evaluated_args)
        else:
            raise ValueError(f"Unknown function: {function_name}")

    def run(self, program):
        for statement in program['body']:
            self.evaluate(statement)