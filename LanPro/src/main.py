from lexer.tokenizer import Tokenizer
from parser.syntax_analyzer import SyntaxAnalyzer
from semantic.semantic_analyzer import SemanticAnalyzer
from runtime.evaluator import Evaluator
from runtime.memory_manager import MemoryManager  # Import MemoryManager

def main():
    print("Welcome to LanPro, your custom programming language!")
    
    # Initialize components
    memory_manager = MemoryManager()  # Create a MemoryManager instance
    evaluator = Evaluator(memory_manager)  # Pass MemoryManager to Evaluator

    while True:
        # Prompt user for input
        code = input("\nEnter your LanPro code (or type 'exit' to quit): ")
        if code.lower() == 'exit':
            print("Goodbye!")
            break

        try:
            # Tokenize, parse, analyze, and execute
            tokenizer = Tokenizer(code)
            tokens = tokenizer.tokenize()
            
            parser = SyntaxAnalyzer()
            ast = parser.parse(tokens)
            
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.analyze(ast)
            
            evaluator.run(ast)  # Use the `run` method of Evaluator to execute the program
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()