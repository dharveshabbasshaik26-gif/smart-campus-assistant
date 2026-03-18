from flask import Blueprint, request, jsonify
from models.db import get_db
from utils.helpers import find_best_match, generate_suggestions
from utils.intent_detector import detect_intent
from utils.translator import detect_language, translate_to_english, translate_text

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chat", methods=["POST"])
def chat():

    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"reply": "Please type a message."})

    # -------- LANGUAGE DETECTION --------
    user_lang = detect_language(user_message)

    # Translate user message to English
    message = translate_to_english(user_message).lower().strip()

    intent = detect_intent(message)

    # -------- DATABASE --------
    conn = get_db()

    courses = conn.execute("SELECT * FROM courses").fetchall()
    facilities = conn.execute("SELECT * FROM facilities").fetchall()

    specialisations = conn.execute(
        "SELECT s.specialisation, c.course, s.course_id FROM specialisations s JOIN courses c ON s.course_id=c.id"
    ).fetchall()

    kb_entries = conn.execute("SELECT * FROM knowledge_base").fetchall()

    course_names = [c["course"].lower() for c in courses]
    facility_names = [f["name"].lower() for f in facilities]

    # -------- GREETING --------
    if any(word in message for word in ["hi", "hello", "hey", "namaste"]):

        reply = "Hello! I am your Smart Campus Assistant. Ask me about courses, fees, eligibility or facilities."
        reply = translate_text(reply, user_lang)

        return jsonify({
            "reply": reply,
            "suggestions": generate_suggestions("general", courses, facilities, user_lang)
        })

    # =========================================================
    # ✅ FACILITIES
    # =========================================================
    if intent == "facilities" or any(word in message for word in ["facility", "facilities", "amenities", "services", "campus"]):

        facility_list = ", ".join([f["name"] for f in facilities])

        reply = "Campus facilities include: " + facility_list
        reply = translate_text(reply, user_lang)

        return jsonify({
            "reply": reply,
            "suggestions": generate_suggestions("facilities", courses, facilities, user_lang)
        })

    # -------- FACILITY DETAILS --------
    facility_match = None

    for facility in facilities:
        if facility["name"].lower() in message:
            facility_match = facility
            break

    if not facility_match:
        match = find_best_match(message, facility_names)
        if match:
            facility_match = next(f for f in facilities if f["name"].lower() == match)

    if facility_match:

        if any(word in message for word in ["fee", "fees", "cost", "price"]):
            reply = f"The fee for {facility_match['name']} facility is {facility_match['fees']}."

        elif intent == "duration":
            reply = f"The duration of {facility_match['name']} facility is {facility_match['duration']}."

        else:
            reply = f"{facility_match['name']} facility fee is {facility_match['fees']} and duration is {facility_match['duration']}."

        reply = translate_text(reply, user_lang)

        return jsonify({
            "reply": reply,
            "suggestions": generate_suggestions("facilities", courses, facilities, user_lang)
        })

    # =========================================================
    # ✅ COURSES LIST
    # =========================================================
    if intent == "courses" or any(word in message for word in ["course", "courses", "program", "programs"]):

        course_list = ", ".join([c["course"] for c in courses])

        reply = "Available courses: " + course_list
        reply = translate_text(reply, user_lang)

        return jsonify({
            "reply": reply,
            "suggestions": generate_suggestions("courses", courses, facilities, user_lang)
        })

    # -------- COURSE MATCH --------
    course_match = None

    for course in courses:
        course_name = course["course"].lower()
        clean_course = course_name.replace(".", "")

        if course_name in message or clean_course in message.replace(".", ""):
            course_match = course
            break

    if not course_match:
        match = find_best_match(message, course_names)
        if match:
            course_match = next(c for c in courses if c["course"].lower() == match)

    if course_match:

        # ✅ AVAILABILITY FIX
        if any(word in message for word in ["available", "exist", "offer", "उपलब्ध", "అందుబాటులో"]):
            reply = f"Yes, {course_match['course']} is available."

        # ✅ FEES
        elif any(word in message for word in ["fee", "fees", "cost", "price"]):
            reply = f"The fee for {course_match['course']} is {course_match['fees']}."

        # ✅ DURATION
        elif intent == "duration":
            reply = f"The duration of {course_match['course']} is {course_match['duration']}."

        # ✅ ELIGIBILITY
        elif intent == "eligibility":
            reply = f"The eligibility for {course_match['course']} is {course_match['eligibility']}."

        # ✅ DEFAULT
        else:
            reply = f"{course_match['course']} fee is {course_match['fees']} and duration is {course_match['duration']}."

        reply = translate_text(reply, user_lang)

        return jsonify({
            "reply": reply,
            "suggestions": generate_suggestions("courses", courses, facilities, user_lang)
        })

    # =========================================================
    # ✅ SPECIALISATIONS
    # =========================================================
    if any(word in message for word in ["specialisation", "specialization", "branch", "stream"]):

        for course in courses:
            if course["course"].lower() in message:

                specs = conn.execute(
                    "SELECT specialisation FROM specialisations WHERE course_id=?",
                    (course["id"],)
                ).fetchall()

                spec_list = [s["specialisation"] for s in specs]

                if spec_list:
                    reply = f"{course['course']} specialisations include: " + ", ".join(spec_list)
                else:
                    reply = f"No specialisations found for {course['course']}."

                reply = translate_text(reply, user_lang)

                return jsonify({
                    "reply": reply,
                    "suggestions": generate_suggestions("courses", courses, facilities, user_lang)
                })

    # -------- KNOWLEDGE BASE --------
    kb_questions = [entry["question"].lower() for entry in kb_entries]

    match = find_best_match(message, kb_questions)

    if match:
        entry = next(e for e in kb_entries if e["question"].lower() == match)

        reply = entry["answer"]
        reply = translate_text(reply, user_lang)

        return jsonify({
            "reply": reply,
            "suggestions": generate_suggestions("general", courses, facilities, user_lang)
        })

    # -------- DEFAULT --------
    reply = "Sorry, I didn't understand. Try asking about courses, fees, eligibility or facilities."
    reply = translate_text(reply, user_lang)

    return jsonify({
        "reply": reply,
        "suggestions": generate_suggestions("general", courses, facilities, user_lang)
    })