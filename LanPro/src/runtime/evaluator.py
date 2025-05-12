class Evaluator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.functions = {}

    def evaluate(self, node):
        if isinstance(node, int):
            return node
        elif isinstance(node, str):
            return self.memory_manager.get(node)
        elif isinstance(node, dict):
            node_type = node.get('type')
            line = node.get('line')

            if node_type == 'Literal':
                value = node['value']
                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                    return value[1:-1]
                return value
            elif node_type == 'Identifier':
                return self.memory_manager.get(node['name'])
            elif node_type == 'NULL':
                return None
            elif node_type == 'BinaryOperation':
                left = self.evaluate(node['left'])
                right = self.evaluate(node['right'])
                operator = node['operator']
                if operator == '+':
                    if isinstance(left, str) and isinstance(right, str):
                        return str(left) + str(right)
                    elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        return left + right
                    else:
                        raise ValueError(f"Type mismatch: Cannot add {type(left).__name__} and {type(right).__name__} at line {line}")
                elif operator == '-':
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        return left - right
                    raise ValueError(f"Type mismatch: Cannot subtract {type(right).__name__} from {type(left).__name__} at line {line}")
                elif operator == '*':
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        return left * right
                    raise ValueError(f"Type mismatch: Cannot multiply {type(left).__name__} and {type(right).__name__} at line {line}")
                elif operator == '/':
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)) and right != 0:
                        return left / right
                    raise ValueError(f"Type mismatch or division by zero: Cannot divide {type(left).__name__} by {type(right).__name__} at line {line}")
                elif operator in ['<', '>', '<=', '>=', '==', '!=']:
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        return {
                            '<': lambda x, y: x < y,
                            '>': lambda x, y: x > y,
                            '<=': lambda x, y: x <= y,
                            '>=': lambda x, y: x >= y,
                            '==': lambda x, y: x == y,
                            '!=': lambda x, y: x != y
                        }[operator](left, right)
                    raise ValueError(f"Type mismatch: Cannot compare {type(left).__name__} and {type(right).__name__} at line {line}")
                else:
                    raise ValueError(f"Unknown operator: {operator} at line {line}")
            elif node_type == 'AssignmentStatement':
                value = self.evaluate(node['value'])
                if value is None:
                    if self.memory_manager.exists(node['identifier']):
                        self.memory_manager.update(node['identifier'], None)
                    else:
                        self.memory_manager.allocate(node['identifier'], None)
                else:
                    self.memory_manager.allocate(node['identifier'], value)
            elif node_type == 'FunctionCall':
                return self.evaluate_function(node['name'], node['arguments'], line)
            elif node_type == 'FunctionDeclaration':
                self.functions[node['name']] = {
                    'parameters': node['parameters'],
                    'body': node['body']
                }
            elif node_type == 'ReturnStatement':
                return self.evaluate(node['value'])
            elif node_type == 'Block':
                for statement in node['body']:
                    result = self.evaluate(statement)
                    if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                        return result
            else:
                return self.evaluate_control_structure(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)} at line {line}")

    def evaluate_control_structure(self, node):
        node_type = node.get('type')
        line = node.get('line')
        if node_type == 'IfStatement':
            condition = self.evaluate(node['condition'])
            if condition:
                return self.evaluate(node['thenBranch'])
            elif node['elseBranch'] is not None:
                return self.evaluate(node['elseBranch'])
        elif node_type == 'WhileStatement':
            while self.evaluate(node['condition']):
                self.evaluate(node['body'])
        elif node_type == 'ForStatement':
            iterable = self.evaluate(node['iterable'])
            for value in iterable:
                self.memory_manager.allocate(node['identifier'], value)
                self.evaluate(node['body'])
        else:
            raise ValueError(f"Unknown control structure type: {node_type} at line {line}")

    def evaluate_function(self, function_name, arguments, line):
        if function_name == "print":
            evaluated_args = [self.evaluate(arg) for arg in arguments]
            print(*evaluated_args)
        elif function_name == "input":
            if not arguments:
                return input()
            raise ValueError(f"input() function does not accept arguments at line {line}")
        elif function_name == "free":
            if len(arguments) != 1 or not isinstance(arguments[0], dict) or arguments[0]['type'] != 'Identifier':
                raise ValueError(f"free() expects a single variable name as argument at line {line}")
            var_name = arguments[0]['name']
            self.memory_manager.deallocate(var_name)
        elif function_name in self.functions:
            function = self.functions[function_name]
            parameters = function['parameters']
            body = function['body']

            if len(arguments) != len(parameters):
                raise ValueError(f"Function '{function_name}' expects {len(parameters)} arguments, but got {len(arguments)} at line {line}")

            original_variables = self.memory_manager.variables.copy()
            for param, arg in zip(parameters, arguments):
                self.memory_manager.allocate(param, self.evaluate(arg))

            result = None
            for statement in body['body']:
                result = self.evaluate(statement)

            self.memory_manager.variables = original_variables
            return result
        else:
            raise ValueError(f"Unknown function: {function_name} at line {line}")

    def run(self, program):
        for statement in program['body']:
            self.evaluate(statement)
            self.memory_manager.run_gc()