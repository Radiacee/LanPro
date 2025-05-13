from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
import argparse
from lexer.tokenizer import Tokenizer
from parser.syntax_analyzer import SyntaxAnalyzer
from semantic.semantic_analyzer import SemanticAnalyzer
from runtime.evaluator import Evaluator
from runtime.memory_manager import MemoryManager

def main():
    console = Console()
    console.print(Panel("Welcome to [bold magenta]LanPro[/bold magenta], your custom programming language!", expand=False))
    

    # Set up argument parser
    parser = argparse.ArgumentParser(description="LanPro Interpreter")
    parser.add_argument('-f', '--file', type=str, help='Path to the LanPro script file to execute')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose mode to show token stream, parse trace, and eval steps')
    args = parser.parse_args()

    # Initialize components
    memory_manager = MemoryManager()
    evaluator = Evaluator(memory_manager)

    if args.file:
        # Read and execute the script file
        try:
            with open(args.file, 'r') as file:
                code = file.read()
                tokenizer = Tokenizer(code)
                tokens = tokenizer.tokenize()
                if args.verbose:
                    console.print("[bold cyan]Token Stream:[/bold cyan]")
                    for token in tokens:
                        console.print(f"  {token}")

                parser_instance = SyntaxAnalyzer()
                ast = parser_instance.parse(tokens)
                if args.verbose:
                    console.print("[bold cyan]Parse Trace:[/bold cyan]")
                    # Note: Parse trace is already printed in SyntaxAnalyzer with debug prints

                semantic_analyzer = SemanticAnalyzer()
                semantic_analyzer.analyze(ast)
                if args.verbose:
                    console.print("[bold cyan]Evaluation Steps:[/bold cyan]")
                    evaluator.set_verbose(True)  # Enable verbose mode in Evaluator

                evaluator.run(ast)
                console.print("[green]Script executed successfully![/green]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    else:
        # Interactive REPL mode
        while True:
            code = Prompt.ask("\n[cyan]Enter your LanPro code (or type 'exit' to quit)[/cyan]\n")
            if code.lower() == 'exit':
                console.print("[bold red]Goodbye![/bold red]")
                break

            try:
                tokenizer = Tokenizer(code)
                tokens = tokenizer.tokenize()
                if args.verbose:
                    console.print("[bold cyan]Token Stream:[/bold cyan]")
                    for token in tokens:
                        console.print(f"  {token}")

                parser_instance = SyntaxAnalyzer()
                ast = parser_instance.parse(tokens)
                if args.verbose:
                    console.print("[bold cyan]Parse Trace:[/bold cyan]")
                    # Note: Parse trace is already printed in SyntaxAnalyzer with debug prints

                semantic_analyzer = SemanticAnalyzer()
                semantic_analyzer.analyze(ast)
                if args.verbose:
                    console.print("[bold cyan]Evaluation Steps:[/bold cyan]")
                    evaluator.set_verbose(True)  # Enable verbose mode in Evaluator
                    
                evaluator.run(ast)
                console.print("[green]Execution completed successfully![/green]")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()