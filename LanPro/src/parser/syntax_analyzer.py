class SyntaxAnalyzer:
    def __init__(self):
        self.ast = []
        self.current_token = None
        self.position = 0

    def parse(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position]  # Initialize current_token
        self.ast = self.program()
        print("Generated AST:", self.ast)  # Debug print
        return self.ast

    def program(self):
        statements = []
        while self.position < len(self.tokens) and self.current_token is not None:
            # Skip invalid tokens (e.g., '}' outside block context)
            if self.current_token.type == 'OPERATOR' and self.current_token.value in ['}', ';']:
                self.advance()
                continue
            statements.append(self.statement())
        return {'type': 'Program', 'body': statements}

    def statement(self):
        if self.current_token is None:
            raise SyntaxError("Unexpected end of input while parsing a statement.")
        print(f"Parsing statement at position {self.current_token.position}, token: {self.current_token}")  # Debugging
        if self.current_token.type == 'IF':  # Prioritize 'if' keyword
            return self.if_statement()
        elif self.current_token.type == 'WHILE':  # Prioritize 'while' keyword
            return self.while_statement()
        elif self.current_token.type == 'FOR':  # Prioritize 'for' keyword
            return self.for_statement()
        elif self.current_token.type == 'IDENTIFIER' and self.current_token.value == 'function':  # Handle 'function' keyword
            return self.function_declaration()
        elif self.current_token.type == 'IDENTIFIER' and self.current_token.value == 'return':  # Handle 'return' keyword
            return self.return_statement()
        elif self.current_token.type == 'IDENTIFIER' and self.peek() and self.peek().type == 'OPERATOR' and self.peek().value == '=':
            return self.assignment_statement()
        elif self.current_token.type == 'IDENTIFIER' and self.peek() and self.peek().type == 'OPERATOR' and self.peek().value == '(':
            return self.function_call_statement()
        else:
            return self.expression_statement()

    def return_statement(self):
        print(f"Parsing return statement at position {self.current_token.position}")  # Debugging
        self.eat('IDENTIFIER')  # Consume the 'return' keyword
        value = self.expression()  # Parse the return value
        self.eat('OPERATOR')  # Ensure the statement ends with a semicolon
        return {
            'type': 'ReturnStatement',
            'value': value
        }

    def assignment_statement(self):
        identifier = self.current_token
        self.eat('IDENTIFIER')  # Consume the identifier
        self.eat('OPERATOR')  # Consume the '=' operator
        value = self.expression()  # Parse the right-hand side expression
        self.eat('OPERATOR')  # Ensure the statement ends with a semicolon
        return {
            'type': 'AssignmentStatement',
            'identifier': identifier.value,
            'value': value
        }
    
    def function_declaration(self):
        print(f"Parsing function declaration at position {self.current_token.position}")  # Debugging
        self.eat('IDENTIFIER')  # Consume the 'function' keyword
        function_name = self.current_token
        self.eat('IDENTIFIER')  # Consume the function name
        self.eat('OPERATOR')  # Consume the '(' operator

        # Parse the parameter list
        parameters = []
        if self.current_token.type == 'IDENTIFIER':
            parameters.append(self.current_token.value)
            self.eat('IDENTIFIER')
            while self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                self.eat('OPERATOR')  # Consume the ',' operator
                parameters.append(self.current_token.value)
                self.eat('IDENTIFIER')

        self.eat('OPERATOR')  # Consume the ')' operator
        body = self.block()  # Parse the function body

        return {
            'type': 'FunctionDeclaration',
            'name': function_name.value,
            'parameters': parameters,
            'body': body
        }

    def function_call_statement(self):
        print(f"Parsing function call at position {self.current_token.position}, token: {self.current_token}")  # Debugging
        function_name = self.current_token
        self.eat('IDENTIFIER')  # Consume the function name
        self.eat('OPERATOR')  # Consume the '(' operator
        arguments = self.argument_list()  # Parse the arguments
        self.eat('OPERATOR')  # Consume the ')' operator
        self.eat('OPERATOR')  # Ensure the statement ends with a semicolon
        print(f"Parsed function call: {function_name.value} with arguments {arguments}")  # Debugging
        return {
            'type': 'FunctionCall',
            'name': function_name.value,
            'arguments': arguments
        }

    def argument_list(self):
        print(f"Parsing argument list at position {self.current_token.position}, token: {self.current_token}")  # Debugging
        arguments = []
        if self.current_token.type != 'OPERATOR' or self.current_token.value != ')':
            arguments.append(self.expression())  # Parse the first argument
            while self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                self.eat('OPERATOR')  # Consume the ',' operator
                arguments.append(self.expression())  # Parse the next argument
        print(f"Parsed arguments: {arguments}")  # Debugging
        return arguments

    def block(self):
        """Parse a block of statements enclosed in braces."""
        if self.current_token is None or self.current_token.value != '{':
            raise SyntaxError(f"Expected '{{' but got '{self.current_token.value if self.current_token else 'None'}' at position {self.current_token.position if self.current_token else 'end of input'}")
        print(f"Entering block at position {self.current_token.position}")  # Debugging
        self.eat('OPERATOR')  # Consume the opening '{'

        statements = []
        while self.current_token is not None and (self.current_token.type != 'OPERATOR' or self.current_token.value != '}'):
            if self.current_token is None:
                raise SyntaxError("Unexpected end of input. Missing closing '}'.")
            statements.append(self.statement())

        print(f"Exiting block at position {self.current_token.position if self.current_token else 'end of input'}")  # Debugging
        self.eat('OPERATOR')  # Consume the closing '}'
        return {'type': 'Block', 'body': statements}
    
    
    def if_statement(self):
        print(f"Parsing if statement at position {self.current_token.position}")  # Debugging
        self.eat('IF')  # Consume the 'IF' keyword
        self.eat('OPERATOR')  # Consume the '(' operator
        condition = self.expression()  # Parse the condition
        self.eat('OPERATOR')  # Consume the ')' operator

        print(f"Parsing thenBranch at position {self.current_token.position}")  # Debugging
        then_branch = self.block()  # Parse the 'then' block

        else_branch = None
        if self.current_token is not None and self.current_token.type == 'ELSE':  # Check for 'ELSE' token
            print(f"Parsing elseBranch at position {self.current_token.position}")  # Debugging
            self.eat('ELSE')  # Consume the 'else' keyword
            else_branch = self.block()  # Parse the 'else' block

        return {
            'type': 'IfStatement',
            'condition': condition,
            'thenBranch': then_branch,
            'elseBranch': else_branch
        }


    def while_statement(self):
        self.eat('WHILE')
        self.eat('OPERATOR')  # Consume '('
        condition = self.expression()
        self.eat('OPERATOR')  # Consume ')'
        body = self.block()  # Parse block
        return {
            'type': 'WhileStatement',
            'condition': condition,
            'body': body
        }

    def for_statement(self):
        self.eat('FOR')
        self.eat('OPERATOR')  # Consume '('
        identifier = self.current_token
        self.eat('IDENTIFIER')
        self.eat('IN')
        iterable = self.expression()
        self.eat('OPERATOR')  # Consume ')'
        body = self.block()  # Parse block
        return {
            'type': 'ForStatement',
            'identifier': identifier.value,  # Use value as string
            'iterable': iterable,
            'body': body
        }

    def expression_statement(self):
        node = self.expression()  # Parse the expression
        if self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == ';':
            self.eat('OPERATOR')  # Ensure the statement ends with a semicolon
        return node

    def expression(self):
        print(f"Parsing expression at position {self.current_token.position}, token: {self.current_token}")  # Debugging
        if self.current_token.type == 'NUMBER':
            left = {'type': 'Literal', 'value': self.current_token.value}
            self.advance()
        elif self.current_token.type == 'IDENTIFIER':
            identifier = self.current_token
            self.advance()
            # Check if this is a function call
            if self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
                self.eat('OPERATOR')  # Consume the '('
                arguments = self.argument_list()  # Parse the arguments
                self.eat('OPERATOR')  # Consume the ')'
                left = {
                    'type': 'FunctionCall',
                    'name': identifier.value,
                    'arguments': arguments
                }
            else:
                left = {'type': 'Identifier', 'name': identifier.value}
        elif self.current_token.type == 'STRING':  # Handle string literals
            left = {'type': 'Literal', 'value': self.current_token.value}
            self.advance()
        elif self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
            self.eat('OPERATOR')  # Consume the '('
            left = self.expression()  # Recursively parse the inner expression
            self.eat('OPERATOR')  # Ensure the closing ')' is consumed
        else:
            raise SyntaxError(
                f"Unexpected token '{self.current_token.type}' with value '{self.current_token.value}' at position {self.current_token.position}."
            )

        # Check for a comparison or binary operator
        while self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=']:
            operator = self.current_token.value
            self.advance()
            right = self.expression()  # Parse the right-hand side of the expression
            left = {
                'type': 'BinaryOperation',
                'operator': operator,
                'left': left,
                'right': right
            }

        print(f"Parsed expression: {left}")  # Debugging
        return left

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
        else:
            raise SyntaxError(
                f"Syntax Error: Expected token '{token_type}', but got '{self.current_token.type}' "
                f"with value '{self.current_token.value}' at position {self.current_token.position}."
            )

    def next_token(self):
        """Advance to the next token."""
        self.position += 1
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        """Move to the next token."""
        self.current_token = self.next_token()
        if self.current_token is None:
            print("Reached end of token stream.")  # Debugging

    def peek(self):
        """Peek at the next token without advancing."""
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def error(self, message):
        raise SyntaxError(message)