import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def print_cli_report(results):
    """
    Prints a rich CLI report based on analysis results.
    """
    if not results:
        console.print("[bold red][-] Error: Could not analyze file.[/bold red]")
        return
        
    console.print("\n[bold cyan]====================================[/bold cyan]")
    console.print("[bold cyan]StegX v1.0[/bold cyan]")
    console.print("[bold cyan]Advanced Steganography Analyzer[/bold cyan]")
    console.print("[bold cyan]====================================[/bold cyan]\n")
    
    info = results.get("file_info", {})
    file_table = Table(title="File Information", show_header=True, header_style="bold magenta")
    file_table.add_column("Property", style="cyan")
    file_table.add_column("Value", style="green")
    
    file_table.add_row("Target File", str(info.get("file_name", "N/A")))
    file_table.add_row("File Type", str(info.get("type", "N/A")))
    file_table.add_row("Size", str(info.get("size", "N/A")))
    file_table.add_row("SHA256", str(info.get("sha256", "N/A")))
    console.print(file_table)
    
    if results.get("metadata"):
        meta = results["metadata"]
        meta_table = Table(title="Metadata Analysis", show_header=True, header_style="bold magenta")
        meta_table.add_column("Status", style="cyan")
        meta_table.add_column("Details", style="green")
        
        if meta.get("status") == "Clean":
            meta_table.add_row("[bold green]Clean[/bold green]", str(meta.get('details', '')))
        else:
            meta_table.add_row(f"[bold red]{meta.get('status', 'Unknown')}[/bold red]", str(meta.get('details', '')))
        console.print(meta_table)
    else:
        console.print("[yellow][-] No metadata analyzed[/yellow]")

    if results.get("detections"):
        det_table = Table(title="Detection Results", show_header=True, header_style="bold magenta")
        det_table.add_column("Detector", style="cyan")
        det_table.add_column("Confidence", style="green")
        det_table.add_column("Raw Score", style="yellow")
        
        for det in results["detections"]:
            raw_score = f"{det['score']:.4f}" if "score" in det else "N/A"
            confidence = f"{det.get('confidence', 0)}%"
            
            conf_val = det.get('confidence', 0)
            if conf_val > 60:
                confidence = f"[bold red]{confidence}[/bold red]"
            elif conf_val > 30:
                confidence = f"[bold yellow]{confidence}[/bold yellow]"
            else:
                confidence = f"[bold green]{confidence}[/bold green]"
                
            det_table.add_row(str(det.get('name', 'Unknown')), confidence, raw_score)
            
        console.print(det_table)
        
    overall = results.get('overall_confidence', 0)
    if overall > 60:
        overall_str = f"[bold red]{overall}%[/bold red]"
    elif overall > 30:
        overall_str = f"[bold yellow]{overall}%[/bold yellow]"
    else:
        overall_str = f"[bold green]{overall}%[/bold green]"
        
    console.print(Panel(f"Overall Confidence: {overall_str}", title="Result", border_style="cyan"))
    
    if overall > 60:
        console.print("[bold red]\n[!] Likely Steganography Detected[/bold red]")
        console.print(f"[bold yellow]Technique:[/bold yellow] {results.get('technique', 'Unknown')}")
        
        if results.get("extraction"):
            ext = results["extraction"]
            ext_table = Table(title="Extraction Payload", show_header=True, header_style="bold magenta")
            ext_table.add_column("Property", style="cyan")
            ext_table.add_column("Value", style="green")
            ext_table.add_row("Payload Found", "Yes")
            ext_table.add_row("Type", str(ext.get("type", "N/A")))
            ext_table.add_row("Recovered", "Successfully")
            console.print(ext_table)
            
            safe_payload = repr(ext.get('data', ''))[:100]
            if len(ext.get('data', '')) > 100:
                safe_payload += "..."
            console.print(Panel(safe_payload, title="Payload", border_style="red"))
    else:
        console.print("[bold green]\n[+] Clean - No Steganography Detected[/bold green]")

    console.print("\n[bold cyan]====================================[/bold cyan]\n")

def save_json_report(results, output_path="analysis.json"):
    # If the provided path is a directory, append default file name
    if os.path.isdir(output_path) or output_path.endswith(('/', '\\')):
        output_path = os.path.join(output_path, "analysis.json")
        
    # Ensure the parent directory exists
    parent_dir = os.path.dirname(output_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
        
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
