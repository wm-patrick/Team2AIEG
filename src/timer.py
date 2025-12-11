#!/usr/bin/env python3
"""
pomodoro_timer.py
Pomodoro Timer module for Pomodoro Study Buddy
"""

import time
import re
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from richstyle import Style

console = Console()

def pomodoro_arg_func(mode_desc: str), work_min: int, break_min: int):
    """ Runs the interactive Pomodoro timer with pause and resume functions. 

        Args:
            mode_desc (str): Description of the selected study mode(must include number of cycle needed).
            work_min (int): Duration of work session in minutes.
            break_min (int): Duration of break in minutes.

        Note: Cycles is extracted from mode_desc usinf regex.
        """
    match = re.search(r'(\d+)\s*cycle', mode_desc)

    if match:
        cycles = int(match.group(1))

    else:
        cycles = 1 # Default to 1 cycle if not specified by user

    if work_min <= 0 or cycles <= 0:
        console.print("f\n Session Ended! {mode_desc} /n")
        return 

    console.print(f"\n [bold yellow] *** Pomodoro Timer Session Started: {mode_desc} *** [/bold yellow]\n")
    console.print(f"[dim]Mode: {mode_desc}[/dim]")

    work_sec = work_min * 60
    break_sec = break_min * 60

    for cycle in range(1, cycles + 1):

        console.print(f"\n[bold green]---- Cycle {cycle} of {cycles}: Work time({work_min}:00-------[/bold green]")
    
        time_left = work_sec
        is_paused = False

        time.sleep(1)

# to pause timer
        pause_choice = Prompt.ask(
            Text(f"Work in progress. Type 'p'to [yellow]Pause[/yellow], 'q' to [red]Quit[/red], or 'Enter' to [green]Continue[/green]", style= Style(dim=True)),
            choices = ['p', 'P', 'c', 'C', 'q', 'Q'],
            default = 'c'
        ).lower()

        if pause_choice == 'p' or pause_choice== 'q'': 
            if pause_choice == 'q':
                console.print("[bold red]Session ended by User! [/bold red]")
                return
        is paused = True
        time_left = (time_left * 100) // 100 # Freeze time left

        console.print("[yellow]Timer Paused. Type 'r' to Resume or 'q' to Quit.[/yellow]".
        console.print(f"Time Remaining: {time_left // 60:02d}:{time_left % 60:02d}"))

        while is_paused:
            resume_choice = Prompt.ask(
                "Enter 'r' to [green]Resume[/green] or 'q' to [red]Quit[/red]:",
                choices = ['r', 'R', 'q', 'Q']

             if resume_choice== 'r':
                is_paused == False 
                console.print("[bold cyaan]Session Resumed. [/bold cyaan]")
            elif resume_choice == 'q':
                 console.print("[bold red]Session Aborted by user.[/bold red]")
                 return 
                
        console.print("[bold green]Work Phase Complete![/bold green]")

 # 2. For Breaks

        if cycle < cycles :
            console.print(f"\n [bold blue]----- Cycle {cycle} Break Time({break_min}:00)-------[/boldblue]")
            console.print("[dim]Take a breath, stretch, and get ready for the next cycle. [/dim]")

            time.sleep(1) 
    
    console.print("\n[bold magenta]Pomodoro session successfully completed! Great work! [/bold magenta]")
    

#---- END LOOP----#

