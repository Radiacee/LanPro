class Token:
    def __init__(self, type, value, position=None):
        self.type = type
        self.value = value
        self.position = position  # Track the position of the token in the source code

    def __repr__(self):
        return f'Token({self.type}, {self.value}, position={self.position})'


class Tokenizer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if self.source_code else None
        self.tokens = []

    def error(self, message):
        raise Exception(f'Error: {message} at position {self.position}')

    def advance(self):
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

            if self.current_char.isalpha():
                self.tokens.append(self.identifier())
                continue

            if self.current_char.isdigit():
                self.tokens.append(self.number())
                continue

            if self.current_char == '"':
                self.tokens.append(self.string())
                continue

            if self.current_char in "=+-*/(){};<>!":
                self.tokens.append(self.operator())
                continue

            self.error(f'Invalid character: {self.current_char}')

        return self.tokens

    def identifier(self):
        result = ''
        start_position = self.position  # Track the starting position of the identifier
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token('IDENTIFIER', result, start_position)

    def number(self):
        result = ''
        start_position = self.position  # Track the starting position of the number
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token('NUMBER', int(result), start_position)

    def string(self):
        result = ''
        start_position = self.position  # Track the starting position of the string
        self.advance()  # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char != '"':  # Ensure the string is properly closed
            self.error("Unterminated string literal")
        self.advance()  # Skip the closing quote
        return Token('STRING', result, start_position)

    def operator(self):
        start_position = self.position  # Track the position of the operator
        char = self.current_char
        self.advance()

        # Handle two-character operators (e.g., >=, <=, ==, !=)
        if char in ['<', '>', '=', '!'] and self.current_char == '=':
            result = char + self.current_char
            self.advance()
            print(f"Tokenized operator: {result} at position {start_position}")  # Debugging
            return Token('OPERATOR', result, start_position)

        # Handle single-character operators
        print(f"Tokenized operator: {char} at position {start_position}")  # Debugging
        return Token('OPERATOR', char, start_position)


def main():
    source_code = 'x = 10; if (x >= 5) { print("hello"); } else { print("world"); }'
    tokenizer = Tokenizer(source_code)
    tokens = tokenizer.tokenize()
    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()