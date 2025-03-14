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
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f7f7f7;
                    padding: 2em;
                }
                .upload-box {
                    background: white;
                    padding: 2em;
                    border-radius: 10px;
                    max-width: 500px;
                    margin: auto;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                input[type="file"] {
                    margin-bottom: 1em;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="upload-box">
                <h2>Upload Payment Screenshot</h2>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required><br>
                    <input type="submit" value="Upload Screenshot">
                </form>
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
        return f"""<h3>File uploaded successfully as {file.filename}</h3><br>
        <a href='/'>Upload another file</a><br><br>
        <a href='http://192.168.2.191:8123'><br><br>
        <button onclick="window.close()" style="padding:15px 30px; background-color:#f44336; color:white; font-size:1.2em; border:none; border-radius:10px; cursor:pointer;">
        ✖ Close Window
        </button><br><br>
        <button style='padding:10px 16px; background-color:#2196F3; color:white; border:none; border-radius:6px; cursor:pointer;'>
        ⬅ Return to Home Assistant Dashboard
        </button>
        </a>"""
    else:
        return "Invalid file type", 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8081)
