import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor, Future

class Evaluator:
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager
        self.functions = {}
        self.verbose = False
        self.debug = False
        self.thread_pool = ThreadPoolExecutor(max_workers=10)  # Limit concurrent threads

    def set_verbose(self, verbose):
        self.verbose = verbose

    def set_debug(self, debug):
        self.debug = debug
        console.print(f"[bold yellow]Evaluator Debug Mode Set To: {self.debug}[/bold yellow]")

    def evaluate(self, node):
        if self.verbose and isinstance(node, dict):
            console.print(f"[magenta]Evaluating node: {node}[/magenta]")

        if isinstance(node, int):
            if self.verbose:
                console.print(f"[magenta]Evaluated to integer: {node}[/magenta]")
            return node
        elif isinstance(node, str):
            value = self.memory_manager.get(node)
            if self.verbose:
                console.print(f"[magenta]Evaluated identifier '{node}' to: {value}[/magenta]")
            return value
        elif isinstance(node, dict):
            node_type = node.get('type')
            line = node.get('line')

            if node_type == 'Literal':
                value = node['value']
                if isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                    result = value[1:-1]  # Strip quotes from string literals
                else:
                    result = value
                if self.verbose:
                    console.print(f"[magenta]Evaluated Literal to: {result}[/magenta]")
                return result
            elif node_type == 'Identifier':
                result = self.memory_manager.get(node['name'])
                if self.verbose:
                    console.print(f"[magenta]Evaluated Identifier '{node['name']}' to: {result}[/magenta]")
                return result
            elif node_type == 'NULL':
                if self.verbose:
                    console.print("[magenta]Evaluated NULL to: None[/magenta]")
                return None
            elif node_type == 'BinaryOperation':
                if self.verbose:
                    console.print(f"[magenta]Evaluating BinaryOperation: {node['operator']}[/magenta]")
                left = self.evaluate(node['left'])
                right = self.evaluate(node['right'])
                operator = node['operator']
                if operator == '+':
                    if isinstance(left, str) or isinstance(right, str):
                        result = str(left) + str(right)  # Adjusted to match current behavior
                    elif isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        result = left + right
                    else:
                        raise ValueError(f"Type mismatch: Cannot add {type(left).__name__} and {type(right).__name__} at line {line}")
                elif operator == '-':
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        result = left - right
                    else:
                        raise ValueError(f"Type mismatch: Cannot subtract {type(right).__name__} from {type(left).__name__} at line {line}")
                elif operator == '*':
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        result = left * right
                    else:
                        raise ValueError(f"Type mismatch: Cannot multiply {type(left).__name__} and {type(right).__name__} at line {line}")
                elif operator == '/':
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        if right == 0:
                            raise ValueError(f"Division by zero error for operation '{left} / {right}' at line {line}, where left = {left}")
                        result = left / right
                    else:
                        raise ValueError(f"Type mismatch or division by zero: Cannot divide {type(left).__name__} by {type(right).__name__} at line {line}")
                elif operator in ['<', '>', '<=', '>=', '==', '!=']:
                    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                        result = {
                            '<': lambda x, y: x < y,
                            '>': lambda x, y: x > y,
                            '<=': lambda x, y: x <= y,
                            '>=': lambda x, y: x >= y,
                            '==': lambda x, y: x == y,
                            '!=': lambda x, y: x != y
                        }[operator](left, right)
                    else:
                        raise ValueError(f"Type mismatch: Cannot compare {type(left).__name__} and {type(right).__name__} at line {line}")
                else:
                    raise ValueError(f"Unknown operator: {operator} at line {line}")
                if self.verbose:
                    console.print(f"[magenta]Evaluated {left} {operator} {right} to: {result}[/magenta]")
                return result
            elif node_type == 'AssignmentStatement':
                if self.verbose:
                    console.print(f"[magenta]Assigning to '{node['identifier']}'[/magenta]")
                value = self.evaluate(node['value'])
                if value is None:
                    if self.memory_manager.exists(node['identifier']):
                        self.memory_manager.update(node['identifier'], None)
                    else:
                        self.memory_manager.allocate(node['identifier'], None)
                else:
                    self.memory_manager.allocate(node['identifier'], value)
                if self.verbose:
                    console.print(f"[magenta]Assigned value: {value} to '{node['identifier']}'[/magenta]")
            elif node_type == 'FunctionCall':
                if self.verbose:
                    console.print(f"[magenta]Calling function '{node['name']}' with args: {node['arguments']}[/magenta]")
                return self.evaluate_function(node['name'], node['arguments'], line)
            elif node_type == 'FunctionDeclaration':
                if self.verbose:
                    console.print(f"[magenta]Declaring function '{node['name']}'[/magenta]")
                self.functions[node['name']] = {
                    'parameters': node['parameters'],
                    'body': node['body']
                }
            elif node_type == 'ReturnStatement':
                if self.verbose:
                    console.print("[magenta]Evaluating return statement[/magenta]")
                return self.evaluate(node['value'])
            elif node_type == 'ListLiteral':
                return [self.evaluate(element) for element in node['elements']]
            elif node_type == 'Block':
                if self.verbose:
                    console.print("[magenta]Entering Block[/magenta]")
                for statement in node['body']:
                    result = self.evaluate(statement)
                    if isinstance(result, dict) and result.get('type') == 'ReturnStatement':
                        if self.verbose:
                            console.print("[magenta]Exiting Block with return[/magenta]")
                        return result
                if self.verbose:
                    console.print("[magenta]Exiting Block[/magenta]")
            elif node_type == 'ParallelStatement':
                if self.verbose:
                    console.print("[magenta]Executing parallel block[/magenta]")
                # Submit each statement in the block to run concurrently
                futures = []
                for statement in node['body']['body']:
                    future = self.thread_pool.submit(self.evaluate, statement)
                    futures.append(future)
                return futures  # Return list of futures for result collection
            else:
                return self.evaluate_control_structure(node)
        else:
            raise ValueError(f"Unknown node type: {type(node)} at line {line}")

    def evaluate_control_structure(self, node):
        node_type = node.get('type')
        line = node.get('line')
        if node_type == 'IfStatement':
            if self.verbose:
                console.print("[magenta]Evaluating IfStatement condition[/magenta]")
            condition = self.evaluate(node['condition'])
            if condition:
                if self.verbose:
                    console.print("[magenta]Condition true, entering then branch[/magenta]")
                return self.evaluate(node['thenBranch'])
            elif node['elseBranch'] is not None:
                if self.verbose:
                    console.print("[magenta]Condition false, entering else branch[/magenta]")
                return self.evaluate(node['elseBranch'])
        elif node_type == 'WhileStatement':
            if self.verbose:
                console.print("[magenta]Entering WhileStatement loop[/magenta]")
            while self.evaluate(node['condition']):
                self.evaluate(node['body'])
            if self.verbose:
                console.print("[magenta]Exiting WhileStatement loop[/magenta]")
        elif node_type == 'ForStatement':
            if self.verbose:
                console.print("[magenta]Entering ForStatement loop[/magenta]")
            iterable = self.evaluate(node['iterable'])
            if not isinstance(iterable, (list, tuple, range)):
                raise ValueError(f"For loop expects an iterable, got {type(iterable).__name__} at line {line}")
            for value in iterable:
                self.memory_manager.allocate(node['identifier'], value)
                self.evaluate(node['body'])
            if self.verbose:
                console.print("[magenta]Exiting ForStatement loop[/magenta]")
        else:
            raise ValueError(f"Unknown control structure type: {node_type} at line {line}")

    def evaluate_function(self, function_name, arguments, line):
        if self.verbose:
            console.print(f"[magenta]Evaluating function call '{function_name}'[/magenta]")
        if function_name == "print":
            evaluated_args = [self.evaluate(arg) for arg in arguments]
            if self.verbose:
                console.print(f"[magenta]Printing arguments: {evaluated_args}[/magenta]")
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
        elif function_name =="help":
            help_text = """
[bold green]LanPro Built-in Help[/bold green]
Available Commands and Features:
  - Assignment: x = 10;    (Assign a value to a variable)
  - Arithmetic: y = x + 5; (Supports +, -, *, /, <, >, <=, >=, ==, !=)
  - print(x);              (Print variable or value)
  - free(x);               (Deallocate a variable)
  - help();                  (Display this help message)
  - Variables: Dynamic allocation with garbage collection
  - Control Structures: if, while, for (syntax varies by implementation)
Running scripts:
    - python main.py -f <script_name>
    - python main.py --file <script_name>
    - python main.py -f <script_name> --verbose
    - python main.py -f <script_name> --debug

"""
            console.print(Panel(help_text, expand=False))
            return None  # Return None to indicate no further evaluation needed

        elif function_name in self.functions:
            function = self.functions[function_name]
            parameters = function['parameters']
            body = function['body']

            if len(arguments) != len(parameters):
                raise ValueError(f"Function '{function_name}' expects {len(parameters)} arguments, but got {len(arguments)} at line {line}")

            if self.verbose:
                console.print(f"[magenta]Setting up function '{function_name}' with parameters: {parameters}[/magenta]")
            original_variables = self.memory_manager.variables.copy()
            for param, arg in zip(parameters, arguments):
                self.memory_manager.allocate(param, self.evaluate(arg))

            result = None
            for statement in body['body']:
                result = self.evaluate(statement)

            self.memory_manager.variables = original_variables
            if self.verbose:
                console.print(f"[magenta]Function '{function_name}' returned: {result}[/magenta]")
            return result
        else:
            raise ValueError(f"Unknown function: {function_name} at line {line}")

    def run(self, program):
        all_futures = []  # Store all parallel execution futures
        for statement in program['body']:
            if self.verbose:
                console.print(f"[magenta]Running statement: {statement}[/magenta]")
            result = self.evaluate(statement)
            if isinstance(result, Future):
                all_futures.append(result)
            elif isinstance(result, list) and all(isinstance(f, Future) for f in result):
                all_futures.extend(result)
            if self.debug:
                console.print("[yellow]Debug: Variable States:[/yellow]")
                for var_name, info in self.memory_manager.variables.items():
                    if var_name not in self.memory_manager.deleted_vars:
                        console.print(f"[yellow]  {var_name} = {info['value']} (ref_count: {info['ref_count']})[/yellow]")
                console.print(f"[yellow]Debug: Memory Usage - Active Variables: {len([v for v in self.memory_manager.variables if v not in self.memory_manager.deleted_vars])}[/yellow]")
                console.print(f"[yellow]Debug: Deleted Variables: {self.memory_manager.deleted_vars}[/yellow]")
            else:
                console.print("[yellow]Debug Mode Off: Skipping variable states and memory usage[/yellow]")
            self.memory_manager.run_gc()
            if self.verbose:
                console.print("[magenta]Garbage collection completed[/magenta]")
        
        # Wait for all parallel executions to complete
        for future in all_futures:
            future.result()  # This will raise any exceptions that occurred in the parallel blocks

from rich.console import Console
from rich.panel import Panel
console = Console()