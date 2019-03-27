import os
from flask import Flask, request, redirect, url_for, Blueprint, render_template, send_from_directory

from werkzeug.utils import secure_filename

upload = Blueprint('upload', __name__)

UPLOAD_FOLDER = './static/uploaded'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload', methods=['POST'])

def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template("image-classifier.html", filename=filename) 
        return 'upload error'
    return 'api error'

@upload.route('/upload/<filename>', methods=['GET'])
def send_file(filename):
    if request.method=='GET':
        return send_from_directory(UPLOAD_FOLDER, filename)
    return 'api error'