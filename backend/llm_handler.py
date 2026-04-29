import os
import re
import json
from backend.config import CONFIG

try:
    import openai
except Exception:
    openai = None

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))


def _load_json(path_relative):
    path = os.path.join(DATA_DIR, path_relative)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


SCHEMA = {
    "required_keys": [
        "disclaimer",
        "condition",
        "summary",
        "symptoms",
        "precautions",
        "when_to_seek_care",
        "sources",
        "confidence",
    ]
}


def _validate_response(resp: dict) -> dict:
    # Ensure keys exist and types are safe
    out = {}
    for k in SCHEMA["required_keys"]:
        val = resp.get(k)
        if val is None:
            # provide safe defaults when missing
            if k in ("symptoms", "precautions", "when_to_seek_care", "sources"):
                out[k] = []
            else:
                out[k] = ""
        else:
            out[k] = val
    # pass through any extra helpful fields
    out["follow_up_questions"] = resp.get("follow_up_questions", [])
    return out


def _call_openai(prompt: str) -> str:
    if not CONFIG.get("OPENAI_API_KEY") or openai is None:
        raise RuntimeError("OpenAI not configured or client library missing")
    openai.api_key = CONFIG.get("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a non-diagnostic health assistant. Always include the disclaimer and return strictly JSON following the schema given."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=800,
    )
    return completion.choices[0].message.content


def generate_response(query: str) -> dict:
    """Generate a response for the frontend. If an OpenAI API key is present this will
    call OpenAI with a JSON-output instruction; otherwise it falls back to the local
    symptom mapping in `data/symptoms.json`.
    """
    faq = _load_json("faq.json") or []
    symptoms_db = _load_json("symptoms.json") or {}
    SYMPTOMS_LIMIT = 12
    PRECAUTIONS_LIMIT = 12
    WHEN_LIMIT = 10
    SOURCES_LIMIT = 3

    # If API key available try to call OpenAI for richer output
    if CONFIG.get("OPENAI_API_KEY") and openai is not None:
        system_schema = {
            "disclaimer": "I am not a medical professional. This tool provides general information only; seek a qualified provider for personal medical advice.",
            "schema": SCHEMA,
        }
        prompt = (
            f"Respond to the user query below in JSON following the schema. Use concise, grade-8 reading level."
            f"\n\nSchema: {json.dumps(system_schema)}\n\nUser query: {query}\n\nProvide up to {SYMPTOMS_LIMIT} symptoms and {PRECAUTIONS_LIMIT} precautions, and 2-{SOURCES_LIMIT} reputable sources."
        )
        try:
            raw = _call_openai(prompt)
            # Attempt to extract JSON from response
            start = raw.find("{")
            if start != -1:
                raw_json = raw[start:]
                resp = json.loads(raw_json)
                validated = _validate_response(resp)
                # ensure disclaimer present
                validated.setdefault("disclaimer", system_schema["disclaimer"])
                return validated
        except Exception:
            # fall through to local mapping fallback
            pass

    # Local fallback: improved keyword match into symptoms_db
    lowered = query.lower()
    found = None
    best_match_count = 0
    
    def keyword_matches(text: str, keyword: str) -> bool:
        keyword = keyword.lower().strip()
        if not keyword:
            return False
        # Use word boundaries to avoid partial matches like "pe" in "peel".
        if re.search(rf"\b{re.escape(keyword)}\b", text):
            return True
        return len(keyword) > 3 and keyword in text

    for cond, info in symptoms_db.items():
        match_count = 0
        if keyword_matches(lowered, cond.lower()):
            match_count += 2
        for kw in info.get("keywords", []):
            if keyword_matches(lowered, kw):
                match_count += 1
        
        # Update best match if this condition has more keyword matches
        if match_count > best_match_count:
            best_match_count = match_count
            found = (cond, info)

    if found:
        cond, info = found
        primary_symptoms = info.get("symptoms", []) or []
        # Use keywords as additional symptom hints so the UI can show more items.
        # This is still non-diagnostic and keyword-based, not a medical assessment.
        keyword_symptoms = info.get("keywords", []) or []
        combined_symptoms = []
        seen = set()
        for s in primary_symptoms + keyword_symptoms:
            s = str(s).strip()
            if not s:
                continue
            k = s.lower()
            if k in seen:
                continue
            combined_symptoms.append(s)
            seen.add(k)

        resp = {
            "disclaimer": "I am not a medical professional. This tool provides general information only; seek a qualified provider for personal medical advice.",
            "condition": cond,
            "summary": info.get("summary", ""),
            "symptoms": combined_symptoms[:SYMPTOMS_LIMIT],
            "precautions": (info.get("precautions", []) or [])[:PRECAUTIONS_LIMIT],
            "when_to_seek_care": (info.get("when_to_seek_care", []) or [])[:WHEN_LIMIT],
            "sources": (info.get("sources", []) or faq[:2])[:SOURCES_LIMIT],
            "confidence": info.get("confidence", "medium"),
            "follow_up_questions": [
                "When did symptoms start, and are they getting better or worse?",
                "Do you have a fever, and if yes, how high?",
                "Where exactly is the discomfort (and does it spread)?",
                "What have you tried so far, and did it help?",
                "Any known allergies or long-term conditions?"
            ],
        }
        return _validate_response(resp)

    # Generic fallback
    resp = {
        "disclaimer": "I am not a medical professional. This tool provides general information only; seek a qualified provider for personal medical advice.",
        "condition": "General symptom information",
        "summary": "This provides general awareness information based on the symptoms described.",
        "symptoms": [],
        "precautions": [
            "Practice basic hygiene (hand washing)",
            "Rest and monitor symptoms",
            "Stay hydrated",
            "Avoid known triggers (if any)",
            "Track symptom timing and severity",
            "Consider contacting a clinician if symptoms persist or worsen"
        ][:PRECAUTIONS_LIMIT],
        "when_to_seek_care": [
            "Difficulty breathing",
            "Chest pain",
            "High fever",
            "Severe or rapidly worsening symptoms",
            "New confusion or fainting"
        ][:WHEN_LIMIT],
        "sources": faq[:SOURCES_LIMIT],
        "confidence": "low",
        "follow_up_questions": [
            "Can you describe your main symptom in your own words?",
            "How long have symptoms been present?",
            "Is the symptom getting better, worse, or staying the same?",
            "Do you have any fever, vomiting, or breathing trouble?"
        ]
    }
    return _validate_response(resp)
