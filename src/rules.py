import logging
from typing import Tuple 

logging.basicConfig(level=logging.INFO)

StudyModeTuple = Tuple[str, int, int] 

def study_mode(current_state: str, minutes: int) -> StudyModeTuple:
    """Determines a suggested study mode based on the user's current energy level and minutes available.

    Returns: 
        A tuple: (description_string, work_min, break_min)
    """

    #-------- 1. Input Validation --------#
    
    if not isinstance(current_state, str):
        logging.warning(f"Invalid state input: {type(current_state)}. Defaulting to 'basic check-in'.")
        return ("Basic check-in (15 min work/ 5 min break, 1 cycle)", 15, 5)
    
    if not isinstance(minutes, int) or minutes <= 0:
        logging.warning(f"Invalid minutes input: {minutes}. Defaulting to 30 minutes.")
        return ("Basic check-in (15 min work/ 5 min break, 1 cycle)", 15, 5)

    current_state = current_state.strip().lower()

    logging.info(f"Processing study mode for current state: '{current_state}' with {minutes} minutes available to study.")


    #----- 2. Study Mode Determination -----#

    if current_state == "exhausted":
        logging.info("Suggestion: Nap time recommended.")
        return ("Nap time (Stop studying, 0 cycles)", 0, 0)
    
    elif current_state == "tired" and minutes < 20:
        logging.info("Suggestion: Light review recommended.")
        return ("Light review (10 min work / 2 min break, 1 cycle)", 10, 2)

    elif current_state == "focused" and minutes >= 40:
        if minutes >= 90:
            return ("Deep study (45 min work/ 15 min break, 2 cycles)", 45, 15)
        else: 
            return ("Basic study (30 min work / 10 min break, 1 cycle)", 30, 10)
    
    elif current_state == "overwhelmed":
        logging.info("Suggestion: Easy material/Flashcards recommended.")
        return ("Easy material (15 min work / 5 min break, 2 cycles)", 15, 5)

    else:
        logging.info("Suggestion: Basic check-in recommended.")
        return ("Standard check-in (25 min work/ 5 min break, 1 cycle)", 25, 5)
