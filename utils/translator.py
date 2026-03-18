from googletrans import Translator

translator = Translator()


def detect_language(text):
    try:
        result = translator.detect(text)
        return result.lang
    except:
        return "en"


def translate_to_english(text):
    try:
        result = translator.translate(text, dest="en")
        return result.text
    except:
        return text


def translate_text(text, dest_lang):
    try:
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except:
        return text