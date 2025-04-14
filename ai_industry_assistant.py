import openai
import speech_recognition as sr
import pyttsx3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Domain-specific system prompts
DOMAIN_CONTEXTS = {
    "healthcare": "You are a helpful AI healthcare assistant. You help with patient queries, medication guidance, and medical documentation assistance.",
    "legal": "You are a knowledgeable AI legal assistant. You summarize legal documents, explain case laws, and help with drafting contracts."
}

# Speak response
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Transcribe uploaded audio
def transcribe_audio_file(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio_data)
        except:
            return "Sorry, couldn't understand the audio."

# Generate response from OpenAI based on domain
def generate_response(domain, user_input):
    if domain not in DOMAIN_CONTEXTS:
        return "Unsupported domain. Please choose 'healthcare' or 'legal'."
    prompt = f"{DOMAIN_CONTEXTS[domain]}\nUser: {user_input}\nAI:"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.6
    )
    reply = response.choices[0].text.strip()
    speak(reply)
    return reply

@app.route('/')
def home():
    return "AI-Powered Industry-Specific Assistant is running."

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.form
    domain = data.get('domain')
    question = data.get('question')
    if not domain or not question:
        return jsonify({"error": "Please provide 'domain' and 'question'"}), 400
    answer = generate_response(domain.lower(), question)
    return jsonify({"response": answer})

@app.route('/transcribe', methods=['POST'])
def transcribe_and_respond():
    audio = request.files['audio']
    domain = request.form.get('domain')
    if not domain or not audio:
        return jsonify({"error": "Please provide 'domain' and audio file"}), 400
    audio_path = os.path.join('uploads', audio.filename)
    os.makedirs('uploads', exist_ok=True)
    audio.save(audio_path)
    transcribed = transcribe_audio_file(audio_path)
    response = generate_response(domain.lower(), transcribed)
    return jsonify({"question": transcribed, "response": response})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True, port=5001)
