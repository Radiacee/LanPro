# LanPro Programming Language

## Overview
LanPro is a fun and innovative programming language designed to provide a unique approach to coding by swapping the sequence of traditional programming constructs. This project aims to create a fully functional interpreter for LanPro, complete with lexical analysis, syntax analysis, semantic analysis, and runtime evaluation.

## Features
- **Lexical Analysis**: Accurately identifies tokens and handles errors for invalid tokens.
- **Syntax Analysis**: Processes valid syntax and constructs an Abstract Syntax Tree (AST).
- **Semantic Analysis**: Manages symbol tables, performs type checking, and detects semantic issues.
- **Execution & Evaluation**: Evaluates expressions, handles control structures, and supports function execution.
- **Memory Management**: Manages variable lifecycle and memory cleanup effectively.
- **Error Handling & Debugging**: Provides helpful error messages and optional verbose logging.
- **User Interface / CLI**: Offers a clean and intuitive command-line interface with REPL support.
- **Advanced Features**: Supports object-oriented programming, lambda functions, concurrency, and extensibility.

## Getting Started
To get started with LanPro, follow these steps:

1. **Clone the Repository**: 
   ```
   git clone <repository-url>
   cd LanPro
   ```

2. **Install Dependencies**: 
   ```
   pip install -r requirements.txt
   ```

3. **Run the Interpreter**: 
   ```
   python src/main.py
   ```

4. **Use the REPL**: Once the interpreter is running, you can start typing LanPro code directly into the command line.

## Documentation
For detailed documentation on each component of the LanPro interpreter, refer to the following files:
- **Lexer**: `src/lexer/tokenizer.py`
- **Parser**: `src/parser/syntax_analyzer.py`
- **Semantic Analysis**: `src/semantic/semantic_analyzer.py`
- **Runtime**: `src/runtime/evaluator.py`
- **CLI**: `src/cli/repl.py`
- **Error Handling**: `src/utils/error_handler.py`

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.