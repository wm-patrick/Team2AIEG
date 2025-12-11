#------------------------IMPORTS GO HERE------------------------------------
import argparse
import sys
import os
import json
from dotenv import load_dotenv
from google import genai
# Assuming these local imports are in place and correct
from src.rules import study_mode
from src.timer import pomodoro_arg_func
from src.history import log_session, get_last_sessions

#----- Rich Import-----#
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.markdown import Markdown
from rich.table import Table


#----Profile Mangement Constants ----
MAX_PROFILES = 3
PROFILES_FILE = "profiles.json"
VALID_METHODS = ['Quiz', 'Flashcards', 'Summary']	


#loading the environment variables
load_dotenv()

# Rich console 
console = Console()


api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
	raise RuntimeError(
		"key not found. Create .env file and add GEMINI_API_KEY to .env"
	)
else:
	console.print("[bold green]API key loaded successfully.[/bold green]")


#2. Create the Google GenAI client
client = genai.Client(api_key=api_key)

#------ Profile functions ----

def load_profiles():
	""" Loads existing study profiles from the JSON file """
	if not os.path.exists(PROFILES_FILE):
		return {}
	try:
		with open(PROFILES_FILE, 'r') as f:
			return json.load(f)
	except json.JSONDecodeError:
		console.print("[bold yellow]Warning:[/bold yellow] Profile file is not working. Starting with a new profile.")
		return {}


def save_profiles(profiles):
	""" Saves the current dictionary of Profiles to JSON file"""
	with open(PROFILES_FILE, 'w') as f:
		json.dump(profiles, f, indent=4)


def delete_profile(profiles):
	"""Prompts the user to select and delete a profile that exists"""
	if not profiles:
		console.print("[bold yellow]No profiles to delete.[/bold yellow]")
		return profiles

	console.print("\n[bold red]==== Select a Profile to delete ====[/bold red]")	
	profile_keys = list(profiles.keys())

	table_display = Table(title ="Available Profiles", show_header = True, header_style = "bold magenta")
	table_display.add_column("#" , style="dim", width=3)
	table_display.add_column("Name", style="cyan")
	table_display.add_column("Subject", style="green")
	table_display.add_column("Method", style="yellow")	
	
	for i, name in enumerate(profile_keys, 1):
		profile_data = profiles[name]
		table_display.add_row(
            str(i), 
            profile_data.get('name', 'N/A'), 
            profile_data.get('subject', 'N/A'), 
            profile_data.get('method', 'N/A')
        )
	console.print(table_display)

	while True:
		try:
			choice = Prompt.ask("Enter the number of the profile to delete (or 'c' to cancel): ")
			if choice.lower() == 'c':
				console.print("Deletion cancelled.")
				return profiles

			index = int(choice) - 1
			if 0 <= index < len(profile_keys):
				deleted_name = profile_keys[index]
				del profiles[deleted_name]
				save_profiles(profiles)
				console.print(f"[bold green]Profile '{deleted_name}' deleted successfully.[/bold green]")
				return profiles
			else:
				console.print("[bold red]Invalid number. Please try again.[/bold red]")
		except ValueError:
			console.print("[bold red]Invalid input.[/bold red] Please enter a number or 'c'.")
            
	return profiles


def select_profile_to_load(profiles):
	""" Prompts the user to select and load an existing profile """
	if not profiles:
		console.print("[bold yellow]No saved profiles found.[/bold yellow] Starting new session.")			 
		return None


	console.print("\n[bold blue]===== Select a Profile to load ===[/bold blue]")
	profile_keys = list(profiles.keys())

	table_display = Table(title="Available Profiles", show_header=True, header_style="bold magenta")
	table_display.add_column("#", style="dim", width=3)
	table_display.add_column("Name", style="cyan")
	table_display.add_column("Subject", style="green")
	table_display.add_column("Method", style="yellow")


	for i, name in enumerate(profile_keys, 1):
		profile_data = profiles[name]
		table_display.add_row(
			str(i),
			profile_data.get('name', 'N/A'),
			profile_data.get('subject', 'N/A'),
			profile_data.get('method', 'N/A')
		)
	console.print(table_display)

	while True:
		try:
			choice = Prompt.ask("Enter the number of the profile to load (or 'c' to cancel): ")
			if choice.lower() == 'c':
				console.print("Loading cancelled. Starting new session.")
				return None

			index = int(choice) - 1
			if 0 <= index < len(profile_keys):
				profile_key = profile_keys[index]
				console.print(f"[bold green]Profile '{profile_key}' loaded successfully.[/bold green]")
				return profiles[profile_key]
			else:
				console.print("[bold red]Invalid number. Please try again.[/bold red]")
		except ValueError:
			console.print("[bold red]Invalid input.[/bold red] Please enter a number or 'c'.")
            
	return None

