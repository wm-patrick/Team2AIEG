import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)


def study_mode(current_state: Optional[object]) -> str:
    """Return a short study-mode suggestion string based on the user's current state.

    """

    if not isinstance(current_state, str):
        logging.warning(f"Invalid state input: {type(current_state)}. Defaulting to 'basic check-in'.")
        return "basic check-in"

    current_state = current_state.strip().lower()

    if current_state == "focused":
        return "deep study"
    if current_state == "tired":
        return "light review"
    return "basic check-in"
