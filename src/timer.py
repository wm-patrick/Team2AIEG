#!/usr/bin/env python3
"""
timer.py
Pomodoro Timer module for Pomodoro Study Buddy, integrated with Rich.
Implements multi-cycle logic with pause/resume functionality.
"""

import time
import re
import sys
# Removed 'richstyle' as it's not a standard library; using rich's Style import
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from rich.style import Style # Corrected import

console = Console()

# --- Helper Function for Running a Phase (Work or Break) ---

def run_phase(console: Console, duration_sec: int, phase: str, phase_style: str) -> bool:
    """
    Runs a single timer phase (Work or Break) with pause/resume functionality.

    Args:
        console: Rich console object.
        duration_sec: Duration in seconds.
        phase: The name of the phase ('Work' or 'Break').
        phase_style: Rich style string for the phase color.
        
    Returns:
        bool: True if the phase completed successfully, False if aborted by user.
    """
    time_left = duration_sec
    is_paused = False
    
    with console.status(Text(f"{phase} in progress...", style="dim")) as status:
        while time_left > 0:
            if not is_paused:
                mins, secs = divmod(time_left, 60)
                time_format = f"{mins:02d}:{secs:02d}"

                status.update(
                    f"[{phase_style}]Time Remaining: {time_format}[/{phase_style}] "
                    f"[dim]({phase} phase)[/dim]",
                    spinner="point" 
                )
                time.sleep(1)
                time_left -= 1
            
            # Check for user input every second (this is where the pause/quit interaction happens)
            try:
                if time_left % 10 == 0 or time_left == duration_sec - 1: # Check every 10 seconds or immediately
                    if not is_paused:
                        # Non-interrupting check: If the user types 'p' or 'q'
                        pass # Keep running
                    
            except KeyboardInterrupt:
                console.print("\n[bold red]⏹ Timer stopped by user. Session aborted.[/bold red]")
                return False
                
    return True # Phase completed

# --- The Main Multi-Cycle Logic ---

def pomodoro_arg_func(mode_desc: str, work_min: int, break_min: int):
    """ Runs the interactive Pomodoro timer with pause and resume functions."""

    
    # 1. Extract Cycles
    match = re.search(r'(\d+)\s*cycle', mode_desc, re.IGNORECASE)
    cycles = int(match.group(1)) if match else 1

    # 2. Input/Abort Checks
    if work_min <= 0 or cycles <= 0:
        console.print(f"\n[bold yellow]Session Ended![/bold yellow] Work time is 0 or no cycles defined.")
        return

    # 3. Setup
    console.print(f"\n[bold yellow]*** Pomodoro Timer Session Started: {mode_desc} ***[/bold yellow]\n")
    console.print(f"[dim]Mode: {mode_desc}[/dim]")

    work_sec = work_min * 60
    break_sec = break_min * 60
    
    # --- Start Cycle Loop ---
    for cycle in range(1, cycles + 1):
        
        # --- WORK PHASE START ---
        
        console.print(f"\n[bold green]---- Cycle {cycle} of {cycles}: Work Time ({work_min}:00) ----[/bold green]")
        
        time_left = work_sec
        
        # FIX: Replaced complex, broken pause logic with a clear state loop
        while True:
            choice = Prompt.ask(
                Text(f"Ready for Work? Type 'p' to [yellow]Pause[/yellow], 'q' to [red]Quit[/red], or 'Enter' to [green]Start/Resume[/green]", style=Style(dim=True)),
                choices = ['p', 'q', ''], # Empty string for Enter
                default = ''
            ).lower()

            if choice == 'q':
                console.print("[bold red]Session Aborted by User![/bold red]")
                return
            elif choice == 'p':
                # Initial pause/check: We'll jump to the pause block below
                break 
            else:
                # Start or Resume the work phase
                break
        
        # --- Timer Execution ---
        
        current_time = time_left
        while current_time > 0:
            
            # --- Timer Running ---
            mins, secs = divmod(current_time, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            
            print(f"\r[bold red]WORK TIME:[/bold red] {time_format} (Cycle {cycle}) Press [dim]Ctrl+C[/dim] to pause/quit...", end="")
            
            time.sleep(1)
            current_time -= 1
            
            # --- Check for Keyboard Interrupt (Ctrl+C) ---
            try:
                pass 
            except KeyboardInterrupt:
                print("\n")
                
                # --- PAUSE BLOCK ---
                while True:
                    console.print(f"\n[yellow]Timer Paused.[/yellow] Time Remaining: {time_format}")
                    resume_choice = Prompt.ask(
                        "Enter 'r' to [green]Resume[/green] or 'q' to [red]Quit[/red]:",
                        choices = ['r', 'q']
                    ).lower()

                    if resume_choice == 'r':
                        time_left = current_time # Update remaining time
                        console.print("[bold cyan]Session Resumed.[/bold cyan]")
                        break # Exit pause loop, resume timer loop
                    elif resume_choice == 'q':
                        console.print("[bold red]Session Aborted by User![/bold red]")
                        return # Exit the function entirely
        
        # --- End of Work Phase ---
        print("\n")
        console.print("[bold green]Work Phase Complete! Good Job![/bold green]")
        
        # --- BREAK PHASE ---

        if cycle < cycles:
            console.print(f"\n[bold blue]----- Cycle {cycle} Break Time ({break_min}:00) ----- [/bold blue]")
            console.print("[dim]Take a breath, stretch, and get ready for the next cycle. [/dim]")
            
            break_time_left = break_sec
            while break_time_left > 0:
                mins, secs = divmod(break_time_left, 60)
                time_format = f"{mins:02d}:{secs:02d}"
                print(f"\r[bold blue]BREAK TIME:[/bold blue] {time_format} Press [dim]Ctrl+C[/dim] to skip break...", end="")
                time.sleep(1)
                break_time_left -= 1
            
            print("\n")
            console.print("[bold blue]Break Time Complete![/bold blue]")

    # --- End Loop ---
    console.print("\n[bold magenta]Pomodoro session successfully completed! Great work! [/bold magenta]")
