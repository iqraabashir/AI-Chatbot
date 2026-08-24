from deep_translator import GoogleTranslator, MyMemoryTranslator

LANGUAGES = {
    "en": "English",
    "ur": "Urdu",
    "hi": "Hindi",
}


def translate_to_english(text, source_language):

    if source_language == "en":
        return text


    try:

        translator = GoogleTranslator(
            source=source_language,
            target="en"
        )

        result = translator.translate(text)

        if result:
            return result

    except Exception as error:

        print(
            "Google translation failed:",
            error
        )

    try:

        translator = MyMemoryTranslator(
            source=source_language,
            target="en"
        )

        result = translator.translate(text)

        if result:
            return result

    except Exception as error:

        print(
            "Fallback translation failed:",
            error
        )

    raise Exception(
        "Unable to translate the question."
    )


def translate_from_english(text, target_language):

    if target_language == "en":
        return text

    try:

        translator = GoogleTranslator(
            source="en",
            target=target_language
        )

        result = translator.translate(text)

        if result:
            return result

    except Exception as error:

        print(
            "Google translation failed:",
            error
        )

    try:

        translator = MyMemoryTranslator(
            source="en",
            target=target_language
        )

        result = translator.translate(text)

        if result:
            return result

    except Exception as error:

        print(
            "Fallback translation failed:",
            error
        )

    raise Exception(
        "Unable to translate the response."
    )

