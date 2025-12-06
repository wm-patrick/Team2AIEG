from src.rules import study_mode

def test_study_mode_known_value():
    assert study_mode("focused") == "deep study"

def test_study_mode_safe_default():
    assert study_mode("incredibly enthused!") == "basic check-in"