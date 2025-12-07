User Story

As a student, I want to be able to enter my current energy level so that the Study Buddy can recommend a mode of study that best suits my current energy level.

Inputs for Sprint 0
-	Text describing energy level
-	Name
-	Mode of preferred study (Quiz, FlashCards, Summary)
-	Subject of Study

Outputs
-	AI-Generated feeback confirming preferred method of study, subject and encouragement.
-	Either a summary, quiz or flashcards related to the given subject of study
-	AI-Generated suggestions for further study

Acceptance Criteria (Sprint 0)
-	Running ‘python -m src.app’ prints welcome message
-	User is asked for level of energy: input is passed to study_mode
-	All tests on study_mode function in ‘tests\test_rules.py’ pass via ‘pytest’
-	User is asked for name
-	User is asked for mode of study
-	User is asked for subject to be studied

Tiny Test Plan
-	Each of the three suggested energy levels produces the proper study mode response
-	Unexpected user input on current state of energy produces “Basic Check-In” response
-	‘pytest’ reports 2 tests passing based on user input: “focused” and unexpected input
