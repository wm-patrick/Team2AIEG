# Developer API & Function Reference

This document serves as the technical reference for the **Pomodoro Study Buddy**. It outlines the external API integrations, environment configuration, and the internal function signatures across the application's modules.

## 1. External Configuration

The application requires a connection to Google's Gemini LLM for generating study content.

### Environment Setup
Ensure a `.env` file exists in the root directory with the following key:
```bash
GEMINI_API_KEY=your_google_api_key_here