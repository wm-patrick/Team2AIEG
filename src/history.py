#-----------IMPORTS-----------
import json
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()
LOG_FILE = "study_log.json"

#-----------FUNCTIONS-----------
def log_session(name: str, subject: str, method: str, content: str):
    """Saves the study session to a JSON file."""

#create a dictionary for the session entry
    entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "name": name,
                "subject": subject,
                "method": method,
                "content": content
            }

    #load existing data if available
    if os.path.exists(LOG_FILE):
        try: 
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError:
                data = [] #starts fresh if file is empty or invalid
    else:
        data = []

    #append the new entry to the data list
    data.append(entry)

    with open(LOG_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_last_sessions(limit: int =3):
    """Retrieves the log file and prints last n sessions."""
    if not os.path.exists(LOG_FILE):
        console.print("[italic yellow]No study log found.[/italic yellow]")
        return
    
    try:
         with open (LOG_FILE, 'r') as f:
            data = json.load(f)

    except json.JSONDecodeError:
        console.print("[bold red]Error reading history file.[/bold red]")
        return
    
    # Get the last 'limit' items (slicing)
    # data[-limit:] gets the last N items
    recent_sessions = data[-limit:]

    #Display the sessions
    console.print(f"\n[bold underline]Last {len(recent_sessions)} Study Sessions:[/bold underline]\n")

    for i, session in enumerate(reversed(recent_sessions), 1):
         #most recent session is first
         console.print(
              Panel(
                   f"[bold cyan]Subject:[/bold cyan]{session['subject']}\n"
                   f"[bold cyan]Method:[/bold cyan] {session['method']}\n"
                   f"[bold cyan]Timestamp:[/bold cyan]{session['timestamp']}\n"
                   f"[dim]Content Snippet:[/dim] {session['content'][:100]}...",
                   title=f"[bold]Session {i}[/bold]",
                   border_style="blue"

              )
         )

      