def load_or_create_profile(profiles):
	""" Prompts user to load, create, delete a profile, or check history using numbered options. """
    
	options_map = {
		"1": "Start new session",
		"2": "Load existing profile",
		"3": "Review Past Sessions",
	}
	if profiles:
		options_map["4"] = "Delete existing profile"
        
	# Display options to the user
	console.print("\n[bold]Please make a selection from the menu options below:[/bold]")
	for key, value in options_map.items():
		console.print(f"[{key}]. [cyan]{value}[/cyan]")
        
	choices = list(options_map.keys())
    
    # Use Prompt.ask for numbered selection
	while True:
		choice = Prompt.ask("Enter selection (1, 2, 3...)", choices=choices, case_sensitive=False)
		
		selected_option = options_map.get(choice)
		
		if selected_option == "Load existing profile":
			return select_profile_to_load(profiles)
		elif selected_option == "Review Past Sessions":
			get_last_sessions(limit=3)
			# After reviewing history, re-prompt the user
			return load_or_create_profile(profiles)
		elif selected_option == "Delete existing profile":
			delete_profile(profiles)
			# After deletion, re-prompt the user
			return load_or_create_profile(profiles)
		elif selected_option == "Start new session":
			return None # Start new session
		
		else:
			console.print("[bold red]Invalid selection. Please try again.[/bold red]")
	


def build_prompt(name: str, method: str, subject: str) -> str:
    """This function builds the prompt that is sent to LLM"""
    
    prompt = f"""
Your role is to act as a friendly tutor or instructor.

The student's name is below. The student's method of learning is also below.

Name: {name}
Method: {method}
Subject: {subject}

1. Confirm to the user in a friendly and encouraging way their name and method of study.
2. Then, generate that method of study for the user.
3. If you are unsure about the subject material, do NOT guess; clearly say that you are unsure.
4. If the method is "Quiz", generate 5 multiple-choice questions (with 4 options each) about the subject.
5. If the method is "Flashcards", generate 5 flashcards (with question on the front and answer on the back).
6. If the method is "Quiz", generate answers after the questions.

"""
    return prompt.strip()


def get_study_materials(prompt: str) -> str:
	""" Call Gemini to generate studying materials. """

	try:
		response = client.models.generate_content(
			model="gemini-2.5-flash",
			contents=prompt
		)
		return response.text

	except Exception as e:
		console.print(f"[bold red]Error generating study materials: {e}[/bold red]")
		console.print(f"Technical details are as follows: {str(e)}")
		return "Error generating study materials. AI service is unavailable at this time."

def parse_args():
	parser = argparse.ArgumentParser(
		description=(
		    "Pomodoro Study Buddy: suggests a study mode and can ask an LLM to generate study materials."
        )
	)

	parser.add_argument(
		'--name',
		help="Your name (optional; will be asked if not provided).",
		default=None,
	)
	parser.add_argument(
		'--method',
		help="Study method: Quiz, Flashcards, or Summary (optional; will be asked if not provided).",
		default=None,		
	)
	parser.add_argument(
		'--subject',
		help="Subject you are studying (optional; will be asked if not provided).",
		default=None,
	)
	# This shows at the bottom of --help
	parser.epilog = "Typical run command: python -m src.app"

	return parser.parse_args()


def main():

	"""Main function: Contains the CLI"""

    # initialize the parser
	args = parse_args()
	profiles = load_profiles()
	session_data = None

	console.clear()
	console.print(Panel.fit(
		"[bold green]==== 🍅 WELCOME TO THE POMODORO STUDY BUDDY 🍅 ====[/bold green]\n"
		"[italic]Study smarter with AI-powered study mode suggestions and material generation![/italic]",
		border_style = "green" 
	))

	# ---- Load or create profile/select option ---- 
	session_data = load_or_create_profile(profiles)
    
    # --- Data Setup (Initialize with defaults) ---
	name = None
	method = None
	subject = None
	state = None
	minutes = 0
	source_type = "CLI/New"

	if session_data:
        # Load data from a selected profile
		console.print("[bold green]Session data loaded from profile.[/bold green]")
		name = session_data.get('name')
		method = session_data.get('method')
		subject = session_data.get('subject')
		state = session_data.get('state')
		minutes = session_data.get('minutes', 30)
		source_type = session_data.get('source', 'CLI/Loaded')	

		console.print(f"[dim]Loaded: Name: {name}, Method: {method}, Subject: {subject}, State: {state}, Minutes: {minutes}, Source: {source_type}[/dim]")

	else: 
        # Start new session, falling back to CLI args then prompts
		name = args.name or Prompt.ask("What is your [bold]name[/bold]? ")

		method = args.method
        # Normalizing method casing from CLI arg
		if method and method.capitalize() in VALID_METHODS:
			method = method.capitalize()
		else:
            # If not provided via CLI or invalid, prompt the user
			method = Prompt.ask(
				"Choose your study method",
				choices=VALID_METHODS, case_sensitive=False
			).capitalize()
			
		subject = args.subject or Prompt.ask("What [bold]subject[/bold] are you studying? ")
		state = None # State and minutes will be prompted below
		source_type = "CLI/New"
        
