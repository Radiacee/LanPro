class Token:
    def __init__(self, type, value, position=None, line=None):
        self.type = type
        self.value = value
        self.position = position
        self.line = line

    def __repr__(self):
        return f'Token({self.type}, {self.value}, position={self.position}, line={self.line})'

class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if self.source_code else None
        self.tokens = []
        self.line = 1  # Track line number

    def error(self, message):
        raise Exception(f'Error: {message} at position {self.position}, line {self.line}')

    def advance(self):
        if self.current_char == '\n':
            self.line += 1
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def tokenize(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char == 'n' and self.peek_next(4) == 'null':
                self.tokens.append(self.null_literal())
                continue

            if self.current_char.isalpha():
                token = self.identifier_or_keyword()
                self.tokens.append(token)
                continue

            if self.current_char.isdigit():
                self.tokens.append(self.number())
                continue

            if self.current_char == '"':
                self.tokens.append(self.string())
                continue
            
            if self.current_char == '=' and self.peek_next(2) == '=>':
                start_position = self.position
                start_line = self.line
                self.advance()  # skip '='
                self.advance()  # skip '>'
                self.tokens.append(Token('OPERATOR', '=>', start_position, start_line))
                continue

            if self.current_char in "=+-*/(){};<>![],.":
                self.tokens.append(self.operator())
                continue

            self.error(f'Invalid character: {self.current_char}')

        return self.tokens

    def peek_next(self, n):
        if self.position + n <= len(self.source_code):
            return self.source_code[self.position:self.position + n]
        return ''

    def identifier_or_keyword(self):
        """Handle identifiers and keywords"""
        keywords = {
            'if': 'IF',
            'else': 'ELSE',
            'while': 'WHILE',
            'for': 'FOR',
            'class': 'CLASS',
            'let': 'LET',
            'new': 'NEW',
            'in': 'IN',
            'parallel': 'PARALLEL',
            'schedule': 'SCHEDULE',
            'every': 'EVERY',
            'after': 'AFTER'
        }
        
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
            
        print(f"Tokenizing identifier/keyword: '{result}'")  # Debug output
        
        if result in keywords:
            print(f"Recognized as keyword: {keywords[result]}")  # Debug output
            return Token(keywords[result], result, self.line)
        return Token('IDENTIFIER', result, self.line)

    def number(self):
        result = ''
        start_position = self.position
        start_line = self.line
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        print(f"Tokenized number: {result} at position {start_position}, line {start_line}")
        return Token('NUMBER', int(result), start_position, start_line)

    def string(self):
        result = ''
        start_position = self.position
        start_line = self.line
        self.advance()  # Skip opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            self.error("Unterminated string literal")
        self.advance()  # Skip closing quote
        print(f"Tokenized string: {result} at position {start_position}, line {start_line}")
        return Token('STRING', f'"{result}"', start_position, start_line)

    def operator(self):
        start_position = self.position
        start_line = self.line
        char = self.current_char
        self.advance()

        if char in ['<', '>', '=', '!'] and self.current_char == '=':
            result = char + self.current_char
            self.advance()
            print(f"Tokenized operator: {result} at position {start_position}, line {start_line}")
            return Token('OPERATOR', result, start_position, start_line)

        print(f"Tokenized operator: {char} at position {start_position}, line {start_line}")
        return Token('OPERATOR', char, start_position, start_line)

    def null_literal(self):
        start_position = self.position
        start_line = self.line
        self.advance()  # Skip 'n'
        self.advance()  # Skip 'u'
        self.advance()  # Skip 'l'
        self.advance()  # Skip 'l'
        return Token('NULL', 'null', start_position, start_line)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.next_token()
        else:
            raise SyntaxError(
                f"Syntax Error: Expected token '{token_type}', but got '{self.current_token.type}' "
                f"with value '{self.current_token.value}' at position {self.current_token.position}, line {self.current_token.line}."
            )

def main():
    source_code = 'x = 10; if (x >= 5) { print("hello"); } else { print("world"); }'
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()