import json
import os
from datetime import datetime
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

HISTORY_FILE = "session_history.json"
console = Console()


def load_history() -> List[dict]:
    """Load session history from a JSON file.

    Returns an empty list when the file doesn't exist or is corrupted.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        console.print("[bold red]Warning: History file corrupted. Starting new log.[/bold red]")
        return []
    except Exception as e:
        console.print(f"[bold red]Error loading history:[/bold red] {e}")
        return []


def save_history(history: List[dict]) -> None:
    """Save the current session history to a JSON file."""
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        console.print(f"[bold red]Error saving history:[/bold red] {e}")


def log_session(
    name: str,
    method: str,
    subject: str,
    state: str,
    minutes: int,
    source_type: str,
    response: Optional[str] = None,
) -> None:
    """Log a completed study session with metadata.

    The optional `response` is truncated for storage as a preview.
    """
    history = load_history()

    preview_text = (response or "")[:200].replace("\n", " ")
    material_preview = preview_text + ("..." if response else "")

    session_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": name,
        "subject": subject,
        "method": method,
        "state": state,
        "minutes": minutes,
        "source": source_type,
        "material_preview": material_preview,
    }

    history.insert(0, session_entry)
    save_history(history)


def get_last_sessions(limit: int = 5) -> None:
    history = load_history()
    if not history:
        console.print("\n[bold yellow]No past sessions found in history.[/bold yellow]")
        return

    recent_sessions = history[:limit]

    console.print(
        Panel(f"[bold blue]--- Last {len(recent_sessions)} Study Sessions ---[/bold blue]", border_style="blue")
    )

    for i, session in enumerate(recent_sessions, 1):
        console.print(
            Panel(
                (
                    f"[bold cyan]Subject:[/bold cyan] {session.get('subject', 'N/A')}\n"
                    f"[bold cyan]Method:[/bold cyan] {session.get('method', 'N/A')}\n"
                    f"[bold cyan]Energy/Time:[/bold cyan] {session.get('state', 'N/A')} state, {session.get('minutes', 'N/A')} min\n"
                    f"[dim]Timestamp:[/dim] {session.get('timestamp', 'N/A')} (Source: {session.get('source', 'N/A')})\n"
                    f"[dim]Material Preview:[/dim] {session.get('material_preview', 'N/A')}"
                ),
                title=f"[bold]Session {i}[/bold]",
                border_style="blue",
            )
        )