#---- Get User State and available Minutes-----
if not state:
	state = Prompt.ask(
		"What is your current state of energy today?",
		choices=["Tired", "Focused", "Overwhelmed", "Exhausted"],
		case_sensitive = False).capitalize()
else: 
	console.print(f"[dim]Loaded state: {state}[/dim]")

minutes = session_data.get('minutes', 0) if session_data else 0

if minutes <= 0:
	while True:
		minutes = IntPrompt.ask("How many minutes do you have available to study today? (Enter a positive integer)")
		if minutes > 0:
			break
		else:
			console.print("[bold red]Please enter a valid positive number for minutes.[/bold red]")
else:
	console.print(f"[dim]Loaded minutes: {minutes}[/dim]")

#-----Study Mode Suggestion -----
# 3 part tuple (mode_desc, work_min, break_min)
mode_desc, work_min, break_min = study_mode(state, minutes)

console.print(f"\n[bold blue]Suggested Study Mode:[/bold blue] {mode_desc}\n")


prompt = build_prompt(name, method, subject)

#--- Shows user .... animation while waiting------
with console.status("[bold green]Generating study materials...[/bold green]", spinner="dots"):
	response = get_study_materials(prompt)

console.print(Panel(
	Markdown(response),
	title= f"[bold green]Your Study Materials generated for {subject}[/bold green]",
	border_style = "blue"
))
# ---- Logs session after getting materials -----
log_session(name, method, subject, state, minutes, source_type)
console.print("[dim italic]Session successfully saved to history.[/dim italic]")

#----- Saving Profile Section -----
current_profile_key = f"{name}_{method}_{subject}".replace(' ', '_')

if current_profile_key not in profiles and len(profiles) < MAX_PROFILES:
	if Confirm.ask("Do you want to save this session as a profile?"):
		new_profile = {
			"name": name,
			"state": state,
			"method": method,
			"subject": subject,
			"source": source_type,
			"minutes": minutes
		}
		profiles[current_profile_key] = new_profile
		save_profiles(profiles)
		console.print(f"[bold green]Profile '{current_profile_key}' saved successfully.[/bold green]")
elif len(profiles) >= MAX_PROFILES and current_profile_key not in profiles:
	console.print(f"\n[bold red]Cannot save profile. Maximum number of profiles reached ({MAX_PROFILES}).[/bold red]")	
else:
	console.print("\n[dim italic]Note: This session matches an existing profile. Saving is skipped.[/dim]")

# Pomodoro Timer Logic
if work_min > 0:
    if Confirm.ask(f"\n[bold green]Do you want to start the Pomodoro timer now (Work: {work_min} min, Break: {break_min} min)?[/bold green]"):
        pomodoro_arg_func(work_min, break_min)
        # If the timer runs, the program will continue to the final exit message below.
    else:
        # If user says NO, print the "Happy Studying" conclusion immediately and exit.
        console.print("[dim]Skipping timer...[/dim]")
        console.print("\n[bold green]Happy Studying! No timer initiated. 🍅[/bold green]")
        sys.exit(0)
else:
    # If mode_desc suggests only rest (e.g., work_min=0)
    console.print(f"\n[bold blue]Suggested Mode: {mode_desc}. Since you are {state}, taking a break is recommended.[/bold blue]")
    # Exit here as the materials were provided but the recommendation is to rest/not study now.
    console.print("\n[bold green]Happy Studying! You deserve a break. 🍅[/bold green]")
    sys.exit(0)

# This final block is only reached if the timer was initiated and completed.
console.print("\n[bold green]Happy Studying! 🍅[/bold green]")

	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		console.print("\n[bold red]Goodbye! See you next time. Program exiting...[/bold red]")
		sys.exit(0)
