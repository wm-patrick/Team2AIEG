#------------------------IMPORTS GO HERE------------------------------------
import argparse
import os
import json
from dotenv import load_dotenv
from google import genai
from .rules import study_mode

#This comment is to test how to push 
#This comment is to demonstrate second push

#----Profile Mangement Constants ----
MAX_PROFILES = 3
PROFILES_FILE = "profiles.json"

#loading the environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
	raise RuntimeError(
		"key not found. Create .env file and add key"
	)
else:
	print("API key loaded successfully.")

#2. create the Google GenAI client
client = genai.Client(api_key=api_key)

#------ Profile funtions ----

def load_profiles():
	""" Loads existing study profiles from the JSON file """
	if not os.path.exists(PROFILES_FILE):
		return {}
	try:
	 	with open (PROFILES_FILE, 'r') as f:
			return json.load(f)
	except json.JSONDecodeError:
		print(f"Warning, Profile not found. Starting with new profile. ")
		return {}


def save_profiles(profiles):
	""" Saves the current dictionary of Profiles to JSON file"""
	with open(PROFILES_FILE, 'w') as f:
		json.dump(profiles, f, indent=4)


def delete_profile(profiles):
	"""Prompts the user to slect and delete a file that exists"""
	if not profiles:
		print("No profiles to delete.")
		return profiles

	print("\n ====Select a Profile to delete ====")	
	profile_keys = list(profiles.keys())
	for i, name in enumerate(profile_keys, 1):
		profile_data = profiles[name]
		print(f" {i}. Name: {profile_data.get('name', 'N/A')}, Subject:{profile_data.get('subject', 'N/A')}, Method: {profile_data.get('method', 'N/A')}")

	while True:
		try:
			choice = input("Enter the number of the profile to delete (or 'c' to cancel): ")
			if choice.lower() == 'c':
				print("Deletion cancelled.")
				return profiles

			index = int(choice) - 1
			if 0 <= index < len(profile_keys):
				deleted_name = profile_keys[index]
				del profiles[deleted_name]
				save_profiles(profiles)
				print(f"Profile '{deleted_name}' delete succussful.")
				return profiles
			else:
				print("Invalid number. Please try again.")
		except ValueError:
			print("Invalid input. Please enter a number or 'c'. ")


def load_existing_profile(profiles):
	""" Prompts the user to select and load an existing profile """
	if not profiles:
		print("No saved profiles found. Starting new session.")			 
		return None
	print("\n===== Select a Profile to load ===")
	profile_keys = list(profiles.keys())
	for i, name in enumerate(profile_keys, 1):
		profile_data = profiles[name]
		print(f" {i}. Name: {profile_data.get('name', 'N/A')}, Subject: {profile_data.get('subject', 'N/A')}, Method:{profile_data.get('method', 'N/A')}")

	while True:
		try:
			choice = input("Enter the number of profiles to load ( or 'c' to cancel): ")
			if choice.lower() == 'c':
				print("loading cancelled. Starting new session.")
				return None

			index = int(choice) - 1
			if 0 <= index < len(profile_keys):
				profile_key = profile_keys[index]
				print(f"Profile '{profile_key}' loaded successfuly.")
				return profiles[profile_key]
			else:
				print("Invaild number. Please try again.")
		except ValueError:
			print("Invalid input. Please enter a number or 'c'.")



"""This function builds the prompt that is sent to LLM"""

def build_prompt(name, method, subject):

	prompt = (f""" Your role is to act as a friendly tutor or instructor.
	
	The student's name is below. The student's method of learning is also below.
	
	Name: {name}
	Method: {method}
	Subject: {subject}
	
	Confirm to the user in a friendly and encouraging way their name and method of study. Then, generate that method of study for the user.
			
	if you are unsure about the subject material do not guess and state that you are unsure.""")
	
	return prompt

def get_study_materials(prompt: str) -> str:
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text
def get_material_source():
	""" Asks user to choose between source or AI generated study guide."""

	while True:
		source_choice = input("\nSelect material source: (1) Upload PDF or (2) Generate materials with AI: ").strip()

		if source_choice == '1':
			pdf_path = input ("Enter the path to your PDF file: ")
		
		#---- PDF HANDLING TO BE IMPLEMENTED 
			return pdf_path, "PDF"

		elif source_choice == '2':
			subject = input(" What subject are you studying? ")
			return subject, "AI"

		else:
			print("Invalid choice. Please enter'1' or '2'. ")
			
def parse_args():
    parser = argparse.ArgumentParser(
        description="Pomodoro Study Buddy: suggests a study mode and can ask an LLM to generate study materials."
    )

    # This shows at the bottom of --help
    parser.epilog = "This terminal command will run the program: python -m src.app"

    return parser.parse_args()


def main():
	"""Main function: Contains the CLI"""

    #initialize the parser
	args = parse_args()
	profiles = load_profiles()
	
	print("==== WELCOME TO THE POMODORO STUDY BUDDY ====")
	
	#---- Profile Mangement -------------
	if len(profiles) >= MAX_PROFILES:
		print(f" MAXIMUM NUMBER OF PROFILES ({MAX_PROFILES}) reached. You must delete one before saving a new one. ")
		profiles = delete_profile(profiles)
	print(f" You currently have {len(profiles)} {MAX_PROFILES} profiles saved. ")

	#------ Loading a new session -------
	session_data = {}
	if profiles and not (args.name and args.method and args.subject):

		load_choice = input(" Would you like to '1' load a saved profile or (2) Start a new session? (1/2): ").strip()
		if load_choice =='1':
			session_data = load_existing_profile(profiles) or {}

	#--------- Gather User Input --------
	VALID_STATES = ['tired', 'focused', 'overwhelmed']
	state = "" #initialize the state variable

	while state.strip().lower() not in VALID_STATES:
		state = input("What is your current state of energy today?: (tired, focused, overwhelmed)")
		if state.strip().lower() in VALID_STATES:
			break
		else:
			print("Invalid selection. Please enter only 'tired', 'focused', or 'overwhelmed'. ")

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
		print(f" Session saved successful as a profile '{current_profile_key}'.\")
	else:
		print("Session not saved.")
else:
	print("Session not saved.")


if __name__ == "__main__":
	main()
def chat_ui_placeholder():
    """Future chat interface for Study Buddy."""
    print("Chat UI component coming soon...")
