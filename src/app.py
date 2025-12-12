# ============================IMPORTS==================================
import argparse
import json
import os
import sys
from dotenv import load_dotenv
from typing import Dict, Optional, Tuple
from google import genai
#-------------------------LOCAL IMPORTS --------------------------------
from src.history import get_last_sessions, log_session
from src.rules import study_mode
from src.timer import pomodoro_arg_func

#-------------------------RICH IMPORTS --------------------------------------
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, IntPrompt, Prompt
from rich.table import Table
#============================END OF IMPORTS==========================

#-------------------------GLOBAL CONSTANTS-------------------------------#
MAX_PROFILES = 3
PROFILES_FILE = "profiles.json"
VALID_METHODS = ["Quiz", "Flashcards", "Summary"]


load_dotenv()
console = Console()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
	raise RuntimeError("API key not found. Create a .env file and add GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

#============================FUNCTIONS===============================

#============================PROFILE MANAGEMENT===============================

#--------- Profile Load/Save/Delete Functions-------------

def load_profiles() -> Dict[str, dict]:
	if not os.path.exists(PROFILES_FILE):
		return {}
	try:
		with open(PROFILES_FILE, "r") as f:
			return json.load(f)
	except json.JSONDecodeError:
		console.print("[bold yellow]Warning:[/bold yellow] Profile file is not readable. Starting fresh.")
		return {}

def save_profiles(profiles: Dict[str, dict]) -> None:
	with open(PROFILES_FILE, "w") as f:
		json.dump(profiles, f, indent=4)

def delete_profile(profiles: Dict[str, dict]) -> Dict[str, dict]:
	if not profiles:
		console.print("[bold yellow]No profiles to delete.[/bold yellow]")
		return profiles

	console.print("\n[bold red]==== Select a Profile to delete ====[/bold red]")
	keys = list(profiles.keys())
	table = Table(title="Available Profiles", show_header=True, header_style="bold magenta")
	table.add_column("#", style="dim", width=3)
	table.add_column("Name", style="cyan")
	table.add_column("Subject", style="green")
	table.add_column("Method", style="yellow")

	for i, k in enumerate(keys, 1):
		p = profiles[k]
		table.add_row(str(i), p.get("name", "N/A"), p.get("subject", "N/A"), p.get("method", "N/A"))

	console.print(table)

	while True:
		choice = Prompt.ask("Enter the number of the profile to delete (or 'c' to cancel): ")
		if choice.lower() == "c":
			console.print("Deletion cancelled.")
			return profiles
		try:
			idx = int(choice) - 1
			if 0 <= idx < len(keys):
				name = keys[idx]
				del profiles[name]
				save_profiles(profiles)
				console.print(f"[bold green]Profile '{name}' deleted successfully.[/bold green]")
				return profiles
		except ValueError:
			console.print("[bold red]Invalid input.[/bold red] Please enter a number or 'c'.")

def select_profile_to_load(profiles: Dict[str, dict]) -> Optional[dict]:
	if not profiles:
		console.print("[bold yellow]No saved profiles found.[/bold yellow] Starting new session.")
		return None

	console.print("\n[bold blue]===== Select a Profile to load ===[/bold blue]")
	keys = list(profiles.keys())
	table = Table(title="Available Profiles", show_header=True, header_style="bold magenta")
	table.add_column("#", style="dim", width=3)
	table.add_column("Name", style="cyan")
	table.add_column("Subject", style="green")
	table.add_column("Method", style="yellow")

	for i, k in enumerate(keys, 1):
		p = profiles[k]
		table.add_row(str(i), p.get("name", "N/A"), p.get("subject", "N/A"), p.get("method", "N/A"))

	console.print(table)

	while True:
		choice = Prompt.ask("Enter the number of the profile to load (or 'c' to cancel): ")
		if choice.lower() == "c":
			console.print("Loading cancelled. Starting new session.")
			return None
		try:
			idx = int(choice) - 1
			if 0 <= idx < len(keys):
				key = keys[idx]
				console.print(f"[bold green]Profile '{key}' loaded successfully.[/bold green]")
				return profiles[key]
		except ValueError:
			console.print("[bold red]Invalid input.[/bold red] Please enter a number or 'c'.")
			
#----------------------- Profile Creation-------------------------------

def load_or_create_profile(profiles: Dict[str, dict]) -> Optional[dict]:
	options = {"1": "Start new session", "2": "Load existing profile", "3": "Review Past Sessions"}
	if profiles:
		options["4"] = "Delete existing profile"

	console.print("\n[bold]Please make a selection from the menu options below:[/bold]")
	for k, v in options.items():
		console.print(f"[{k}]. [cyan]{v}[/cyan]")

	choices = list(options.keys())
	while True:
		choice = Prompt.ask("Enter selection (Please choose: 1, 2, 3)", choices=choices, case_sensitive=False)
		selected = options.get(choice)
		if selected == "Load existing profile":
			return select_profile_to_load(profiles)
		if selected == "Review Past Sessions":
			get_last_sessions(limit=3)
			return load_or_create_profile(profiles)
		if selected == "Delete existing profile":
			delete_profile(profiles)
			return load_or_create_profile(profiles)
		if selected == "Start new session":
			return None

#------------------------- BUILD PROMPT FOR THE LLM -------------------------------#

def build_prompt(name: str, method: str, subject: str) -> str:
	prompt = f"""
Your role is to act as a friendly tutor or instructor. For the following user,
studying the specified subject who is studying using a specified method, generate appropriate study materials.

Name: {name}
Method: {method}
Subject: {subject}

1. Confirm the user's name and method in a friendly way.
2. Generate the requested study materials for the user.
3. If unsure about the subject, say you are unsure.
4. If method is "Quiz", generate 5 multiple-choice questions with 4 options.
5. If method is "Flashcards", generate 5 flashcards.
"""
	return prompt.strip()

#-----------------------GENERATE STUDY MATERIALS VIA LLM-------------------------------#

def get_study_materials(prompt: str) -> str:
    """Call Gemini to generate study materials."""
    # Safety check: if client failed to load above
    if not client:
        return "Error: API Client not initialized. Check API Key."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
        
    except Exception as e:
        console.print(f"[bold red]Error generating study materials: {e}[/bold red]")
        return "I apologize, but the AI service is currently unavailable. Please try again later."

def parse_args():
	parser = argparse.ArgumentParser(description="Pomodoro Study Buddy: suggests a study mode and can ask an LLM to generate study materials.")
	parser.add_argument("--name", help="Your name (optional).", default=None)
	parser.add_argument("--method", help="Study method: Quiz, Flashcards, or Summary (optional).", default=None)
	parser.add_argument("--subject", help="Subject you are studying (optional).", default=None)
	parser.epilog = "Typical run command: python -m src.app"
	return parser.parse_args()

#-------------------------MAIN FUNCTION-------------------------------#

def main():
	"""provides user interface for the Pomodoro Study Buddy application."""

	args = parse_args()
	profiles = load_profiles()
	session_data = None

	console.clear()
	console.print(Panel.fit("[bold green]==== 🍅 WELCOME TO THE POMODORO STUDY BUDDY 🍅 ====[/bold green]\n[italic]Study smarter with AI-powered suggestions.[/italic]", border_style="green"))

	session_data = load_or_create_profile(profiles)

	name = None
	method = None
	subject = None
	state = None
	minutes = 0
	source_type = "CLI/New"

	if session_data:
		console.print("[bold green]Session data loaded from profile.[/bold green]")
		name = session_data.get("name")
		method = session_data.get("method")
		subject = session_data.get("subject")
		state = session_data.get("state")
		minutes = session_data.get("minutes", 30)
		source_type = session_data.get("source", "CLI/Loaded")
		console.print(f"Loaded: Name: {name}, Method: {method}, Subject: {subject}, State: {state}, Minutes: {minutes}, Source: {source_type}", style="dim")
	else:
		name = args.name or Prompt.ask("What is your [bold]name[/bold]? ")
		method = args.method
		if method and method.capitalize() in VALID_METHODS:
			method = method.capitalize()
		else:
			method = Prompt.ask("Choose your study method", choices=VALID_METHODS, case_sensitive=False).capitalize()
		subject = args.subject or Prompt.ask("What [bold]subject[/bold] are you studying? ")

	if not state:
		state = Prompt.ask("What is your current state of energy today?", choices=["Tired", "Focused", "Overwhelmed", "Exhausted"], case_sensitive=False).lower()

	if session_data:
		minutes = session_data.get("minutes", 0)

	if not minutes or minutes <= 0:
		while True:
			minutes = IntPrompt.ask("How many minutes do you have available to study today? (Enter a positive integer)")
			if minutes > 0:
				break
			console.print("[bold red]Please enter a valid positive number for minutes.[/bold red]")

	# Convert state to our rules input expectations (lowercase)
	state_label = state.strip().lower() if isinstance(state, str) else state

	# study_mode now returns a simple label; map it back to a mode description and durations
	label = study_mode(state_label)
	mapping: Dict[str, Tuple[str, int, int]] = {
		"deep study": ("Deep study (45 min work/ 15 min break, 2 cycles)", 45, 15),
		"light review": ("Light review (10 min work / 2 min break, 1 cycle)", 10, 2),
		"basic check-in": ("Standard check-in (25 min work/ 5 min break, 1 cycle)", 25, 5),
	}

	mode_desc, work_min, break_min = mapping.get(label, mapping["basic check-in"])

	console.print(f"\n[bold blue]Suggested Study Mode:[/bold blue] {mode_desc}\n")

	prompt = build_prompt(name, method, subject)
	with console.status("[bold green]Generating study materials...[/bold green]", spinner="dots"):
		response = get_study_materials(prompt)

	console.print(Panel(Markdown(response), title=f"[bold green]Your Study Materials for {subject}[/bold green]", border_style="blue"))

	# Log session including the AI response preview
	log_session(name, method, subject, state_label, minutes, source_type, response=response)
	console.print("[dim italic]Session successfully saved to history.[/dim italic]")

	# Save profile if user wants
	current_profile_key = f"{name}_{method}_{subject}".replace(" ", "_")
	if current_profile_key not in profiles and len(profiles) < MAX_PROFILES:
		if Confirm.ask("Do you want to save this session as a profile?"):
			profiles[current_profile_key] = {
				"name": name,
				"state": state_label,
				"method": method,
				"subject": subject,
				"source": source_type,
				"minutes": minutes,
			}
			save_profiles(profiles)
			console.print(f"[bold green]Profile '{current_profile_key}' saved successfully.[/bold green]")
	elif len(profiles) >= MAX_PROFILES and current_profile_key not in profiles:
		console.print(f"\n[bold red]Cannot save profile. Maximum number of profiles reached ({MAX_PROFILES}).[/bold red]")
	else:
		console.print("\n[dim italic]Note: This session matches an existing profile. Saving is skipped.[/dim italic]")

	# Pomodoro Timer Logic
	if work_min > 0:
		if Confirm.ask(f"\n[bold green]Do you want to start the Pomodoro timer now (Work: {work_min} min, Break: {break_min} min)?[/bold green]"):
			pomodoro_arg_func(work_min, break_min)
		else:
			console.print("[dim]Skipping timer...[/dim]")
			console.print("\n[bold green]Happy Studying! No timer initiated. 🍅[/bold green]")
			sys.exit(0)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		console.print("\n[bold red]Goodbye! See you next time. Program exiting...[/bold red]")
		sys.exit(0)
