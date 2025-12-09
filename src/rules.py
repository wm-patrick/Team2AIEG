import logging

logging.basicConfig(level=logging.INFO)

def study_mode(current_state: str, minutes: int) -> str:
    """Suggest a study mode based on the user's current energy level and mintues available."""

    if not isinstance(current_state, str):
        return "basic check-in"
    if not isinstance(minutes, int) or minutes <=0:
        return "basic check-in"

    current_state = current_state.strip().lower()

    logging.info(f"Processing study mode for current state: '{current_state}' with '{minutes}' minutes to study.")

    if current_state == "tired" and minutes < 20:
        return "light review"
    elif current_state == "focused" and minutes >= 40:
        return "deep study"
    elif current_state == "overwhelmed":
        return "easy material"
    elif current_state == "exhausted":
        return "nap time"
    else:
        return "basic check-in"
