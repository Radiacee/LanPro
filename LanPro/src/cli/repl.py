from lexer.tokenizer import Tokenizer
from parser.syntax_analyzer import SyntaxAnalyzer
from semantic.semantic_analyzer import SemanticAnalyzer
from runtime.evaluator import Evaluator
from runtime.memory_manager import MemoryManager  # Import MemoryManager

class LanProREPL:
    def __init__(self):
        self.memory_manager = MemoryManager()  # Initialize MemoryManager
        self.evaluator = Evaluator(self.memory_manager)  # Pass MemoryManager to Evaluator

    def start(self):
        print("Welcome to LanPro REPL! Type 'exit' to quit.")
        while True:
            try:
                user_input = input("LanPro> ")
                if user_input.lower() == 'exit':
                    print("Goodbye!")
                    break

                # Tokenize the input
                tokenizer = Tokenizer(user_input)
                tokens = tokenizer.tokenize()
                print("Tokens:", tokens)  # Debugging: Show tokens

                # Parse the tokens into an AST
                parser = SyntaxAnalyzer()
                ast = parser.parse(tokens)
                print("AST:", ast)  # Debugging: Show AST

                # Perform semantic analysis
                semantic_analyzer = SemanticAnalyzer()
                semantic_analyzer.analyze(ast)

                # Evaluate the AST
                self.evaluator.run(ast)
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    repl = LanProREPL()
    repl.start()