#------------------------IMPORTS GO HERE------------------------------------
import argparse
import os
from dotenv import load_dotenv
from google import genai
from src.rules import study_mode
from src.timer import pomodoro_arg_func

#load the environment variables
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


def build_prompt(name, method, subject):
	"""This function builds the prompt that is sent to LLM"""

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
	
	print("==== 🍅 WELCOME TO THE POMODORO STUDY BUDDY 🍅 ====")
	
	#get the user's state of energy and time available to study
	state = input("What is your current state of energy today? (tired, focused, overwhelmed):")
	while state not in ["tired", "focused", "overwhelmed"]:
		state = input("Invalid input. Please enter tired, focused, or overwhelmed: ")	

	minutes = input("How many minutes do you have to study?(Enter a whole number):")
	while not minutes.isdigit():
		minutes = input("Invalid input. Please enter a whole number: ")
	minutes = int(minutes)

	#call the study_mode function to suggest a study mode based on the user's state of energy and time available
	mode = study_mode(state, minutes)

	#show the suggested study mode
	print(f"Suggested mode: {mode}")


	name = input("What is your name? ")
	method = input("What method do you want to use to learn? (Quiz, Flashcards or Summary) ")
	while method not in ["Quiz", "Flashcards", "Summary"]:
		method = input("Invalid input. Please enter Quiz, Flashcards, or Summary: ")
	subject = input("What subject are you studying? ")
	prompt = build_prompt(name, method, subject)
	response = get_study_materials(prompt)
	print(response)

    #give the option to start a timer
	#timer_yes_no = input("Would you like to start a pomodoro timer? (yes/no): ")
	pomodoro_arg_func()

if __name__ == "__main__":
	main()
	
def chat_ui_placeholder():
    """Future chat interface for Study Buddy."""
    print("Chat UI component coming soon...")
