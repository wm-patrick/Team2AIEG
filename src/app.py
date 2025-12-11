# ============================IMPORTS==========================
import argparse
import sys
import os
from dotenv import load_dotenv
from google import genai

#-------------------------LOCAL IMPORTS --------------------------------
from src.rules import study_mode     
from src.timer import pomodoro_arg_func
from src.history import log_session, get_last_sessions 

#-------------------------RICH IMPORTS --------------------------------------
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.markdown import Markdown

#============================END OF IMPORTS==========================

#============================FUNCTIONS===============================
# load the environment variables
load_dotenv()

#initialize rich console
console = Console()

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
        ))

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

def start_new_session(args):
    """Start a study session with the user's input."""
    state = Prompt.ask(
        "What is your [cyan]current state[/cyan] of energy?", 
        choices = ["Tired", "Focused", "Overwhelmed"],
        case_sensitive=False)

    # ---- Get minutes available, prompt user to enter positive number if <=0 entered ----
    while True:
        minutes = IntPrompt.ask("How many [cyan]minutes[/cyan] do you have available for studying? ")
        if minutes > 0:
            break
        else:
            console.print("[bold red]Please enter a positive number of minutes.[/bold red]")

    # call the study_mode function to suggest a study mode
    mode = study_mode(state, minutes)

    # show the suggested study mode
    console.print(f"\n[bold yellow]Suggested mode:[/bold yellow] {mode}\n")

    # ---- Name ----
    name = args.name or Prompt.ask("What is your [bold]name[/bold]?")

    # ---- Method ----
    VALID_METHODS = ["Quiz", "Flashcards", "Summary"]
    method = args.method or ""

    if method.capitalize() not in VALID_METHODS:
        method = Prompt.ask(
            "Choose a learning method", 
            choices=VALID_METHODS, case_sensitive=False
        )

    # ---- Subject ----
    subject = args.subject or Prompt.ask("What [bold cyan]subject[/bold cyan] are you studying?")

    # ---- LLM call ----
    prompt = build_prompt(name, method, subject)

    # creates the "dot dot dot" animation while waiting
    with console.status("[bold green]Gemini is generating materials...[/bold green]", spinner="dots"):
        response = get_study_materials(prompt)

    # This prints the AI's answer inside a blue box, formatted as Markdown
    console.print(Panel(
        Markdown(response), 
        title=f"Generated {method}", 
        border_style="blue"
    ))

    log_session(name, subject, method, response)
    console.print("[dim italic]Session saved to history log.[/dim italic]")
    # ---- Option to start Pomodoro timer ----
    # Confirm.ask returns True for yes, False for no
    if Confirm.ask("\nStart Pomodoro timer now?"):
        pomodoro_arg_func()
        
    else:
        # If user says no, generate a summary
        console.print("[dim]Skipping timer... generating summary instead.[/dim]")
        
        method = "Summary"
        new_prompt = build_prompt(name, method, subject)
        
        with console.status("[bold green]Generating summary...[/bold green]"):
            response = get_study_materials(new_prompt)
            
        console.print(Markdown(response))
        console.print("[bold green]Happy studying! 🍅[/bold green]")




def main():
    """Main function: Contains the CLI."""
    # initialize the parser
    args = parse_args()

    console.clear()

    console.print(Panel.fit(
        "[bold green]==== 🍅 WELCOME TO THE POMODORO STUDY BUDDY 🍅 ====[/bold green]\n"
        "[italic]Your AI-powered Study Assistant[/italic]",
        border_style="green"
    ))
    #---above remains
    #---new menu system designed to be used with new history.py file below
    console.print(f"\n[bold]Please make a selection from the menu options below:[/bold]")
    console.print("\n[cyan]1. Start a New Session[/cyan]")
    console.print("\n[cyan]2. Review Past Sessions[/cyan]")

    choice = Prompt.ask("Please select an option:", choices=["1", "2"], case_sensitive=False)

    if choice == "1":
        start_new_session(args)
    elif choice == "2":
        get_last_sessions(limit=3)
#--------------------------old main code to be transferred to start_new_session function
    # ---- Get user's state of energy ----
   

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold yellow] Goodbye! See you next time.[/bold yellow]")
        sys.exit(0)
