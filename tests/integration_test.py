import sys
import os
from unittest.mock import patch, MagicMock
import pytest

# Add the root directory to sys.path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import app

@patch('src.app.client')
@patch('src.app.Prompt.ask')
@patch('src.app.IntPrompt.ask')
@patch('src.app.Confirm.ask')
def test_full_session_flow(mock_confirm, mock_int_prompt, mock_prompt, mock_client):
    """
    Integration Test: Simulates a user starting the app, running a session, 
    getting AI results.
    """
    
    # 1. Setup the mock User Inputs
    mock_prompt.side_effect = [
        "1",              # Select "Start New Session"
        "Test User",      # Name
        "Quiz",           # Method
        "Python Lists",   # Subject
        "focused"         # State
    ]
    
    mock_int_prompt.return_value = 25  # Minutes
    
    # Say NO to everything (Saving Profile and Starting Timer)
    mock_confirm.return_value = False

    # 2. Setup the mock AI Response
    mock_response = MagicMock()
    mock_response.text = "# Mocked Quiz\n1. What is a list?"
    mock_client.models.generate_content.return_value = mock_response

    # 3. Run the App
    with patch.object(sys, 'argv', ['app.py']): 
        try:
            app.main()
        except SystemExit:
            pass 

    # 4. Assertions
    # Did we ask the AI for the right thing? YES.
    mock_client.models.generate_content.assert_called_once()
    
    # Did we ask the user for inputs? YES.
    assert mock_prompt.call_count == 5 

def test_missing_api_key():
    """Test that the app exits gracefully without an API key."""
    with patch.dict(os.environ, {"GEMINI_API_KEY": ""}):
        import importlib
        import src.app
        
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            importlib.reload(src.app)
            
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 1