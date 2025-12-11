def study_mode(current_state: str, minutes: int) -> tuples[str, int, int, int]:
    """Determines a suggested study mode based on the user's current energy level and mintues available."""

    """ Returns: (descrption_string, work_min, break_min, cycles)"""

    #-------- 1. Input Validation --------#

    #--- Defaults to "basic check-in" if inputs are invalid ---#
    
    if not isinstance(current_state, str) or not isinstance(minutes, int) or minutes <= 0:
        return "Basic check-in (15 min work/ 5 min break, 1 cycle)" 15, 5, 1)

    current_state = current_state.strip().lower()

    #----- 2. Study Mode Determination -----#
    
    current_state = current_state.strip().lower()

    if current_state == "tired" and minutes < 20:
        return ("Light review (10 min work / 2 min break, 1 cycle)" 10, 2, 1)

    elif current_state == "focused" and minutes >= 40:
        if minutes >= 90:
            return "Deep study (45 min work/ 15 min break, 2 cycles)", 45, 15, 2)
        else: 
            return ("Basic study (30 min work / 10 min break, 1 cycles)" 30, 10, 1)         
    
    elif current_state == "overwhelmed":
        return "Easy material/Flashcards (15 ,in work / 5 min break, 2 cycle)", 15, 5, 2)
    else:
        return "Basic check-in/Summary (25 min work / 5 min break, 2 cycle)", 25, 5, 2)
