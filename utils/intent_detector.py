INTENTS = {
    "fees": [
        "fee", "fees", "cost", "price",
        "शुल्क", "फीस",
        "ఫీజు", "ఫీజులు", "ధర"
    ],

    "eligibility": [
        "eligibility", "qualification",
        "योग्यता",
        "అర్హత"
    ],

    "duration": [
        "duration", "years", "how long",
        "अवधि",
        "వ్యవధి"
    ],

    "courses": [
        "course", "courses", "program", "programs",
        "curriculum",
        "पाठ्यक्रम", "कोर्स",
        "కోర్స్", "కోర్సులు"
    ],

    "facilities": [
        "facility", "facilities", "amenities", "services", "campus",
        "सुविधा", "सुविधाएं",
        "సదుపాయం", "సదుపాయాలు"
    ]
}


def detect_intent(text):
    text = text.lower()

    scores = {}

    for intent, keywords in INTENTS.items():
        score = 0
        for word in keywords:
            if word in text:
                score += 1
        if score > 0:
            scores[intent] = score

    if not scores:
        return None

    if "facilities" in scores:
        scores["facilities"] += 1

    return max(scores, key=scores.get)