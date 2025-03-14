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
        <html>
        <head><title>Upload Screenshot</title></head>
        <body>
            <h2>Upload Payment Screenshot (2A)</h2>
            <form action="/upload_2a" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <br><br>
                <input type="submit" value="Upload Screenshot">
            </form>
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
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)
        return f"File uploaded successfully as {file.filename}"
    return "Invalid file type", 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=8081)
