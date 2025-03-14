from flask import Flask, request
import os

UPLOAD_FOLDER = "/config/www/payment"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Payment Screenshot</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    padding: 4em;
                }}
                .upload-box {{
                    background: white;
                    padding: 4em;
                    border-radius: 24px;
                    max-width: 900px;
                    margin: auto;
                    box-shadow: 0 0 24px rgba(0, 0, 0, 0.2);
                    text-align: center;
                }}
                h2 {{
                    font-size: 3em;
                    margin-bottom: 1.5em;
                    color: #333;
                }}
                input[type='file'] {{
                    font-size: 1.8em;
                    padding: 1.5em;
                    margin-top: 1.5em;
                }}
                input[type='submit'] {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 22px 44px;
                    font-size: 2em;
                    border: none;
                    border-radius: 12px;
                    margin-top: 3em;
                    cursor: pointer;
                }}
                input[type='submit']:hover {{
                    background-color: #45a049;
                }}
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
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta http-equiv='refresh' content='3; url=http://192.168.2.191:8123'>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 4em;
                        background-color: #f9f9f9;
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
                        font-size: 2.5em;
                        color: green;
                    }}
                    p, a {{
                        font-size: 2em;
                        margin-top: 1.5em;
                    }}
                    a {{
                        color: #2196F3;
                        text-decoration: underline;
                    }}
                </style>
            </head>
            <body>
                <div class='success-box'>
                    <h3>✅ File uploaded successfully as {file.filename}</h3>
                    <p>Returning to MyVille Dashboard in 3 seconds...</p>
                    <a href='http://192.168.2.191:8123'>⬅ Tap here if not redirected</a>
                </div>
            </body>
            </html>
        """
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8081)
