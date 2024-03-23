from flask import Flask, request, send_file
import pyttsx3
import tempfile
import os

app = Flask(__name__)

def speak_text(text, voice_id):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    output_file = tempfile.mktemp(suffix='.mp3')
    engine.save_to_file(text, output_file)
    engine.runAndWait()
    return output_file

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Text to Speech</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }
            .container {
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
                max-width: 600px;
                width: 100%;
                text-align: center;
            }
            h1 {
                color: #333;
            }
            textarea {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                resize: vertical;
                font-size: 16px;
            }
            select, button {
                padding: 10px;
                margin-top: 10px;
                border: none;
                border-radius: 4px;
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
            audio {
                margin-top: 20px;
                width: 100%;
            }
            a {
                display: block;
                margin-top: 10px;
                text-decoration: none;
                color: #4CAF50;
                font-weight: bold;
            }
            p {
                color: #4CAF50;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Text to Speech</h1>
            <form action="/convert" method="post" id="form">
                <textarea name="text" id="text" rows="4" placeholder="Enter text to convert"></textarea><br>
                <select name="voice" id="voice">
                    <option value="0">Voice 1</option>
                    <option value="1">Voice 2</option>
                    <!-- Add more options for different voices -->
                </select><br>
                <button type="submit">Convert</button>
            </form>
            <p id="status" style="display: none;">Text converted successfully!</p>
            <audio controls id="audio" style="display: none;">
                <source id="audio-source" src="" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
            <a href="" id="download" download style="display: none;">Download</a>
        </div>

        <script>
            document.getElementById('form').addEventListener('submit', function(event) {
                event.preventDefault();
                var text = document.getElementById('text').value;
                var voice = document.getElementById('voice').value;
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/convert', true);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.onreadystatechange = function() {
                    if (xhr.readyState == 4 && xhr.status == 200) {
                        document.getElementById('status').style.display = 'block';
                        var response = JSON.parse(xhr.responseText);
                        var audioSource = document.getElementById('audio-source');
                        audioSource.src = '/download/' + response.filename;
                        document.getElementById('audio').load();
                        document.getElementById('audio').style.display = 'block';
                        document.getElementById('download').href = '/download/' + response.filename;
                        document.getElementById('download').style.display = 'block';
                    }
                };
                xhr.send('text=' + text + '&voice=' + voice);
            });

            // Reset audio and download link when text is changed
            document.getElementById('text').addEventListener('input', function() {
                document.getElementById('audio').src = '';
                document.getElementById('audio').style.display = 'none';
                document.getElementById('download').href = '';
                document.getElementById('download').style.display = 'none';
                document.getElementById('status').style.display = 'none';
            });
        </script>
    </body>
    </html>
    """

@app.route('/convert', methods=['POST'])
def convert():
    text = request.form['text']
    voice_id = int(request.form['voice'])
    output_file = speak_text(text, voice_id)
    filename = os.path.basename(output_file)
    return {'filename': filename}

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(tempfile.gettempdir(), filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
