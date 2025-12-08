def study_mode(current_state: str) -> str:
    """Suggest a study mode based on the user's current energy level.
    
    Args:
        energy_state: The user's current energy state ('tired', 'focused', 'overwhelmed').
    
    Returns: A suffested study method.
        
        """

    if not isinstance(current_state, str):
        return "basic check-in"
    current_state = current_state.strip().lower()

    if current_state == "tired":
        return "light review/ Summary"
    elif current_state == "focused":
        return "deep study/ Quiz"
    elif current_state == "overwhelmed":
        return "easy material/ Flashcards"
    else:
        return "basic check-in / Summary"
