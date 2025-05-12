def handle_runtime_error(error_message, line_number=None):
    if line_number is not None:
        print(f"Runtime Error on line {line_number}: {error_message}")
    else:
        print(f"Runtime Error: {error_message}")

def handle_syntax_error(error_message, line_number):
    print(f"Syntax Error on line {line_number}: {error_message}")

def handle_semantic_error(error_message, line_number):
    print(f"Semantic Error on line {line_number}: {error_message}")

def verbose_logging(message):
    print(f"DEBUG: {message}")