# Team2AIEG
PROJECT NAME: Pomodoro Study Buddy

## PURPOSE
A CLI Study Buddy that: 
-Helps the user study by taking user name, level of energy, number of mintues to study and subject and sending it to LLM for 
the creation of a quiz, flashcards or summary.
-Sets a Pomodoro timer for the user during the study session.
-Logs what was studied
-Sends short encouragement messages 

# SETUP
# QUICKSTART
-Python 3.10+
-Clone this repo.
# Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>

# Create a virtual environment (Recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

-Create a .env file in the project root with:
    GEMINI_API_KEY=your_actual_key_here

# USAGE
Run the app:
python -m src.app

# COMMAND LINE OPTIONS (FLAGS)
Flag,Description,Example
-h, --help,Show the help message and exit.,python -m src.app --help
--name,Your name (loads your profile if it exists).,"--name ""Patrick"""
--subject,The topic you want to study.,"--subject ""Calculus"""
--method,"The study format (Quiz, Flashcards, or Summary).","--method ""Quiz"""

# EXAMPLE USE OF FLAGS
python -m src.app --name "Patrick" --subject "System Design" --method "Quiz"

# RESPONSIBLE AI USE:
We use Gemini to generate study materials and encourage the user.
User should check with course materials or instructors regarding any discrepancies.
AI-Generated responses are reviewed by the team and used as guidance.

# TEAM
Sharonda (GitHub: @smhc94)
Franklin (GitHub: @3327-epoch)
Keyron (GitHub: @Ron2035)
William (GitHub: @wm-patrick)

# PROMPT LIBRARY
Promt Library Location: https://docs.google.com/document/d/1xK62k5tmNCo5H2Jc5aDURiCmJ4MJAeeXtwGZRMoIGu8/edit?usp=sharing

# LINK TO EXAMPLE RUN ON YOUTUBE
https://youtu.be/tZSs0tkV_To

## Ethical AI & Privacy

### Ethics Statement
The Pomodoro Study Buddy utilizes Generative AI (Google Gemini) to create educational content. We prioritize academic integrity and user transparency. Users are explicitly informed that all quizzes and summaries are AI-generated and should be verified against primary course materials. We do not claim AI outputs as fact without verification, and the application is designed to support—not replace—active learning.

### Risk Analysis Table

| Risk Category | Potential Harm | Mitigation Strategy |
| :--- | :--- | :--- |
| **Accuracy / Hallucination** | The AI might generate incorrect quiz answers or false facts, leading to study errors. | **User Warning:** A disclaimer is displayed before every AI session reminding users to verify facts. |
| **Data Privacy** | Sensitive user data could be sent to the external LLM provider. | **Data Minimization:** The app only sends the *subject topic* to the AI. No personal names or PII are transmitted. |
| **Over-Reliance** | Students might rely entirely on the AI for studying and skip actual source materials. | **Design Choice:** The app uses the "Pomodoro" timer to encourage deep work, treating the AI only as a starting point. |
| **Bias** | The AI model may reflect inherent biases in its training data regarding certain historical or social topics. | **Scope Limitation:** The app is intended for technical and factual academic subjects where social bias is less prevalent. |

### Privacy Checklist

- [x] **Local Storage:** User profiles and session history are stored 100% locally on the user's machine (`profiles.json`).
- [x] **No PII Transmission:** Personal Identifiable Information (like user names) is stripped before sending requests to the Google Gemini API.
- [x] **Transparency:** The application clearly states when it is connecting to the internet and using AI services.
- [x] **User Control:** Users can delete their local profiles and history at any time via the application menu.


Action Items as of 12/9/25:
- Add user-friendly error messages
- Gracefully exit the program or give user an option to restart the timer and choose a study mode again
- add code to take PDF, clean PDF, convert to JSON and send to LLM for response
- add code to create a 'memory' as was discussed in W10D1


