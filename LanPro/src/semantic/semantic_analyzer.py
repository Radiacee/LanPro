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
        elif node['type'] == 'Block':
            if not isinstance(node['body'], list):
                raise Exception(f"Expected 'body' of Block node to be a list, but got {type(node['body'])}")
            for statement in node['body']:
                self.visit(statement)
        elif node['type'] == 'FunctionCall':
            for argument in node['arguments']:
                self.visit(argument)
        elif node['type'] == 'BinaryOperation':
            self.visit(node['left'])
            self.visit(node['right'])
        elif node['type'] == 'Literal' or node['type'] == 'Identifier':
            pass  # No semantic checks needed for literals or identifiers
        elif node['type'] == 'FunctionDeclaration':
            self.analyze_function_declaration(node)
        elif node['type'] == 'ReturnStatement':  # Handle ReturnStatement nodes
            self.analyze_return_statement(node)
        else:
            raise Exception(f"Unknown node type: {node['type']}")

    def analyze_assignment(self, node):
        variable_name = node['identifier']
        if variable_name in self.declared_variables:
            # Issue a redeclaration warning
            self.console.print(f"[bold yellow]Notice:[/bold yellow] Redeclaration warning for variable '{variable_name}'")
        else:
            # Mark the variable as declared
            self.declared_variables.add(variable_name)
        self.visit(node['value'])  # Analyze the value being assigned

    def analyze_function_declaration(self, node):
        function_name = node['name']
        if function_name in self.declared_functions:
            # Issue a redeclaration warning for the function
            self.console.print(f"[bold yellow]Notice:[/bold yellow] Redeclaration warning for function '{function_name}'")
        else:
            # Mark the function as declared
            self.declared_functions.add(function_name)

        # Temporarily add parameters to the declared variables
        original_variables = self.declared_variables.copy()
        for param in node['parameters']:
            self.declared_variables.add(param)

        # Analyze the function body
        if node['body']['type'] == 'Block':  # Ensure the body is a Block node
            self.visit(node['body'])
        else:
            raise Exception(f"Expected a Block node for function body, but got {node['body']['type']}")

        # Restore the original declared variables
        self.declared_variables = original_variables

    def analyze_return_statement(self, node):
        # Analyze the return value
        self.console.print("[cyan]Analyzing return statement...[/cyan]")
        self.visit(node['value'])