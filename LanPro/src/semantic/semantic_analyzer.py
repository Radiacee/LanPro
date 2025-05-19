from rich.console import Console

class SemanticAnalyzer:
    def __init__(self):
        self.console = Console()
        self.declared_variables = set()  # Track declared variables
        self.declared_functions = set()  # Track declared functions

    def analyze(self, ast):
        self.console.print("[cyan]Starting semantic analysis...[/cyan]")
        self.visit(ast)

    def visit(self, node):
        if node['type'] == 'Program':
            for statement in node['body']:
                self.visit(statement)
        elif node['type'] == 'AssignmentStatement':
            self.analyze_assignment(node)
        elif node['type'] == 'IfStatement':
            self.visit(node['condition'])
            self.visit(node['thenBranch'])
            if node['elseBranch']:
                self.visit(node['elseBranch'])
        elif node['type'] == 'WhileStatement':
            self.visit(node['condition'])
            self.visit(node['body'])
        elif node['type'] == 'ForStatement':
            self.declared_variables.add(node['identifier'])
            self.visit(node['iterable'])
            self.visit(node['body'])
        elif node['type'] == 'ParallelStatement':
            self.visit(node['body'])
        elif node['type'] == 'ScheduleStatement':
            self.visit(node['body'])
            self.visit(node['interval'])
        elif node['type'] == 'NewExpression':
            pass
        elif node['type'] == 'MethodCall':
            self.visit(node['object'])
            for arg in node['arguments']:
                self.visit(arg)
        elif node['type'] == 'LambdaExpression':
            # Visit the body of the lambda to check for semantic errors
            self.visit(node['body'])
        elif node['type'] == 'Block':
            if not isinstance(node['body'], list):
                raise Exception(f"Expected 'body' of Block node to be a list, but got {type(node['body'])} at line {node.get('line', 'unknown')}")
            for statement in node['body']:
                self.visit(statement)
        elif node['type'] == 'FunctionCall':
            for argument in node['arguments']:
                self.visit(argument)
        elif node['type'] == 'BinaryOperation':
            self.visit(node['left'])
            self.visit(node['right'])
        elif node['type'] == 'Literal' or node['type'] == 'Identifier':
            pass
        elif node['type'] == 'NULL':
            pass
        elif node['type'] == 'ListLiteral':
            for element in node['elements']:
                self.visit(element)
        elif node['type'] == 'FunctionDeclaration':
            self.analyze_function_declaration(node)
        elif node['type'] == 'ClassDeclaration':
            for method in node['methods']:
                self.visit(method)
        elif node['type'] == 'ReturnStatement':
            self.analyze_return_statement(node)
        else:
            raise Exception(f"Unknown node type: {node['type']} at line {node.get('line', 'unknown')}")

    def analyze_assignment(self, node):
        variable_name = node['identifier']
        if variable_name in self.declared_variables:
            self.console.print(f"[bold yellow]Notice:[/bold yellow] Redeclaration warning for variable '{variable_name}' at line {node.get('line', 'unknown')}")
        else:
            self.declared_variables.add(variable_name)
        self.visit(node['value'])

    def analyze_function_declaration(self, node):
        function_name = node['name']
        if function_name in self.declared_functions:
            self.console.print(f"[bold yellow]Notice:[/bold yellow] Redeclaration warning for function '{function_name}' at line {node.get('line', 'unknown')}")
        else:
            self.declared_functions.add(function_name)

        original_variables = self.declared_variables.copy()
        for param in node['parameters']:
            self.declared_variables.add(param)

        if node['body']['type'] == 'Block':
            self.visit(node['body'])
        else:
            raise Exception(f"Expected a Block node for function body, but got {node['body']['type']} at line {node.get('line', 'unknown')}")

        self.declared_variables = original_variables

    def analyze_return_statement(self, node):
        self.console.print("[cyan]Analyzing return statement...[/cyan]")
        self.visit(node['value'])