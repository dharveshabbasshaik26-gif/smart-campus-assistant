from rapidfuzz import process, fuzz
from utils.translator import translate_text
import random


# -------- FIND BEST MATCH --------
def find_best_match(user_input, options, threshold=70):
    """
    Finds the closest match for user input from a list of options
    using fuzzy matching.
    """

    result = process.extractOne(
        user_input,
        options,
        scorer=fuzz.token_sort_ratio
    )

    if result and result[1] >= threshold:
        return result[0]

    return None


# -------- GENERATE SUGGESTIONS --------
def generate_suggestions(intent, courses, facilities, user_lang):
    """
    Generate smart suggestion buttons for the chatbot UI.
    """

    suggestions = []

    # Shuffle for variety
    random_courses = courses[:]
    random_facilities = facilities[:]

    random.shuffle(random_courses)
    random.shuffle(random_facilities)

    # ---------- COURSE QUESTIONS ----------
    if intent == "courses":

        if random_courses:
            suggestions.append(f"What is the fee for {random_courses[0]['course']}?")

        if len(random_courses) > 1:
            suggestions.append(f"What is the duration of {random_courses[1]['course']}?")

        suggestions.append("What facilities are available?")

    # ---------- FEES QUESTIONS ----------
    elif intent == "fees":

        if random_courses:
            suggestions.append(f"What is the duration of {random_courses[0]['course']}?")

        if len(random_courses) > 1:
            suggestions.append(f"What is the eligibility for {random_courses[1]['course']}?")

        suggestions.append("What courses are offered?")

    # ---------- FACILITIES QUESTIONS ----------
    elif intent == "facilities":

        if random_facilities:
            suggestions.append(f"Is {random_facilities[0]['name']} available?")

        if len(random_facilities) > 1:
            suggestions.append(f"What is the fee for {random_facilities[1]['name']}?")

        suggestions.append("What courses are offered?")

    # ---------- GENERAL (STARTING BUTTONS 🔥) ----------
    else:

        suggestions = [
            "What courses are offered?",
            "What facilities are available?",
            "Tell me about B.Tech fees"
        ]

    # Remove duplicates
    suggestions = list(dict.fromkeys(suggestions))

    # Limit to 3 suggestions
    suggestions = suggestions[:3]

    # Translate suggestions
    translated = [translate_text(s, user_lang) for s in suggestions]

    return translated