# Integration Test Checklist

## Core Functionality
- [x] **Application Launch**: `python -m src.app` starts without errors.
- [x] **Environment Variables**: App correctly identifies missing `.env` file (Graceful exit).
- [x] **Profile Loading**:
    - [x] Loads existing `profiles.json` if present.
    - [x] Creates new profile dictionary if file is missing.

## User Flows
- [x] **New Session Flow**:
    - [x] User can enter Name, Method, Subject.
    - [x] AI generates content successfully.
    - [x] Session is logged to `history.py`.
- [x] **Load Profile Flow**:
    - [x] Selecting a profile pre-fills user data.
    - [x] Invalid selection handles gracefully (updated error message).
- [x] **Delete Profile Flow**:
    - [x] User can delete a specific profile.
    - [x] `profiles.json` updates immediately.

## AI Integration
- [x] **Prompt Construction**: `build_prompt` correctly formats user input.
- [x] **API Connection**: `get_study_materials` returns text from Google Gemini.
- [x] **Error Handling**: Network disconnects or bad keys return a "Service Unavailable" message instead of crashing.

## CLI Polish
- [x] **Help Text**: `python -m src.app --help` shows clear usage examples.
- [x] **Rich UI**: Tables and Panels render correctly on standard terminal.
