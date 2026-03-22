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
    text = request.form.get("text", "")
    src = request.form.get("source", "auto")
    dest = request.form.get("target", "en")

    translated = GoogleTranslator(source=src, target=dest).translate(text)

    return render_template("index.html",
                           languages=languages,
                           translated_text=translated,
                           original_text=text,
                           dest_lang=dest)

# 🔊 NEW SPEAK ROUTE
@app.route("/speak", methods=["POST"])
def speak():
    text = request.form.get("text")
    lang = request.form.get("lang", "en")

    tts = gTTS(text=text, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)

    return send_file(filename, as_attachment=False)

if __name__ == "__main__":
    app.run(debug=True)