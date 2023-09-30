from flask import Flask, render_template, request
import openai
import speech_recognition as sr

app = Flask(__name__)

# Set up OpenAI API key and models
openai.api_key = 'YOUR_API_KEY'
whisper_model = "whisper-large"
chatgpt_model = "gpt-3.5-turbo"

def record_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your audio.")
        return None

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )

    assistant_reply = response['choices'][0]['message']['content']
    return assistant_reply

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_voice', methods=['POST'])
def process_voice():
    voice_input = request.form['voice_input']
    if voice_input:
        response = chat_with_gpt(voice_input)
        return render_template('index.html', voice_input=voice_input, response=response)
    else:
        return render_template('index.html', voice_input="Please try again.", response="")

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/process_voice', methods=['POST'])
def process_voice():
    voice_input = request.form['voice_input']
    
    # Debugging print statements
    print("Received voice input:", voice_input)
    
    if voice_input:
        response = chat_with_gpt(voice_input)
        # Debugging print statements
        print("Generated response:", response)
        return render_template('index.html', voice_input=voice_input, response=response)
    else:
        # Debugging print statements
        print("No voice input received.")
        return render_template('index.html', voice_input="Please try again.", response="")