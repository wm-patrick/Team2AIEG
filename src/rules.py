import logging

logging.basicConfig(level=logging.INFO)

def study_mode(current_state: str, minutes: int = 45) -> str:
    """Suggest a study mode based on the user's current energy level and minutes available.

    `minutes` is optional and defaults to 45 so callers that only provide
    a `current_state` (the common case in tests) still get sensible output.
    """

    if not isinstance(current_state, str):
        return "basic check-in"
    if not isinstance(minutes, int) or minutes <= 0:
        return "basic check-in"

    current_state = current_state.strip().lower()

    logging.info(
        "Processing study mode for current state: '%s' with '%d' minutes to study.",
        current_state,
        minutes,
    )

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
