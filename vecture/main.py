"""
Vecture Redact CLI Interface
----------------------------
The operator terminal for Vecture Redact.
Exposes the 'redact' and 'restore' directives to the user.
Manages the injection of silence and the reconstruction of reality.

Origin: VECTURE LABORATORIES
"""

import typer
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

from .core import VectureRedactor

app = typer.Typer(help="Vecture Redact: Public Redaction, Private Reality.")
console = Console()

@app.command()
def redact(
    file_path: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to the file to redact."),
    style: str = typer.Option("CLASSIC", help="Redaction style: CLASSIC, BLACKOUT, VECTURE_NOISE"),
    words: Optional[Path] = typer.Option(None, exists=True, dir_okay=False, help="Path to a .txt file with custom words to redact (one per line)."),
    capitals: bool = typer.Option(False, help="Enable heuristic redaction of capitalized words."),
    obfuscate_key: bool = typer.Option(False, help="Obfuscate the generated key file so it's not human-readable."),
    output: Optional[Path] = typer.Option(None, help="Custom output path for the redacted file.")
):
    """
    [BOLD]OPERATION: REDACT[/BOLD]
    
    Scans a target file for sensitive information and excises it.
    Generates a sanitized public file and a private restoration key.
    """
    console.print(Panel.fit("[bold red]VECTURE REDACT[/bold red] v1.0", border_style="red"))

    # Ingest Suppression List
    custom_word_list = []
    if words:
        try:
            custom_word_list = words.read_text(encoding='utf-8').splitlines()
            custom_word_list = [w.strip() for w in custom_word_list if w.strip()]
            console.print(f"[green]Loaded {len(custom_word_list)} custom words.[/green]")
        except Exception as e:
            console.print(f"[bold red]Error reading words file:[/bold red] {e}")
            raise typer.Exit(code=1)

    # Acquire Target Asset
    try:
        text = file_path.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[bold red]Error reading source file:[/bold red] {e}")
        raise typer.Exit(code=1)

    redactor = VectureRedactor()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Scanning and Redacting...", total=None)
        
        # Execute Redaction Protocol
        redacted_text, key_data = redactor.redact(
            text, 
            style=style, 
            custom_words=custom_word_list, 
            redact_caps=capitals
        )

    # Calculate Artifact Trajectories
    if output:
        out_path = output
    else:
        out_path = file_path.with_name(f"{file_path.stem}_redacted{file_path.suffix}")
    
    key_path = out_path.with_suffix(out_path.suffix + ".vecture")

    # Commit Sanitized Asset
    try:
        out_path.write_text(redacted_text, encoding='utf-8')
        console.print(f"[bold green]✔ Redacted file saved to:[/bold green] {out_path}")
    except Exception as e:
        console.print(f"[bold red]Error writing redacted file:[/bold red] {e}")
        raise typer.Exit(code=1)

    # Generate Vecture Key
    try:
        if obfuscate_key:
            key_content = redactor.obfuscate_key(key_data)
        else:
            key_content = import_json_dumps(key_data)
            
        key_path.write_text(key_content, encoding='utf-8')
        console.print(f"[bold yellow]🔑 Key file saved to:[/bold yellow] {key_path}")
        if obfuscate_key:
             console.print("[dim](Key is obfuscated)[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error writing key file:[/bold red] {e}")
        # Try to cleanup redacted file so we don't leave a half-state
        out_path.unlink(missing_ok=True)
        raise typer.Exit(code=1)

@app.command()
def restore(
    redacted_file: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to the redacted file."),
    key_file: Path = typer.Argument(..., exists=True, dir_okay=False, help="Path to the .vecture key file."),
    output: Optional[Path] = typer.Option(None, help="Custom output path for the restored file.")
):
    """
    [BOLD]OPERATION: RESTORE[/BOLD]
    
    Reconstructs the original reality from a redacted file using a valid Vecture Key.
    Verifies cryptographic integrity before proceeding.
    """
    console.print(Panel.fit("[bold green]VECTURE RESTORE[/bold green]", border_style="green"))

    # Ingest Artifacts
    try:
        r_text = redacted_file.read_text(encoding='utf-8')
        k_text = key_file.read_text(encoding='utf-8')
    except Exception as e:
        console.print(f"[bold red]Error reading files:[/bold red] {e}")
        raise typer.Exit(code=1)

    redactor = VectureRedactor()

    # Decrypt Key Data
    try:
        key_data = redactor.deobfuscate_key(k_text)
    except ValueError as e:
        console.print(f"[bold red]Invalid Key File:[/bold red] {e}")
        raise typer.Exit(code=1)

    # Execute Restoration Protocol
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Verifying and Restoring...", total=None)
        
        try:
            original_text = redactor.restore(r_text, key_data)
        except ValueError as e:
            console.print(f"[bold red]Restoration Failed:[/bold red] {e}")
            raise typer.Exit(code=1)

    # Commit Restored Reality
    if output:
        out_path = output
    else:
        # Heuristic Naming Convention: 
        # file_redacted.md -> file_restored.md
        # file.md -> file_restored.md
        if "_redacted" in redacted_file.stem:
            clean_stem = redacted_file.stem.replace("_redacted", "_restored")
            out_path = redacted_file.with_name(clean_stem + redacted_file.suffix)
        else:
            out_path = redacted_file.with_name(f"{redacted_file.stem}_restored{redacted_file.suffix}")

    try:
        out_path.write_text(original_text, encoding='utf-8')
        console.print(f"[bold green]✔ Restored file saved to:[/bold green] {out_path}")
    except Exception as e:
        console.print(f"[bold red]Error writing output:[/bold red] {e}")
        raise typer.Exit(code=1)

def import_json_dumps(data):
    import json
    return json.dumps(data, indent=2)

if __name__ == "__main__":
    app()
