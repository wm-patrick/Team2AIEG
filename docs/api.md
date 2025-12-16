# Developer API & Function Reference

This document serves as the technical reference for the **Pomodoro Study Buddy**. It outlines the external API integrations, environment configuration, and the internal function signatures across the application's modules.

## 1. External Configuration

The application requires a connection to Google's Gemini LLM for generating study content.

### Environment Setup
Ensure a `.env` file exists in the root directory with the following key:
```bash
GEMINI_API_KEY=your_google_api_key_here

##`src/app.py`

`def build_prompt(name: str, method: str, subject: str) -> str:`
- takes the following parameters: name, method, subject 
- builds a string with the parameters included 
- returns a str response to get_study_materials function

`def get_study_materials(prompt: str)->str:`
- takes prompt generated in the build_prompt function as a parameter
- call Gemini to generate study materials
- returns Gemini response
- response is printed to the terminal using rich formatting