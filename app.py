from flask import Flask, render_template, request, send_file
from deep_translator import GoogleTranslator
from gtts import gTTS
import os

app = Flask(__name__)

languages = {
    "auto": "Auto Detect",
    "en": "English", "hi": "Hindi", "te": "Telugu", "ta": "Tamil",
    "kn": "Kannada", "ml": "Malayalam", "gu": "Gujarati",
    "bn": "Bengali", "pa": "Punjabi", "mr": "Marathi",
    "ur": "Urdu", "fr": "French", "es": "Spanish",
    "de": "German", "zh-cn": "Chinese", "ja": "Japanese", "ru": "Russian"
}

@app.route("/")
def home():
    return render_template("index.html", languages=languages)

@app.route("/translate", methods=["POST"])
def translate():
    try:
        text = request.form.get("text", "").strip()
        src = request.form.get("source", "auto")
        dest = request.form.get("target", "en")

        if not text:
            return render_template("index.html", languages=languages, error="Enter text")

        translated = GoogleTranslator(source=src, target=dest).translate(text)

        return render_template(
            "index.html",
            languages=languages,
            translated_text=translated,
            original_text=text,
            src_lang=src,
            dest_lang=dest
        )

    except Exception as e:
        return render_template("index.html", languages=languages, error=str(e))


# 🔊 SPEAK ROUTE (gTTS)
@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    lang = request.form.get("lang", "en")

    # gTTS language fix
    if lang == "zh-cn":
        lang = "zh-CN"

    tts = gTTS(text=text, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)

    return send_file(filename, mimetype="audio/mpeg")


# 🚀 IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)