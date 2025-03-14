from flask import Flask, request
import os

UPLOAD_FOLDER = "/config/www/payment/2A"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Upload Payment Screenshot</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f0f0f0;
                    padding: 3em;
                }}
                .upload-box {{
                    background: white;
                    padding: 3em;
                    border-radius: 16px;
                    max-width: 700px;
                    margin: auto;
                    box-shadow: 0 0 16px rgba(0, 0, 0, 0.15);
                    text-align: center;
                }}
                h2 {{
                    font-size: 2em;
                    margin-bottom: 1em;
                    color: #333;
                }}
                input[type="file"] {{
                    font-size: 1.2em;
                    padding: 1em;
                    margin-top: 1em;
                }}
                input[type="submit"] {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 15px 30px;
                    font-size: 1.2em;
                    border: none;
                    border-radius: 10px;
                    margin-top: 2em;
                    cursor: pointer;
                }}
                input[type="submit"]:hover {{
                    background-color: #45a049;
                }}
                .back-link {{
                    font-size: 1.2em;
                    margin-top: 2em;
                    display: block;
                    color: #2196F3;
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <div class="upload-box">
                <h2>Upload Payment Screenshot (2A)</h2>
                <form action="/upload_2a" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required><br><br>
                    <input type="submit" value="Upload Screenshot">
                </form>
                <br><br>
                <a href="http://192.168.2.191:8123" class="back-link">⬅ Back to Home Assistant Dashboard</a>
            </div>
        </body>
        </html>
    '''

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
        return f"""<h3>✅ File uploaded successfully as {file.filename}</h3><br>
        <p>Returning to Home Assistant...</p>
        <meta http-equiv="refresh" content="3; url=http://192.168.2.191:8123">
        <a href='http://192.168.2.191:8123' style='font-size:1.2em; color:blue; text-decoration:underline;'>⬅ Tap here if not redirected</a>"""
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8081)
