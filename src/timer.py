timer.py
#!/usr/bin/env python3
"""Pomodoro Timer module for Pomodoro Study Buddy, integrated with Rich.

Provides a simple interactive multi-cycle Pomodoro implementation with
pause/resume support via keyboard interrupts.
"""

import re
import time
from typing import Tuple

from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style

console = Console()


def pomodoro_arg_func(work_min: int, break_min: int, mode_desc: str = "1 cycle") -> None:
    """Run a Pomodoro session using the supplied work/break minutes.

    The optional `mode_desc` is used to infer cycles when it contains
    a 'N cycle(s)' fragment (e.g. '2 cycles').
    """

    match = re.search(r"(\d+)\s*cycle", mode_desc, re.IGNORECASE)
    cycles = int(match.group(1)) if match else 1

    if work_min <= 0 or cycles <= 0:
        console.print("\n[bold yellow]Session Ended![/bold yellow] Work time is 0 or no cycles defined.")
        return

    console.print(f"\n[bold yellow]*** Pomodoro Timer Session Started: {mode_desc} ***[/bold yellow]\n")
    console.print(f"[dim]Mode: {mode_desc}[/dim]")

    work_sec = work_min * 60
    break_sec = break_min * 60

    for cycle in range(1, cycles + 1):
        console.print(f"\n[bold green]---- Cycle {cycle} of {cycles}: Work Time ({work_min}:00) ----[/bold green]")

        # Ask user to start or abort
        choice = Prompt.ask(
            "Ready for Work? Type 'p' to Pause, 'q' to Quit, or press Enter to Start/Resume",
            choices=["p", "q", ""],
            default="",
        ).lower()

        if choice == "q":
            console.print("[bold red]Session Aborted by User![/bold red]")
            return

        current_time = work_sec
        try:
            while current_time > 0:
                mins, secs = divmod(current_time, 60)
                time_format = f"{mins:02d}:{secs:02d}"
                print(f"\rWORK TIME: {time_format} (Cycle {cycle}) Press Ctrl+C to pause/quit...", end="")
                time.sleep(1)
                current_time -= 1
        except KeyboardInterrupt:
            print("\n")
            # Pause loop
            while True:
                mins, secs = divmod(current_time, 60)
                time_format = f"{mins:02d}:{secs:02d}"
                console.print(f"\n[yellow]Timer Paused.[/yellow] Time Remaining: {time_format}")
                resume_choice = Prompt.ask("Enter 'r' to Resume or 'q' to Quit:", choices=["r", "q"]).lower()
                if resume_choice == "r":
                    console.print("[bold cyan]Session Resumed.[/bold cyan]")
                    try:
                        while current_time > 0:
                            mins, secs = divmod(current_time, 60)
                            time_format = f"{mins:02d}:{secs:02d}"
                            print(f"\rWORK TIME: {time_format} (Cycle {cycle}) Press Ctrl+C to pause/quit...", end="")
                            time.sleep(1)
                            current_time -= 1
                        break
                    except KeyboardInterrupt:
                        continue
                elif resume_choice == "q":
                    console.print("[bold red]Session Aborted by User![/bold red]")
                    return

        print("\n")
        console.print("[bold green]Work Phase Complete! Good Job![/bold green]")

        if cycle < cycles:
            console.print(f"\n[bold blue]----- Cycle {cycle} Break Time ({break_min}:00) -----[/bold blue]")
            console.print("[dim]Take a breath, stretch, and get ready for the next cycle.[/dim]")
            break_time_left = break_sec
            while break_time_left > 0:
                mins, secs = divmod(break_time_left, 60)
                time_format = f"{mins:02d}:{secs:02d}"
                print(f"\rBREAK TIME: {time_format} Press Ctrl+C to skip break...", end="")
                time.sleep(1)
                break_time_left -= 1
            print("\n")
            console.print("[bold blue]Break Time Complete![/bold blue]")

    console.print("\n[bold magenta]Pomodoro session successfully completed! Great work![/bold magenta]")

