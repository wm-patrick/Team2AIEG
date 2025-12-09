Sprint 1 Plan: Pomodoro Study Buddy

##Sprint Goal
Create a functional CLI that accepts user data in the form of a one-page PDF, user name, energy level, minutes to study and mode of study and returns encouragement and materials formatted according to preferred mode of study(i.e. a quiz, flashcards or summary).

##User Stories
Story 1:
As a student, I want to start the application, load my PDF, enter my name, energy level, number of minutes I have to study and preferred mode of study and receive output that is encouraging and useful in my study session.

**Acceptance Criteria**
- App asks for path to PDF
- App asks for Name, energy level and mintues available for study
- App accepts input without crashing 
- App returns encouragement and preferred mode of study
- App starts Pomodoro timer on at the end of response

##Test Plan
-Manual Testing: Run the program and verify prompts appear, PDF can be loaded, each item takes input and there is a response. Program fails gracefully with friendly error messages on invalid inputs. Pomodoro timer starts.
- Unit Testing: Verify that the input validator rejects invalid energy levels

## Definition of Done (DOD)
[] Code is written and commented.
[] Unit tests are written and passing.
[] Code is pushed to main on GitHub
[] "Responsible AI" usage disclaimer is visible in README.md

##Planned Issues (Backlog)
Issue                                              |  Owner      |    Due Date    |
-----------------------------------------------------------------------------------
Show user-friendly errors                            William            12/10
Implement optional functionality on Pomodoro timer   Sharonda           12/10
error handling for PDF upload			     William            12/10
research data cleaning for PDF                       Sharonda           12/10
research format for PDF presentation to LLM 	     Keyron		12/10
validate file type: PDF only			     William	        12/10
implement PDF file upload                            Sharonda           12/10
