from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from lexer.tokenizer import Tokenizer
from parser.syntax_analyzer import SyntaxAnalyzer
from semantic.semantic_analyzer import SemanticAnalyzer
from runtime.evaluator import Evaluator
from runtime.memory_manager import MemoryManager

def main():
    console = Console()
    console.print(Panel("Welcome to [bold magenta]LanPro[/bold magenta], your custom programming language!", expand=False))
    
    # Initialize components
    memory_manager = MemoryManager()
    evaluator = Evaluator(memory_manager)

    while True:
        # Prompt user for input
        code = Prompt.ask("\n[cyan]Enter your LanPro code (or type 'exit' to quit)[/cyan]")
        if code.lower() == 'exit':
            console.print("[bold red]Goodbye![/bold red]")
            break

        try:
            # Tokenize, parse, analyze, and execute
            tokenizer = Tokenizer(code)
            tokens = tokenizer.tokenize()
            
            parser = SyntaxAnalyzer()
            ast = parser.parse(tokens)
            
            semantic_analyzer = SemanticAnalyzer()
            semantic_analyzer.analyze(ast)
            
            evaluator.run(ast)
            console.print("[green]Execution completed successfully![/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()