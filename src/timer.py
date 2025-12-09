#!/usr/bin/env python3
"""
pomodoro_timer.py
Pomodoro Timer module for Pomodoro Study Buddy
"""

import time
import argparse
import sys

# Map timer types to durations in minutes
TIMER_MAP = {
    "pomodoro_15": 15,
    "pomodoro_25": 25,
    "deep_focus_45": 45
}

def run_timer(timer_type: str):
    """Run the Pomodoro timer."""
    minutes = TIMER_MAP.get(timer_type, 25)  # default to 25 min
    seconds = minutes * 60
    print(f"Starting Pomodoro Timer: {minutes} minutes ({timer_type})")
    
    try:
        while seconds > 0:
            mins, secs = divmod(seconds, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            print(f"\rTime Remaining: {time_format}", end="")
            time.sleep(1)
            seconds -= 1
        print("\n⏰ Time's up! Take a break or start next session.")
    except KeyboardInterrupt:
        print("\n⏹ Timer stopped by user.")
        sys.exit(0)

def pomodoro_arg_func(argv=None):
    parser = argparse.ArgumentParser(
        description="Pomodoro Timer CLI for Pomodoro Study Buddy"
    )
    parser.add_argument(
        "--timer",
        type=str,
        choices=list(TIMER_MAP.keys()),
        default="pomodoro_25",
        help="Select timer type (pomodoro_15, pomodoro_25, deep_focus_45)"
    )
    args = parser.parse_args(argv)
    run_timer(args.timer)

if __name__ == "__main__":
    pomodoro_arg_func()
