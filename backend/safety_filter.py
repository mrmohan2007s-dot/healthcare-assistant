import re

DISCLAIMER = (
    "I am not a medical professional. This tool provides general information only; "
    "seek a qualified provider for personal medical advice."
)

_REFUSE_PATTERNS = [
    r"\bdiagnos(e|is|ing)\b",
    r"\btreat(ment|ing|ments)?\b",
    r"\bprescrib(e|ing|ed)\b",
    r"\bdose(s)?\b",
    r"\bsurgery\b",
    r"\bimmediate help\b",
    r"\bemergency\b",
]

_URGENT_PATTERNS = [
    r"\bdifficulty breathing\b",
    r"\bchest pain\b",
    r"\bsevere bleeding\b",
    r"\bloss of consciousness\b",
    r"\bnot breathing\b",
]


def get_disclaimer():
    return DISCLAIMER


def check_query(query: str):
    """Return (allowed: bool, reason: str). If query appears to request diagnosis/treatment,
    refuse and explain. If query contains urgent language, mark as urgent (still non-diagnostic).
    """
    q = query.lower()
    for p in _REFUSE_PATTERNS:
        if re.search(p, q):
            return False, "Request appears to ask for diagnosis or treatment; refusing."

    for p in _URGENT_PATTERNS:
        if re.search(p, q):
            return True, "urgent"

    return True, "ok"


def is_urgent_flag(reason: str) -> bool:
    return reason == "urgent"
