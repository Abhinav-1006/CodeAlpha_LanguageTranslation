from flask import Flask, render_template, request
import requests

app = Flask(__name__)

LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese"
}

def translate_text(text, source, target):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{source}|{target}"
    }
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    if data.get("responseStatus") != 200:
        raise ValueError(data.get("responseDetails", "Translation service returned an error."))

    return data["responseData"]["translatedText"]

@app.route("/", methods=["GET", "POST"])
def home():
    translated = ""
    original = ""
    source = "en"
    target = "hi"
    error = ""

    if request.method == "POST":
        original = request.form.get("text", "").strip()
        source = request.form.get("source", "en")
        target = request.form.get("target", "hi")

        if not original:
            error = "Please enter some text to translate."
        elif source not in LANGUAGES or target not in LANGUAGES:
            error = "Please choose valid languages."
        elif len(original) > 450:
            error = "Please keep the text under 450 characters for this demo."
        elif source == target:
            translated = original
        else:
            try:
                translated = translate_text(original, source, target)
            except requests.RequestException:
                error = "Could not contact the translation service. Check your internet and try again."
            except (ValueError, KeyError):
                error = "The translation service could not translate this text right now."

    return render_template(
        "index.html",
        languages=LANGUAGES,
        translated=translated,
        original=original,
        source=source,
        target=target,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)
