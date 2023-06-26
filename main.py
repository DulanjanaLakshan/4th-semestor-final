from flask import Flask, request, jsonify
import speech_recognition as sr
import pyttsx3
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def process_voice():
    def load_intents():
        with open('intents.json') as file:
            intents = json.load(file)
        return intents['intents']

    def initialize_engines():
        recognizer = sr.Recognizer()
        engine = pyttsx3.init()
        return recognizer, engine

    def recognize_speech(recognizer):
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print("You:", text)
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            print("Sorry, an error occurred while accessing the speech recognition service.")
            return ""

    def generate_response(intents, text):
        for intent in intents:
            for pattern in intent.get('patterns', []):
                if pattern in text:
                    return intent['responses']
        return [intent['responses'] for intent in intents if 'unknown' in intent['tag']][0]

    def speak(engine, response):
        for text in response:
            engine.say(text)
            engine.runAndWait()

    def main():
        intents = load_intents()
        recognizer, engine = initialize_engines()

        while True:
            text = recognize_speech(recognizer)
            if text:
                response = generate_response(intents, text)
                speak(engine, response)

    main()
    return "working ..!"


if __name__ == '__main__':
    app.run(debug=True)

