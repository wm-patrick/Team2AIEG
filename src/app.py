#------------------------IMPORTS GO HERE------------------------------------
import argparse
import sys
import os
import json
from dotenv import load_dotenv
from google import genai
from src.rules import study_mode
from src.timer import pomodoro_arg_func
from src.history import log_session, get_last_sessions

#----- Rich Import-----#
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm, Select
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
		"key not found. Create .env file and add GEMINI_API_KEY TO .env"
	)
else:
	console.print("[bold green] API key loaded successfully.[/bold green]")


#2. Create the Google GenAI client
client = genai.Client(api_key=api_key)

#------ Profile funtions ----

def load_profiles():
	""" Loads existing study profiles from the JSON file """
	if not os.path.exists(PROFILES_FILE):
		return {}
	try:
		with open(PROFILES_FILE, 'r') as f:
			return json.load(f)
	except json.JSONDecodeError:
		console.print("[bold yellow] Warning: [\bold yellow] Profile not found. Starting with a new profile. ")
		return {}


def save_profiles(profiles):
	""" Saves the current dictionary of Profiles to JSON file"""
	with open(PROFILES_FILE, 'w') as f:
		json.dump(profiles, f, indent=4)


def delete_profile(profiles):
	"""Prompts the user to slect and delete a file that exists"""
	if not profiles:
		console.print("[bold yellow]No profiles to delete.[/bold yellow]")
		return profiles

	console.print("\n[bold red] ====Select a Profile to delete [/bold red]====")	
	profile_keys = list(profiles.keys())

	table = table(title ="Available Profiles", show_header = True, header_style = "bold magenta")
	table.add_column("#" , style="dim", width=3)
	table.add_column("Name, style="cyan")
	table.add_column("Subject", style="green")
	table.add_column("Method", style="yellow")	
	
	for i, name in enumerate(profile_keys, 1):
		profile_data = profiles[name]
		table.add_row(str(i), 
		profile_data.get('name', 'N/A'), 
		profile_data.get('subject', 'N/A'), 
		profile_data.get('method', 'N/A')
		)
	console.print(table)

	while True:
		try:
			#Rich Prompt for input
			choice = Prompt.ask("Enter the number of the profile to delete (or 'c' to cancel): ")
			if choice.lower() == 'c':
				console.print("Deletion cancelled.")
				return profiles

			index = int(choice) - 1
			if 0 <= index < len(profile_keys):
				deleted_name = profile_keys[index]
				del profiles[deleted_name]
				save_profiles(profiles)
				console.print(f"[bold green]Profile '{deleted_name}' delete succussful. [/bold green]")
				return profiles
			else:
				console.print("[bold red] Invalid number. Please try again. [/bold red]")
		except ValueError:
			console.print("[bold red] Invalid input.[/bold red] Please enter a number or 'c'. ")


def select_profile_to_load(profiles):
	""" Prompts the user to select and load an existing profile """
	if not profiles:
		console.print("[bold yellow]No saved profiles found.[/bold yellow] Starting new session.")			 
		return None


	console.print("\n[bold blue]===== Select a Profile to load ===[/bold blue]")
	profile_keys = list(profiles.keys())

	table = Table(title="Available Profiles", show_header=True, header_style="bold magenta")
	table.add_column("#", style="dim", width=3)
	table.add_column("Name", style="cyan")
	table.add_column("Subject", style="green")
	table.add_column("Method", style="yellow")


	for i, name in enumerate(profile_keys, 1):
		profile_data = profiles[name]
		table.add_row(
			str(i),
			profile_data.get('name', 'N/A'),
			profile_data.get('subject', 'N/A'),
			profile_data.get('method', 'N/A')
		)
	console.print(table)

	while True:
		try:
			choice = Prompt.ask("Enter the number of profiles to load ( or 'c' to cancel): ")
			if choice.lower() == 'c':
				console.print("loading cancelled. Starting new session.")
				return None

			index = int(choice) - 1
			if 0 <= index < len(profile_keys):
				profile_key = profile_keys[index]
				console.print(f"[bold green]Profile '{profile_key}' loaded successfuly.[/bold green]")
				return profiles[profile_key]
			else:
				console.print("[bold red]Invaild number. Please try again.[/bold red]")
		except ValueError:
			print("[bold red] Invalid input.[/bold red] Please enter a number or 'c'.")

def load_or_create_profile(profiles):
	""" Prompts user to load, create or delete a profile """
	options ={
		"1": "Start new session",
		"2": "Load existing profile",
	}
	if profiles:
		options["3"] = "Delete existing profile"

	choice = select.ask(
		"Choose an option:",
		choices=list(options.values()),
		default="Start new session"
	)

	if choice == "Load existing profile":
		return select_profile_to_load(profiles)
	elif choice.startswith ("Delete existing profile") :
		delete_profile(profiles)
		return load_or_create_profile(profiles)
	else:
		return None #Start new session#	
	


"""This function builds the prompt that is sent to LLM"""



def build_prompt(name: str, method: str , subject: str): -> str:

	prompt = (f""" Your role is to act as a friendly tutor or instructor.
	
	The student's name is below. The student's method of learning is also below.
	
	Name: {name}
	Method: {method}
	Subject: {subject}
	
	1. Confirm to the user in a friendly and encouraging way their name and method of study. 
	2. Then, generate that method of study for the user.
	3. If you are unsure about the subject material, do NOT guess; clearly say that you are unsure.
	4. If the method is "Quiz", generate 5 multiple-choice questions (with 4 options each) about the subject.
	5. If the method is "Flashcards", generate 5 flashcards (with question on
	6. If the method is "Quiz", generate answers after the questions. 

	"""
	
	return prompt.strip()



def get_study_materials(prompt: str) -> str:
	""" Call Gemini to generat studying materials. """

	try:
    	response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text

	except Exception as e:
		console.print(f"[bold red]Error generating study materials: {e}[/bold red
		console.print(f" Technical details are as follows: {str(e)}")
		return "Error generating study materials. AI service is unavailable at this time."

def parse_args():
	parser = argparse.ArgumentParser(
		description=
		 ("Pomodoro Study Buddy: suggests a study mode and can ask an LLM to generate study materials.")
		
	)

	parser.add_argument(
		'--name',
		help = " Your name (optional; will be asked if not provided).",
		default=None,
	)
	parser.add_argument(
		'--method',
		help=" Study method: Quiz, Flashcards, or Summary (optional; will be asked if not provided).",
		default=None,		
	)
	parser.add_argument(
		'--subject',
		help=" Subject you are studying (optional; will be asked if not provided).",
		default=None,
	)
	# This shows at the bottom of --help
	parser.epilog = "Typical run command: python -m src.app"

	return parser.parse_args()



def main():

	"""Main function: Contains the CLI"""

    #initialize the parser
	args = parse_args()
	profiles = load_profiles()
	session_data = None

	console.clear()
	console.print(Panel.fit(
		"[bold green]== WELCOME TO THE POMODORO STUDY BUDDY ==== [/bold green]\n"
		"italic=Study smarter with AI-powered study mode suggestions and material generation!", 
		border_style = "green" 

	))

	# ---- Load or create profile ---- 

	session_data = load_or_create_profile(profiles)

	# Inital data Setup 

	if session_data:
# load data from a slescted profile
		console.print("[bold green] Session data loaded from profile. [/bold green]")
	 name = session_data.get('name')
	 method = session_data.get('method')
	 subject = session_data.get('subject')
	 state = session_data.get('state')
	 minutes = session_data.get('minutes', 30
	 source_type = session_data.get('source', 'CLI/Loaded')	 

	console.print(f[dim]Loaded : Name: {name}, Method: {method}, Subject: {subject}, State: {state}, Minutes: {minutes}, Source: {source_type}[/dim]")

	else: 
		name = args.name or Prompt.ask("What is your [bold]name[/bold]? ")

		method = args.method
		if method and method.capitalize() in VALID_METHODS:
			method = method.capitalize()
		else:
			method = Prompt.ask(
				"Choose your study method",
				choices=VALID_METHODS, case_sensitive=False
			)

		subject = args.subject or Prompt.ask("What [bold]subject[/bold] are you studying? ")
		state = None
		source_type = "AI"

		




		# Gather data from user input or command-line args
	state = input("What is your current state of energy today?: (tired, focused, overwhelmed)")
	mode = study_mode(state)

	print(f"Suggested mode: {mode}")

	name = session_data.get('name') or args.name
	if not name:
		name = input("What is your name? ")
	print(f" Name set: {name}")


	VALID_METHODS = ['quiz', 'flashcards', 'summary']
	method = session_data.get('method') or args.method


	if method and method.strip().lower() in VALID_METHODS:
		method = method.strip()
		print(f" Method set: {method}")
	else:
		method = ""
		while method.strip().lower() not in VALID_METHODS:
			method = input("What method do you want to use to learn? (Quiz, Flashcards or Summary) ")
			
			if method.strip().lower() in VALID_METHODS:
				break
			else:
				print("Invalid selecetion. Please enter only Quiz, Flashcards, or Summary.")

	subject = session_data.get('subject') or args.subject
	source_type = session_data.get('source')

	if subject:
		print(f" Subject set: {subject}")
		if not source_type:
			source_type = "CLI/Loaded"
	else:
		subject, source_type = get_material_source()
		subject = input("What subject are you studying? ")


	print("\nGenerating study materials .....")
	prompt = build_prompt(name, method, subject)
	response = get_study_materials(prompt)
	print("\n" + response)

	##------ Saving a Profile -------

	current_profile_key = f"{name}_{method}_{subject}".replace(' ', '_')

	if current_profile_key in profiles:
		print("\nNote: This session matches an existing profile. Saving is skipped.")
		return

	save_choice = input("\nDo you want to save this session as a profile? (y/n): ").strip().lower()

	if save_choice == 'y': 
		if len(profiles) >= MAX_PROFILES:
			print("\nCannot save profile. MAX NUMBER REACHED.")
			return

		new_profile = {
			"name": name, 
			"state": state, 
			"method": method, 
			"subject": subject, 
			"source": source_type
		}

		profiles[current_profile_key] = new_profile
		save_profiles(profiles)
		print(f" Session saved successful as a profile '{current_profile_key}'.")
	else:
		print("Session not saved.")


if __name__ == "__main__":
	main()
def chat_ui_placeholder():
    """Future chat interface for Study Buddy."""
    print("Chat UI component coming soon...")
