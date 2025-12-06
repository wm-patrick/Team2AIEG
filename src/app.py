import os
from dotenv import load_dotenv
from google import genai
from .rules import study_mode

#This comment is to test how to push 
#This comment is to demonstrate second push
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

def main():
	print("==== WELCOME TO THE POMODORO STUDY BUDDY ====")
	state = input("What is your current state of energy today?: (tired, focused, overwhelmed)")
	mode = study_mode(state)

	print(f"Suggested mode: {mode}")

	name = input("What is your name? ")
	method = input("What method do you want to use to learn? (Quiz, Flashcards or Summary) ")
	subject = input("What subject are you studying? ")
	prompt = build_prompt(name, method, subject)
	response = get_study_materials(prompt)
	print(response)

if __name__ == "__main__":
	main()
