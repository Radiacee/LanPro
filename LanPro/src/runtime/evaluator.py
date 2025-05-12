class Evaluator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.functions = {}  # Store user-defined functions

    def evaluate(self, node):
        if isinstance(node, int):  # Handle integer literals
            return node
        elif isinstance(node, str):  # Handle variable names
            return self.memory_manager.get(node)
        elif isinstance(node, dict):  # Handle AST nodes
            if node['type'] == 'Literal':  # Handle Literal nodes
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
            elif node['type'] == 'FunctionDeclaration':
                self.functions[node['name']] = {
                    'parameters': node['parameters'],
                    'body': node['body']
                }
            elif node['type'] == 'ReturnStatement':  # Handle ReturnStatement nodes
                return self.evaluate(node['value'])
            elif node['type'] == 'Block':
                for statement in node['body']:
                    result = self.evaluate(statement)
                    if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                        return result  # Propagate return value
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
        elif function_name in self.functions:
            # Get the function definition
            function = self.functions[function_name]
            parameters = function['parameters']
            body = function['body']

            # Check if the number of arguments matches the number of parameters
            if len(arguments) != len(parameters):
                raise ValueError(f"Function '{function_name}' expects {len(parameters)} arguments, but got {len(arguments)}.")

            # Temporarily allocate arguments to parameters
            original_variables = self.memory_manager.variables.copy()  # Use 'variables' instead of 'memory'
            for param, arg in zip(parameters, arguments):
                self.memory_manager.allocate(param, self.evaluate(arg))

            # Evaluate the function body
            result = None
            for statement in body['body']:
                result = self.evaluate(statement)

            # Restore original variables
            self.memory_manager.variables = original_variables  # Use 'variables' instead of 'memory'

            return result
        else:
            raise ValueError(f"Unknown function: {function_name}")

    def run(self, program):
        for mentstatement in program['body']:
            self.evaluate(statement)