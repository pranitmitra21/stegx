import sys
import os

# Force UTF-8 encoding for standard output on Windows to prevent UnicodeEncodeError
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from analyzer.core import run_analysis
from reports.generator import print_cli_report, save_json_report
from utils.encoder import encode

console = Console()

def display_banner():
    banner = """
███████╗████████╗███████╗ ██████╗ ██╗  ██╗
██╔════╝╚══██╔══╝██╔════╝██╔════╝ ╚██╗██╔╝
███████╗   ██║   █████╗  ██║  ███╗ ╚███╔╝
╚════██║   ██║   ██╔══╝  ██║   ██║ ██╔██╗
███████║   ██║   ███████╗╚██████╔╝██╔╝ ██╗
╚══════╝   ╚═╝   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝

StegX
Advanced Steganography Detection & Analysis Toolkit

Version: 1.0.0
Author: Security Researcher
License: MIT
Python Version: {python_version}
Operating System: {os_name}
Working Directory: {cwd}
"""
    formatted_banner = banner.format(
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        os_name=os.name.upper(),
        cwd=os.getcwd()
    )
    console.print(Panel(formatted_banner, style="bold green", border_style="green"))

def main_menu():
    while True:
        console.print("\n[bold cyan]========================[/bold cyan]")
        console.print("[bold cyan]       MAIN MENU        [/bold cyan]")
        console.print("[bold cyan]========================[/bold cyan]")
        console.print("[bold yellow]1)[/bold yellow] Scan File & Detect Steganography")
        console.print("[bold yellow]2)[/bold yellow] Scan Folder")
        console.print("[bold yellow]3)[/bold yellow] Extract Hidden Payload")
        console.print("[bold yellow]4)[/bold yellow] Analyze Metadata")
        console.print("[bold yellow]5)[/bold yellow] Calculate File Hashes")
        console.print("[bold yellow]6)[/bold yellow] Compare Two Files")
        console.print("[bold yellow]7)[/bold yellow] Batch Scan")
        console.print("[bold yellow]8)[/bold yellow] Generate Report")
        console.print("[bold yellow]9)[/bold yellow] Settings")
        console.print("[bold yellow]10)[/bold yellow] Help")
        console.print("[bold yellow]11)[/bold yellow] Examples")
        console.print("[bold yellow]12)[/bold yellow] About")
        console.print("[bold yellow]13)[/bold yellow] Encode Secret Message (Testing Utility)")
        console.print("[bold red]0)[/bold red] Exit")
        
        choice = Prompt.ask("\n[bold green]StegX>[/bold green]", default="0")
        
        if choice == "1":
            file_path = Prompt.ask("[bold cyan]Enter path to target file[/bold cyan]")
            if os.path.exists(file_path):
                with console.status("[bold green]Analyzing file...[/bold green]"):
                    results = run_analysis(file_path)
                if results:
                    print_cli_report(results)
                    out_path = Prompt.ask("[bold cyan]Enter path to save JSON report[/bold cyan]", default="analysis.json")
                    save_json_report(results, out_path)
                    console.print(f"[bold green][+] Report saved to {out_path}[/bold green]")
                else:
                    console.print("[bold red][-] Analysis failed or file not supported.[/bold red]")
            else:
                console.print("[bold red][-] File not found![/bold red]")
                
        elif choice == "13":
            cover = Prompt.ask("[bold cyan]Enter path to cover image[/bold cyan]")
            msg = Prompt.ask("[bold cyan]Enter secret message[/bold cyan]")
            out = Prompt.ask("[bold cyan]Enter output path[/bold cyan]")
            if os.path.exists(cover):
                try:
                    with console.status("[bold green]Encoding message...[/bold green]"):
                        encode(cover, msg, out)
                    console.print(f"[bold green][+] Successfully encoded message to {out}[/bold green]")
                except Exception as e:
                    console.print(f"[bold red][-] Error encoding: {e}[/bold red]")
            else:
                console.print("[bold red][-] Cover image not found![/bold red]")
                
        elif choice == "0":
            console.print("[bold red]Exiting StegX...[/bold red]")
            sys.exit(0)
            
        else:
            console.print("[bold yellow][!] Feature currently in development or invalid option.[/bold yellow]")

def main():
    display_banner()
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting StegX...[/bold red]")
        sys.exit(0)

if __name__ == "__main__":
    main()
