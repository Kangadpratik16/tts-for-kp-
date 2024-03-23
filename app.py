from flask import Flask, render_template, request, send_file
import pyttsx3

app = Flask(__name__)

def speak_text(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    voice_id = int(request.form['voice'])  # Get selected voice ID
    speak_text(text, voice_id)
    return render_template('index.html', text=text, converted=True)

@app.route('/download')
def download():
    return send_file('output.mp3', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)