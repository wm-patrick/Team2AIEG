def study_mode(current_state: str) -> str:
    """Suggest a study mode based on the user's current energy level."""

    if not isinstance(current_state, str):
        return "basic check-in"
    
    current_state = current_state.strip().lower()

    if current_state == "tired":
        return "light review"
    elif current_state == "focused":
        return "deep study"
    elif current_state == "overwhelmed":
        return "easy material"
    else:
        return "basic check-in"
