from flask import Flask, request
import os
from datetime import datetime
import requests

UPLOAD_FOLDER = "/config/www/payment"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

# Home Assistant API Config
HA_URL = "http://192.168.2.191:8123/api/states/input_text.active_user"
HA_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJkMmExMzgzMDFkOWU0NzExYWNkMTEyYWY0NTNmZDMxMCIsImlhdCI6MTc0MTk0Mzk2MSwiZXhwIjoyMDU3MzAzOTYxfQ.5hgLZ0E29HA3fxOIBk8k79OBDDCW4RtpueLtNy84IHc"  # <-- Replace this with your real token

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_active_username():
    try:
        headers = {
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json"
        }
        response = requests.get(HA_URL, headers=headers)
        if response.status_code == 200:
            return response.json().get('state', 'anonymous')
    except:
        pass
    return "anonymous"

@app.route('/')
def index():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Payment Screenshot</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    padding: 4em;
                    font-size: 0.5em;
                }
                .upload-box {
                    background: white;
                    padding: 4em;
                    border-radius: 24px;
                    max-width: 900px;
                    margin: auto;
                    box-shadow: 0 0 24px rgba(0, 0, 0, 0.2);
                    text-align: center;
                }
                h2 {
                    font-size: 2em;
                    margin-bottom: 1.5em;
                    color: #333;
                }
                input[type='file'] {
                    font-size: 1.2em;
                    padding: 1em;
                    margin-top: 1.5em;
                }
                input[type='submit'] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 14px 28px;
                    font-size: 1.5em;
                    border: none;
                    border-radius: 12px;
                    margin-top: 3em;
                    cursor: pointer;
                }
                input[type='submit']:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class='upload-box'>
                <h2>📤 Upload Payment Screenshot</h2>
                <form action='/upload' method='post' enctype='multipart/form-data'>
                    <input type='file' name='file' required><br><br>
                    <input type='submit' value='Upload Screenshot'>
                </form>
            </div>
        </body>
        </html>
    """

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in request", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        username = get_active_username()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        extension = file.filename.rsplit('.', 1)[1].lower()
        new_filename = f"{username}_{timestamp}.{extension}"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(save_path)

        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 4em;
                        background-color: #f9f9f9;
                        font-size: 0.5em;
                    }}
                    .success-box {{
                        background-color: #fff;
                        padding: 4em;
                        border-radius: 24px;
                        max-width: 900px;
                        margin: auto;
                        box-shadow: 0 0 24px rgba(0, 0, 0, 0.2);
                    }}
                    h3 {{
                        font-size: 2em;
                        color: green;
                    }}
                    p {{
                        font-size: 1.5em;
                        margin-top: 1.5em;
                    }}
                </style>
            </head>
            <body>
                <div class='success-box'>
                    <h3>✅ File uploaded successfully as {new_filename}</h3>
                    <p>You may now close this window.</p>
                </div>
            </body>
            </html>
        """
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8081)
