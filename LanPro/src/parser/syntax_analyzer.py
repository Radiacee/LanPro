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
            if self.current_token.type == 'OPERATOR' and self.current_token.value in ['}', ';']:
                self.advance()
                continue
            statements.append(self.statement())
        return {'type': 'Program', 'body': statements}

    def statement(self):
        if self.current_token is None:
            raise SyntaxError(f"Unexpected end of input while parsing a statement at line {self.current_token.line if self.current_token else 'unknown'}")
        print(f"Parsing statement at position {self.current_token.position}, line {self.current_token.line}, token: {self.current_token}")
        if self.current_token.type == 'CLASS':
            return self.class_declaration()
        elif self.current_token.type == 'LET':
            return self.let_statement()
        elif self.current_token.type == 'IF':
            return self.if_statement()
        elif self.current_token.type == 'WHILE':
            return self.while_statement()
        elif self.current_token.type == 'FOR':
            return self.for_statement()
        elif self.current_token.type == 'PARALLEL':
            return self.parallel_statement()
        elif self.current_token.type == 'SCHEDULE':
            return self.schedule_statement()
        elif self.current_token.type == 'IDENTIFIER' and self.current_token.value == 'function':
            return self.function_declaration()
        elif self.current_token.type == 'IDENTIFIER' and self.current_token.value == 'return':
            return self.return_statement()
        elif self.current_token.type == 'IDENTIFIER' and self.peek() and self.peek().type == 'OPERATOR' and self.peek().value == '=':
            return self.assignment_statement()
        elif self.current_token.type == 'IDENTIFIER' and self.peek() and self.peek().type == 'OPERATOR' and self.peek().value == '(':
            return self.function_call_statement()
        else:
            return self.expression_statement()

    def return_statement(self):
        print(f"Parsing return statement at position {self.current_token.position}, line {self.current_token.line}")
        self.eat('IDENTIFIER')
        value = self.expression()
        self.eat('OPERATOR')
        return {
            'type': 'ReturnStatement',
            'value': value,
            'line': self.current_token.line if self.current_token else None
        }
        
    def class_declaration(self):
        self.eat('CLASS')
        class_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('OPERATOR')  # {
        methods = []
        while self.current_token.value != '}':
            methods.append(self.function_declaration(is_method=True))
        self.eat('OPERATOR')  # }
        return {'type': 'ClassDeclaration', 'name': class_name, 'methods': methods}

    def let_statement(self):
        self.eat('LET')
        var_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('OPERATOR')  # =
        value = self.expression()
        self.eat('OPERATOR')  # ;
        return {'type': 'LetStatement', 'identifier': var_name, 'value': value}

    def assignment_statement(self):
        identifier = self.current_token
        self.eat('IDENTIFIER')
        self.eat('OPERATOR')
        value = self.expression()
        self.eat('OPERATOR')
        return {
            'type': 'AssignmentStatement',
            'identifier': identifier.value,
            'value': value,
            'line': identifier.line
        }
    
    def function_declaration(self, is_method=False):
        print(f"Parsing function declaration at position {self.current_token.position}, line {self.current_token.line}")
        if not is_method:
            self.eat('IDENTIFIER')  # 'function'
        function_name = self.current_token
        self.eat('IDENTIFIER')
        self.eat('OPERATOR')  # (
        parameters = []
        if self.current_token.type == 'IDENTIFIER':
            parameters.append(self.current_token.value)
            self.eat('IDENTIFIER')
            while self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                self.eat('OPERATOR')
                parameters.append(self.current_token.value)
                self.eat('IDENTIFIER')
        self.eat('OPERATOR')  # )
        body = self.block()
        return {
            'type': 'FunctionDeclaration',
            'name': function_name.value,
            'parameters': parameters,
            'body': body,
            'line': function_name.line
        }

    def function_call_statement(self):
        print(f"Parsing function call at position {self.current_token.position}, line {self.current_token.line}, token: {self.current_token}")
        function_name = self.current_token
        self.eat('IDENTIFIER')
        self.eat('OPERATOR')
        arguments = self.argument_list()
        self.eat('OPERATOR')
        self.eat('OPERATOR')
        print(f"Parsed function call: {function_name.value} with arguments {arguments}")
        return {
            'type': 'FunctionCall',
            'name': function_name.value,
            'arguments': arguments,
            'line': function_name.line
        }

    def argument_list(self):
        print(f"Parsing argument list at position {self.current_token.position}, line {self.current_token.line}, token: {self.current_token}")
        arguments = []
        if self.current_token.type != 'OPERATOR' or self.current_token.value != ')':
            arguments.append(self.expression())
            while self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                self.eat('OPERATOR')
                arguments.append(self.expression())
        print(f"Parsed arguments: {arguments}")
        return arguments

    def block(self):
        if self.current_token is None or self.current_token.value != '{':
            raise SyntaxError(f"Expected '{{' but got '{self.current_token.value if self.current_token else 'None'}' at position {self.current_token.position}, line {self.current_token.line if self.current_token else 'unknown'}")
        print(f"Entering block at position {self.current_token.position}, line {self.current_token.line}")
        self.eat('OPERATOR')

        statements = []
        while self.current_token is not None and (self.current_token.type != 'OPERATOR' or self.current_token.value != '}'):
            if self.current_token is None:
                raise SyntaxError("Unexpected end of input. Missing closing '}'.")
            statements.append(self.statement())

        print(f"Exiting block at position {self.current_token.position}, line {self.current_token.line if self.current_token else 'unknown'}")
        self.eat('OPERATOR')
        return {'type': 'Block', 'body': statements, 'line': self.current_token.line if self.current_token else None}
    
    def if_statement(self):
        print(f"Parsing if statement at position {self.current_token.position}, line {self.current_token.line}")
        self.eat('IF')
        self.eat('OPERATOR')
        condition = self.expression()
        self.eat('OPERATOR')

        print(f"Parsing thenBranch at position {self.current_token.position}, line {self.current_token.line}")
        then_branch = self.block()

        else_branch = None
        if self.current_token is not None and self.current_token.type == 'ELSE':
            print(f"Parsing elseBranch at position {self.current_token.position}, line {self.current_token.line}")
            self.eat('ELSE')
            else_branch = self.block()

        return {
            'type': 'IfStatement',
            'condition': condition,
            'thenBranch': then_branch,
            'elseBranch': else_branch,
            'line': self.current_token.line if self.current_token else None
        }

    def while_statement(self):
        self.eat('WHILE')
        self.eat('OPERATOR')
        condition = self.expression()
        self.eat('OPERATOR')
        body = self.block()
        return {
            'type': 'WhileStatement',
            'condition': condition,
            'body': body,
            'line': self.current_token.line if self.current_token else None
        }

    def for_statement(self):
        self.eat('FOR')
        self.eat('OPERATOR')
        identifier = self.current_token
        self.eat('IDENTIFIER')
        self.eat('IN')
        iterable = self.expression()
        self.eat('OPERATOR')
        body = self.block()
        return {
            'type': 'ForStatement',
            'identifier': identifier.value,
            'iterable': iterable,
            'body': body,
            'line': identifier.line
        }

    def expression_statement(self):
        node = self.expression()
        if self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == ';':
            self.eat('OPERATOR')
        return node

    def expression(self):
        print(f"Parsing expression at position {self.current_token.position}, line {self.current_token.line}, token: {self.current_token}")

        # --- NEW: Handle 'new' keyword for object instantiation ---
        if self.current_token.type == 'NEW':
            self.eat('NEW')
            class_name = self.current_token.value
            self.eat('IDENTIFIER')
            self.eat('OPERATOR')  # (
            self.eat('OPERATOR')  # )
            left = {'type': 'NewExpression', 'class': class_name, 'line': self.current_token.line}
        # --- END NEW ---
        
        if self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
            self.eat('OPERATOR')  # (
            params = []
            if self.current_token.type == 'IDENTIFIER':
                params.append(self.current_token.value)
                self.eat('IDENTIFIER')
                while self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR')
                    params.append(self.current_token.value)
                    self.eat('IDENTIFIER')
            self.eat('OPERATOR')  # )
            if self.current_token.type == 'OPERATOR' and self.current_token.value == '=>':
                self.eat('OPERATOR')
                body = self.expression()
                return {
                    'type': 'LambdaExpression',
                    'parameters': params,
                    'body': body,
                    'line': self.current_token.line
                }

        elif self.current_token.type == 'NUMBER':
            left = {'type': 'Literal', 'value': self.current_token.value, 'line': self.current_token.line}
            self.advance()
        elif self.current_token.type == 'IDENTIFIER':
            identifier = self.current_token
            self.advance()
            if self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
                self.eat('OPERATOR')
                arguments = self.argument_list()
                self.eat('OPERATOR')
                left = {
                    'type': 'FunctionCall',
                    'name': identifier.value,
                    'arguments': arguments,
                    'line': identifier.line
                }
            else:
                left = {'type': 'Identifier', 'name': identifier.value, 'line': identifier.line}
        elif self.current_token.type == 'STRING':
            left = {'type': 'Literal', 'value': self.current_token.value, 'line': self.current_token.line}
            self.advance()
        elif self.current_token.type == 'NULL':
            left = {'type': 'NULL', 'value': None, 'line': self.current_token.line}
            self.advance()
        elif self.current_token.type == 'OPERATOR' and self.current_token.value == '[':
            self.eat('OPERATOR')  # Eat '['
            elements = []
            while self.current_token is not None and not (self.current_token.type == 'OPERATOR' and self.current_token.value == ']'):
                elements.append(self.expression())
                if self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR')  # Eat ','
                else:
                    break
            self.eat('OPERATOR')  # Eat ']'
            left = {'type': 'ListLiteral', 'elements': elements, 'line': self.current_token.line if self.current_token else None}
        else:
            raise SyntaxError(
                f"Unexpected token '{self.current_token.type}' with value '{self.current_token.value}' at position {self.current_token.position}, line {self.current_token.line}."
            )

        # --- NEW: Handle member access and method calls (e.g., p.greet or p.greet()) ---
        while self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == '.':
            self.eat('OPERATOR')
            member = self.current_token.value
            self.eat('IDENTIFIER')
            # Check for method call: p.greet()
            if self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
                self.eat('OPERATOR')
                arguments = self.argument_list()
                self.eat('OPERATOR')
                left = {
                    'type': 'MethodCall',
                    'object': left,
                    'member': member,
                    'arguments': arguments,
                    'line': self.current_token.line if self.current_token else None
                }
            else:
                left = {
                    'type': 'MemberAccess',
                    'object': left,
                    'member': member,
                    'line': self.current_token.line if self.current_token else None
                }
        # --- END NEW ---

        while self.current_token is not None and self.current_token.type == 'OPERATOR' and self.current_token.value in ['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=']:
            operator = self.current_token.value
            self.advance()
            right = self.expression()
            left = {
                'type': 'BinaryOperation',
                'operator': operator,
                'left': left,
                'right': right,
                'line': left['line'] if 'line' in left else self.current_token.line if self.current_token else None
            }

        print(f"Parsed expression: {left}")
        return left

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
        else:
            raise SyntaxError(
                f"Syntax Error: Expected token '{token_type}', but got '{self.current_token.type}' "
                f"with value '{self.current_token.value}' at position {self.current_token.position}, line {self.current_token.line}."
            )

    def next_token(self):
        self.position += 1
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def advance(self):
        self.current_token = self.next_token()
        if self.current_token is None:
            print("Reached end of token stream.")

    def peek(self):
        if self.position + 1 < len(self.tokens):
            return self.tokens[self.position + 1]
        return None

    def error(self, message):
        raise SyntaxError(message)

    def parallel_statement(self):
        self.eat('PARALLEL')
        body = self.block()
        return {
            'type': 'ParallelStatement',
            'body': body,
            'line': self.current_token.line if self.current_token else None
        }

    def schedule_statement(self):
        print(f"Parsing schedule statement at position {self.current_token.position}, line {self.current_token.line}")
        self.eat('SCHEDULE')
        body = self.block()
        
        # Check for timing specifier
        if self.current_token.type == 'EVERY':
            self.eat('EVERY')  # Eat the EVERY token
            interval = self.expression()
            schedule_type = 'recurring'
        elif self.current_token.type == 'AFTER':
            self.eat('AFTER')  # Eat the AFTER token
            interval = self.expression()
            schedule_type = 'delayed'
        else:
            raise SyntaxError(f"Expected 'every' or 'after' after schedule block at line {self.current_token.line}")
        
        # Eat the semicolon if present
        if self.current_token and self.current_token.type == 'OPERATOR' and self.current_token.value == ';':
            self.eat('OPERATOR')
        
        return {
            'type': 'ScheduleStatement',
            'body': body,
            'interval': interval,
            'schedule_type': schedule_type,
            'line': self.current_token.line if self.current_token else None
        }