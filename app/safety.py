def is_safe(question: str) -> bool:
    blocked_keywords = ["porn", "nude", "naked", "adult content","hack",
    "kill", "bomb", "drug", "weapon","suicide", 
    "abuse", "terrorist", "violence","xxx", "explicit", "onlyfans"]

    legal_keywords = ["law", "legal", "court", "judge", "justice",
    "act", "section", "ipc", "rti", "fir",
    "bail", "arrest", "lawyer", "advocate", "rights",
    "constitution", "penalty", "offence", "contract", "verdict",
    "case", "crime", "police", "punishment", "complaint",
    "sexual harassment", "rape", "murder", "assault",
    "domestic violence", "cybercrime", "fraud", "theft",
    "consumer", "tenant", "landlord", "divorce", "custody"]

    question = question.lower()
    if any(keyword in question for keyword in legal_keywords):
        return True
    if any(keyword in question for keyword in blocked_keywords):
        return False
    return False
