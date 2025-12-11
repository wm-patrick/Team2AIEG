import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

HISTORY_FILE = "session_history.json"
console = Console()

#-----------FUNCTIONS-----------

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

def log_session(name: str, method: str, subject: str, state: str, minutes: int, source_type: str, response: str):
    """
    Logs a completed study session with all key metadata.
    The AI 'response' content is truncated for logging.
    """
    history = load_history()
    
    material_preview = Text.from_markup(response[:200]).plain.replace('\n', ' ') + "..."
    
    session_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "subject": subject,
        "method": method,
        "state": state,
        "minutes": minutes,
        "source": source_type,
        "material_preview": material_preview, # Store the truncated preview
    }
        history.insert(0, session_entry) 
    save_history(history)


def get_last_sessions(limit: int = 5):
    history = load_history()
    
    if not history:
        console.print("\n[bold yellow]No past sessions found in history.[/bold yellow]")
        return
    
    recent_sessions = history[:limit]

    console.print(Panel(
        f"[bold blue]--- Last {len(recent_sessions)} Study Sessions ---[/bold blue]",
        border_style="blue"
    ))
    
    for i, session in enumerate(recent_sessions, 1):
        console.print(
            Panel(
                f"[bold cyan]Subject:[/bold cyan] {session.get('subject', 'N/A')}\n"
                f"[bold cyan]Method:[/bold cyan] {session.get('method', 'N/A')}\n"
                f"[bold cyan]Energy/Time:[/bold cyan] {session.get('state', 'N/A')} state, {session.get('minutes', 'N/A')} min\n"
                f"[dim]Timestamp:[/dim] {session.get('timestamp', 'N/A')} (Source: {session.get('source', 'N/A')})\n"
                f"[dim]Material Preview:[/dim] {session.get('material_preview', 'N/A')}",
                title=f"[bold]Session {i}[/bold]",
                border_style="blue"
            )
        )   
