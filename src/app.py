# ------------------------ IMPORTS GO HERE ------------------------------------
import argparse
import os
from dotenv import load_dotenv
from google import genai
from src.rules import study_mode        # or: from rules import study_mode
from src.timer import pomodoro_arg_func # or: from timer import pomodoro_arg_func

# load the environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "key not found. Create .env file and add GEMINI_API_KEY to .env"
    )
else:
    print("API key loaded successfully.")

# 2. create the Google GenAI client
client = genai.Client(api_key=api_key)


def build_prompt(name: str, method: str, subject: str) -> str:
    """Builds the prompt that is sent to the LLM."""
    prompt = f"""
Your role is to act as a friendly tutor or instructor.

The student's name and method of learning are below.

Name: {name}
Method: {method}
Subject: {subject}

1. Confirm to the user in a friendly and encouraging way their name and method of study.
2. Then, generate that method of study for the user for the given subject.
3. If you are unsure about the subject material, do NOT guess; clearly say that you are unsure.
4. If the method is "Quiz", generate 5 multiple-choice questions (with 4 options each) about the subject.
5. If the method is "Flashcards", generate 5 flashcards (with question on
6. If the method is "Quiz", generate answers after the questions.

"""
    return prompt.strip()

def get_study_materials(prompt: str) -> str:
    """Call Gemini to generate study materials."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text
    
    except Exception as e:

        print("An error occurred while generating study materials.")
        print (f"Technical details are as follows: {str(e)}")

        return "I apologize, but the AI service is currently unavailable. Please try again later."

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Pomodoro Study Buddy: suggests a study mode and can ask an LLM "
            "to generate study materials."
        )
    )

    parser.add_argument(
        "--name",
        help="Your name (optional; will be asked if not provided).",
        default=None,
    )
    parser.add_argument(
        "--method",
        help="Study method: Quiz, Flashcards, or Summary.",
        default=None,
    )
    parser.add_argument(
        "--subject",
        help="Subject you are studying.",
        default=None,
    )

    # This shows at the bottom of --help
    parser.epilog = "Typical run: python -m src.app"

    return parser.parse_args()

def main():
    """Main function: Contains the CLI."""
    # initialize the parser
    args = parse_args()

    print("==== 🍅 WELCOME TO THE POMODORO STUDY BUDDY 🍅 ====")

    # ---- Get the user's state of energy ----
    state = input(
        "What is your current state of energy today? (tired, focused, overwhelmed): "
    ).strip().lower()
    while state not in ["tired", "focused", "overwhelmed"]:
        state = input(
            "Invalid input. Please enter tired, focused, or overwhelmed: "
        ).strip().lower()

    # ---- Get minutes available ----
    minutes = input("How many minutes do you have to study? (Enter a whole number): ").strip()
    while not minutes.isdigit():
        minutes = input("Invalid input. Please enter a whole number: ").strip()
    minutes = int(minutes)

    # call the study_mode function to suggest a study mode
    # (assumes study_mode(state, minutes) signature)
    mode = study_mode(state, minutes)

    # show the suggested study mode
    print(f"\nSuggested mode: {mode}\n")

    # ---- Name ----
    name = args.name or input("What is your name? ").strip()

    # ---- Method ----
    VALID_METHODS = ["Quiz", "Flashcards", "Summary"]
    method = args.method or ""
    method = method.strip().capitalize()

    while method not in VALID_METHODS:
        method = input(
            "What method do you want to use to learn? (Quiz, Flashcards, or Summary): "
        ).strip().capitalize()
        if method not in VALID_METHODS:
            print("Invalid input. Please enter Quiz, Flashcards, or Summary.")

    # ---- Subject ----
    subject = args.subject or ""
    if not subject:
        subject = input("What subject are you studying? ").strip()

    # ---- LLM call ----
    prompt = build_prompt(name, method, subject)
    print("\nGenerating study materials with Gemini...\n")
    response = get_study_materials(prompt)
    print(response)

    # ---- Optional Pomodoro timer ----
    start_timer = input("\nWould you like to start a Pomodoro timer now? (yes/no): ").strip().lower()
    if start_timer in ["yes", "y"]:
        pomodoro_arg_func()
        
    elif start_timer in ["no", "n"]:
        method = "Summary"
        new_prompt = build_prompt(name, method, subject)
        print(f"\nGenerating {method}...\n")
        response = get_study_materials(new_prompt)
        print(response)
    else:
        print("Okay, no timer started. Happy studying! 🍅")


if __name__ == "__main__":
    main()


def chat_ui_placeholder():
    """Future chat interface for Study Buddy."""
    print("Chat UI component coming soon...")