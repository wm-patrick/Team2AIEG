# Team2AIEG
PROJECT NAME: Pomodoro Study Buddy

## PURPOSE
A CLI Study Buddy that: 
-Helps the user study by taking user name, level of energy, number of mintues to study and subject and sending it to LLM for 
the creation of a quiz, flashcards or summary.
-Sets a Pomodoro timer for the user during the study session.
-Logs what was studied
-Sends short encouragement messages 

# SETUP AND QUICKSTART
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

# TEAM
Sharonda (GitHub: @smhc94)
Franklin (GitHub: @3327-epoch)
Keyron (GitHub: @Ron2035)
William (GitHub: @wm-patrick)

# PROMPT LIBRARY
Promt Library Location: https://docs.google.com/document/d/1xK62k5tmNCo5H2Jc5aDURiCmJ4MJAeeXtwGZRMoIGu8/edit?usp=sharing

# LINK TO EXAMPLE RUN ON YOUTUBE
https://youtu.be/tZSs0tkV_To

# LINK TO ADOBE ACROBAT INFORMATIONAL SLIDES
https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:c0784ed9-b6ed-4b2f-a452-e21b1e65dacf

# LINK TO GOOGLE AI STUDIO VERSION OF THE POMODORO STUDY BUDDY
https://ai.studio/apps/drive/1T6CsskD_xG3aQQdVMGEVkJn1wogNAEIH

##  Responsible AI & Privacy

### A) Responsible AI System Card

* **Purpose & Users:**
    * **Purpose:** To overcome "study paralysis" by instantly generating focused study materials (quizzes, summaries) and enforcing timed work sessions (Pomodoro technique).
    * **Users:** Students, self-learners, and professionals seeking structured study aids for technical or factual topics.

* **Data Sources & Collection Method:**
    * **User Inputs:** The system collects user-provided names, study topics, and energy levels directly via the CLI interface.
    * **AI Knowledge Base:** The system retrieves educational content from the Google Gemini API (Large Language Model), subject to Google's Terms of Service. No external datasets are scraped or stored by this application.

* **PII Handling:**
    * **Minimization:** Only the User Name and Study Topic are processed. No emails, passwords, or contact info are requested.
    * **Storage:** All user data is stored locally on the client machine in `profiles.json`. Nothing is stored on external servers by the application developers.
    * **Retention:** Data persists locally until the user explicitly deletes their profile via the main menu.

* **Model/Logic Summary:**
    * **Logic:** The application uses rule-based logic for the Timer and Profile management.
    * **Model:** It utilizes `google-genai` (Gemini Pro) for content generation. The model is prompted with structured engineering prompts to ensure output is formatted as quizzes or flashcards.

* **Known Limitations & Bias Risks:**
    * **Hallucinations:** The AI may confidently present incorrect facts.
    * **Bias:** The model may reflect training data biases, though this is mitigated by the technical/factual nature of the intended use cases (e.g., "Python Lists" vs. social commentary).

* **Evaluation & Testing:**
    * **Testing:** Integration tests verified the conversation flow and API connectivity.
    * **Checks:** Manual testing was performed on diverse topics (History, Math, Coding) to ensure formatting stability.

* **Risk Mitigations & Fallbacks:**
    * **Disclaimers:** Users are warned at startup that AI content may be inaccurate.
    * **Fallbacks:** If the API fails or is unreachable, the application degrades gracefully, allowing the Timer to function without AI features.

* **Change/Monitoring Plan:**
    * **Feedback:** Users can submit issues via the GitHub repository.
    * **Monitoring:** Since the app runs locally, no centralized logging exists; developers rely on user bug reports to catch post-launch issues.

### B) Privacy & Data-Flow Checklist

| Requirement | Status | Notes |
| :--- | :--- | :--- |
| **Collect only necessary data** |  Yes | Only Name + Topic needed for personalization. |
| **Obtain clear consent** |  Yes | Implied consent by using the tool; usage is voluntary. |
| **Store securely** |  Yes | Stored locally (user controls their own device security). |
| **Restrict access** |  Yes | No remote access; only the local user can see profiles. |
| **Set retention and deletion policy** |  Yes | User can delete profiles at any time via menu option [4]. |
| **Avoid sharing raw PII** |  Note | User Name IS sent to Google Gemini for personalization. |
| **Document incidents** |  Yes | Issues tracked via GitHub Issues. |

### C) Risk & Mitigation Table

| Risk | Who’s impacted | Evidence/Trigger | Mitigation | Owner |
| :--- | :--- | :--- | :--- | :--- |
| **AI Hallucination** | Students / Learners | AI generates a false answer key for a quiz. | **Disclaimer:** "Verify all AI outputs" warning displayed before study sessions. | Dev Team |
| **Data Leakage** | Users with sensitive topics | User enters a password or secret as a "Study Topic". | **Documentation:** README warns against entering sensitive data into prompts. | User |
| **API Failure** | All Users | "Network Error" or "Invalid Key" crashes the app. | **Graceful Handling:** App catches errors and allows Timer-only mode. | Dev Team |
| **Study Fatigue** | Students | User studies too long without breaks. | **Logic:** App enforces mandatory breaks via Pomodoro rules. | Product Owner |


