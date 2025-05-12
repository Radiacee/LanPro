# LanPro Programming Language

LanPro is a fun and innovative programming language designed to explore the concepts of programming language design and implementation. The name "LanPro" is derived from a simple swap of the letters in "Programming Language," reflecting its playful nature.

## Features

- **Lexical Analysis**: Efficiently tokenizes input code, identifying valid tokens and handling errors for invalid ones.
- **Syntax Analysis**: Parses the code to ensure valid syntax and constructs an Abstract Syntax Tree (AST) for further processing.
- **Semantic Analysis**: Manages symbol tables, performs type checking, and detects semantic issues such as undefined variables.
- **Execution & Evaluation**: Evaluates expressions, handles control structures (if, while, for), and supports function execution.
- **Memory Management**: Manages variable lifecycle, memory cleanup, and prevents use-after-delete issues.
- **Error Handling & Debugging**: Provides runtime error messages and helpful debugging feedback, with an optional verbose mode for detailed logs.
- **User Interface / CLI**: Offers a clean and intuitive command-line interface with support for user documentation and help commands.
- **Advanced Features**: Supports object-oriented programming, lambda functions, concurrency, and extensibility for new features.

## Getting Started

To get started with LanPro, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd LanPro
pip install -r requirements.txt
```

You can run the interpreter using:

```bash
python src/main.py
```

## Documentation

For detailed usage instructions and feature descriptions, please refer to the documentation located in the `docs` directory.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to help improve LanPro.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.