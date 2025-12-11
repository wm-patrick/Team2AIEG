import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

HISTORY_FILE = "session_history.json"
console = Console()

def load_history():
    """Loads session history from a JSON file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        console.print("[bold red]Warning: History file corrupted. Starting new log.[/bold red]")
        return []
    except Exception as e:
        console.print(f"[bold red]Error loading history:[/bold red] {e}")
        return []
  def save_history(history):
    """Saves the current session history to a JSON file."""
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        console.print(f"[bold red]Error saving history:[/bold red] {e}")

def log_session(name: str, subject: str, method: str, response: str):
    """
    Logs a completed study session with the generated AI material.
    
    NOTE: The full AI response is truncated for logging to keep the history file small.
    """
    history = load_history()
    
    session_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "subject": subject,
        "method": method,
        # Truncate long responses for the log file
        "material_preview": response[:200].replace('\n', ' ') + "...",
    }
    
    history.insert(0, session_entry) # Insert at the beginning (newest first)
    save_history(history)

def get_last_sessions(limit: int = 5):
    """Displays the last N logged study sessions."""
    history = load_history()
    
    if not history:
        console.print("\n[bold yellow]No past sessions found in history.[/bold yellow]")
        return
    
    console.print(Panel(
        f"[bold blue]--- Last {min(limit, len(history))} Study Sessions ---[/bold blue]",
        border_style="blue"
    ))
    
    for i, session in enumerate(history[:limit], 1):
        console.print(f"[bold cyan]{i}. {session['timestamp']}[/bold cyan]")
        console.print(f"  [dim]User:[/dim] {session.get('name', 'N/A')}")
        console.print(f"  [dim]Subject/Method:[/dim] {session.get('subject', 'N/A')} ({session.get('method', 'N/A')})")
        console.print(f"  [dim]Material Preview:[/dim] {session.get('material_preview', 'N/A')}\n")         