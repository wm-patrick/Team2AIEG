import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
	raise RuntimeError(
		"key not found. Create .env file and add key"
	)

#2. create the OPENAI client
client = OpenAI(api_key = api_key)


def build_prompt(name, method, subject):

	prompt = (f""" Your role is to act as a friendly tutor or instructor.
	
	The student's name is below. The student's method of learning is also below.
	
	Name: {name}
	Method: {method}
	Subject: {subject}
	
	Confirm to the user in a friendly and encouraging way their name and method of study. 
			
	if you are unsure about the subject material do not guess and state that you are unsure.""")
	
	return prompt

def get_study_materials(prompt: str) -> str:
	model = "gpt-4-mini"
	response = client.chat.completions.create(
		model=model,
		messages=[{"role": "user", "content": prompt}]
	)
	return response.choices[0].message.content

def main():
	name = input("What is your name? ")
	method = input("What method do you want to use to learn? (Quiz, Flashcards or Summary) ")
	subject = input("What subject are you studying? ")
	prompt = build_prompt(name, method, subject)
	response = get_study_materials(prompt)
	print(response)

if __name__ == "__main__":
	main()
